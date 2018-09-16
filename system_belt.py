import numpy as np
import random
import math

# state
STATE_REST=0
STATE_PROCESS=1
STATE_LOAD=2
STATE_WASH=3
STATE_MOVE=4
STATE_BROKEN=5

class process_system(object):
    def __init__(self,t_move,t_process,tools,n_process,t_load,t_wash,may_broken=False):
        self.t_move=t_move
        self.t_process=t_process
        self.t_load=t_load
        self.t_wash=t_wash
        self.tools=tools
        self.n_process=n_process
        self.may_broken=may_broken
        
        self.timestep=1
        self.t_broken_range=[10*60,20*60]
        self.p_final=0.01
        self.p_broken=self.p_final/np.average(self.t_broken_range)*self.timestep
        
        self.n_CNC=8
        self.t_move_CNC=np.array([[
            ([0]+self.t_move)[abs(i//2-j//2)]
        for j in range(self.n_CNC)] for i in range(self.n_CNC)])
        
        self.CNC=[machine_CNC(id=i,t_process=self.t_process[i],tool=self.tools[i],system=self,may_broken=self.may_broken) for i in range(self.n_CNC)]
        self.RGV=machine_RGV(t_move_CNC=self.t_move_CNC,t_load=self.t_load,t_wash=t_wash,system=self)
        self.n_sample=0
        self.samples=[]
        self.uncompleted_samples=[]
        if self.may_broken:self.brokens=[]

    def run(self,t_run):
        self.state=STATE_PROCESS
        for self.time in range(0,t_run,self.timestep):
            # Last
            for CNC in self.CNC:
                CNC.before(self.timestep)
            self.RGV.before(self.timestep)
            for CNC in self.CNC:
                CNC.last(self.timestep)
            self.RGV.last(self.timestep)
        if self.RGV.sample is not None:
            if self.RGV.sample.processstep+1>=self.n_process:
                self.samples.append(self.RGV.sample)
                        
    def determine(self,requirements):
        # Here is what we need to discuss
        move_time=[(0 if self.CNC[requirement].t_statetotal-self.CNC[requirement].t_state<=self.t_move_CNC[self.RGV.position][requirement] else self.CNC[requirement].t_statetotal-self.CNC[requirement].t_state-self.t_move_CNC[self.RGV.position][requirement])+ self.t_move_CNC[self.RGV.position][requirement]+self.t_load[requirement]+self.t_wash for requirement in requirements]
        best=requirements[np.where(move_time==np.min(move_time))[0][0]]
        return best
      
class machine(object):  
    def last(self,timestep):
        if not self.state==STATE_REST:
            self.t_state+=timestep
        
class machine_CNC(machine):
    def __init__(self,id,t_process,tool,system,may_broken=False):
        self.t_process=t_process
        self.system=system
        self.tool=tool
        self.may_broken=may_broken
        self.id=id

        self.state=STATE_REST
        self.t_state=0
        self.t_statetotal=0
        self.sample=None
        self.determine=None

    def before(self,timestep):
        #before
        self.checkbroken()
        if not self.state==STATE_REST:
            if self.t_state>=self.t_statetotal:
                self.state=STATE_REST
                self.t_state=0
                self.t_statetotal=0
    
    def checkbroken(self):
        if self.may_broken and self.state==STATE_PROCESS:
            if random.random()<self.system.p_broken:
                # broken
                broken=Broken(sampleid=self.sample.id,CNCid=self.id)
                self.sample=None
                self.state=STATE_BROKEN
                self.t_state=0
                self.t_statetotal=random.randint(self.system.t_broken_range[0],self.system.t_broken_range[1])
                broken.starttime=self.system.time
                broken.endtime=self.system.time+self.t_statetotal
                self.system.brokens.append(broken)
    
class machine_RGV(machine):
    def __init__(self,t_move_CNC,t_load,t_wash,system):
        self.t_move_CNC=t_move_CNC
        self.t_load=t_load
        self.t_wash=t_wash
        self.system=system
        
        self.state=STATE_REST
        self.t_state=0
        self.t_statetotal=0
        self.sample=None
        self.unload_sample=None
        self.load_sample=None
        self.position=1
        self.determine=None

    def before(self,timestep):
        if not self.state==STATE_REST:
            if self.t_state>=self.t_statetotal:
                self.t_statetotal=0
                self.t_state=0
                self.todo()
        else:
            self.todo()
    
    def todetermine(self):
        if self.determine is None:
        # Determine what to do
            requirements=[i for i in range(len(self.system.CNC))
                            if (self.system.CNC[i].tool==0 or len(self.system.uncompleted_samples)>0) ]

            if requirements:
                self.determine=self.system.determine(requirements)
            
    def todo(self):
        #Before a timestep starts
        self.todetermine()
        if self.determine is not None:
            if self.state==STATE_REST:
                # move
                if self.t_move_CNC[self.position][self.determine]>0:
                    self.move(self.determine)
                else:
                    self.position=self.determine
                    if self.system.CNC[self.determine].state==STATE_REST:
                        self.load(self.determine)
                    else:
                        self.state=STATE_REST
                        self.determine=None
            elif self.state==STATE_MOVE:
                self.position=self.determine
                if self.system.CNC[self.determine].state==STATE_REST:
                    self.load(self.determine)
                else:
                    self.done()
            elif self.state==STATE_LOAD:
                self.load_complete(self.determine)
            elif self.state==STATE_WASH:
                self.done()
    
    def done(self):
        self.state=STATE_REST
        self.determine=None
        self.todo() # do the next thing
    
    def move(self,move_to):
        self.state=STATE_MOVE
        self.t_statetotal=self.t_move_CNC[self.position][move_to]

    def load(self,id):
        self.state=STATE_LOAD
        self.t_statetotal=self.t_load[id]
        if self.system.CNC[id].sample is not None:
            # unload
            self.unload_sample=self.system.CNC[id].sample
            self.unload_sample.endtime.append(self.system.time)
            self.system.CNC[id].sample=None
        if self.system.state==STATE_PROCESS:
            if self.system.CNC[id].tool==0:
                # new sample
                self.load_sample=Sample(id=self.system.n_sample)
                self.system.n_sample+=1
            else:
                # load from uncompleted samples
                self.load_sample=self.system.uncompleted_samples[0]
                del self.system.uncompleted_samples[0]
            self.load_sample.starttime.append(self.system.time)
        
    def load_complete(self,id):
        # load sample
        if self.load_sample is not None:
            self.system.CNC[id].sample=self.load_sample
            self.load_sample=None
            self.system.CNC[id].state=STATE_PROCESS
            self.system.CNC[id].t_statetotal=self.system.CNC[id].t_process
            self.system.CNC[id].sample.CNCid.append(id)
        # wash sample
        if self.unload_sample is not None:
            if self.sample is not None:
                # complete
                self.sample.processstep+=1
                if self.sample.processstep>=self.system.n_process:
                    # completed sample
                    self.system.samples.append(self.sample)
                else:
                    # uncompleted sample
                    self.system.uncompleted_samples.append(self.sample)
                self.sample=None
            
            self.sample=self.unload_sample
            self.unload_sample=None
            self.state=STATE_WASH
            self.t_statetotal=self.t_wash
        else:
            self.done()

class Sample(object):
    def __init__(self,id):
        self.id=id
        self.processstep=0
        self.CNCid=[]
        self.starttime=[]
        self.endtime=[]
        
class Broken(object):
    def __init__(self,sampleid,CNCid):
        self.sampleid=sampleid
        self.CNCid=CNCid

