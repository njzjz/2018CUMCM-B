# result:
         # g1      g2      g3
# c1      383     360     392
# c2      253     211     244
# c3r1    380     356     389
# c3r2    238     200     241 

from system import process_system
if __name__=='__main__':
    # group1
    t_move1=[20,33,46]
    t_load1=[28,31]*4
    t_wash1=25
    
    t_process_single1=560
    tools1=[0, 1, 0, 1, 0, 1, 0, 1]
    t_process1=[400 if tool==0 else 378 for tool in tools1]

    # group2
    t_move2=[23,41,59]
    t_load2=[30,35]*4
    t_wash2=30
    
    t_process_single2=580
    tools2=[1, 0, 1, 0, 1, 0, 1, 0]
    t_process2=[280 if tool==0 else 500 for tool in tools2]
    
    # group3
    t_move3=[18,32,46]
    t_load3=[27,32]*4
    t_wash3=25
    
    t_process_single3=545
    tools3=[0, 1, 0, 0, 1, 0, 0, 1]
    t_process3=[455 if tool==0 else 182 for tool in tools3]

    runtime=8*60*60

    print("\t","g1","\t","g2","\t","g3")
    print("c1","\t",end='')
    # case 1 , group 1
    system=process_system(
        t_move=t_move1,
        t_process=[t_process_single1]*8,
        tools=[0]*8,
        n_process=1,
        t_load=t_load1,
        t_wash=t_wash1
    )
    system.run(runtime)
    with open("case1group1.txt",'w') as f:
        for sample in sorted(system.samples,key=lambda x:x.id):
            print(sample.id+1,sample.CNCid[0]+1,sample.starttime[0],sample.endtime[0],file=f)
    print(len(system.samples),"\t",end='')
    
    # case 1 , group 2
    system=process_system(
        t_move=t_move2,
        t_process=[t_process_single2]*8,
        tools=[0]*8,
        n_process=1,
        t_load=t_load2,
        t_wash=t_wash2
    )
    system.run(runtime)
    with open("case1group2.txt",'w') as f:
        for sample in sorted(system.samples,key=lambda x:x.id):
            print(sample.id+1,sample.CNCid[0]+1,sample.starttime[0],sample.endtime[0],file=f)
    print(len(system.samples),"\t",end='')
            
    # case 1 , group 3
    system=process_system(
        t_move=t_move3,
        t_process=[t_process_single3]*8,
        tools=[0]*8,
        n_process=1,
        t_load=t_load3,
        t_wash=t_wash3
    )
    system.run(runtime)
    with open("case1group3.txt",'w') as f:
        for sample in sorted(system.samples,key=lambda x:x.id):
            print(sample.id+1,sample.CNCid[0]+1,sample.starttime[0],sample.endtime[0],file=f) 
    print(len(system.samples),"\t")    
            
    print("c2","\t",end='')
    # case 2, group 1  
    system=process_system(
        t_move=t_move1,
        t_process=t_process1,
        tools=tools1,
        n_process=2,
        t_load=t_load1,
        t_wash=t_wash1
    )
    system.run(runtime)
    with open("case2group1.txt",'w') as f:
        for sample in sorted(system.samples,key=lambda x:x.id):
            print(sample.id+1,sample.CNCid[0]+1,sample.starttime[0],sample.endtime[0],sample.CNCid[1]+1,sample.starttime[1],sample.endtime[1],file=f)
    print(len(system.samples),"\t",end='')
    
    # case 2, group 2
    system=process_system(
        t_move=t_move2,
        t_process=t_process2,
        tools=tools2,
        n_process=2,
        t_load=t_load2,
        t_wash=t_wash2
    )
    system.run(runtime)
    with open("case2group2.txt",'w') as f:
        for sample in sorted(system.samples,key=lambda x:x.id):
            print(sample.id+1,sample.CNCid[0]+1,sample.starttime[0],sample.endtime[0],sample.CNCid[1]+1,sample.starttime[1],sample.endtime[1],file=f)
    print(len(system.samples),"\t",end='')
    
    # case 2, group 3
    system=process_system(
        t_move=t_move3,
        t_process=t_process3,
        tools=tools3,
        n_process=2,
        t_load=t_load3,
        t_wash=t_wash3
    )
    system.run(runtime)
    with open("case2group3.txt",'w') as f:
        for sample in sorted(system.samples,key=lambda x:x.id):
            print(sample.id+1,sample.CNCid[0]+1,sample.starttime[0],sample.endtime[0],sample.CNCid[1]+1,sample.starttime[1],sample.endtime[1],file=f)
    print(len(system.samples),"\t")
   
    print("c3r1","\t",end='')
    # case 3 , result 1, group 1
    system=process_system(
        t_move=t_move1,
        t_process=[t_process_single1]*8,
        tools=[0]*8,
        n_process=1,
        t_load=t_load1,
        t_wash=t_wash1,
        may_broken=True
    )
    system.run(runtime)
    with open("case3result1group1.txt",'w') as f:
        for sample in sorted(system.samples,key=lambda x:x.id):
            print(sample.id+1,sample.CNCid[0]+1,sample.starttime[0],sample.endtime[0],file=f)
    with open("case3result1group1_broken.txt",'w') as f:
        for broken in sorted(system.brokens,key=lambda x:x.sampleid):
            print(broken.sampleid+1,broken.CNCid+1,broken.starttime,broken.endtime,file=f)
    print(len(system.samples),"\t",end='')
            
    # case 3 , result 1 , group 2
    system=process_system(
        t_move=t_move2,
        t_process=[t_process_single2]*8,
        tools=[0]*8,
        n_process=1,
        t_load=t_load2,
        t_wash=t_wash2,
        may_broken=True
    )
    system.run(runtime)
    with open("case3result1group2.txt",'w') as f:
        for sample in sorted(system.samples,key=lambda x:x.id):
            print(sample.id+1,sample.CNCid[0]+1,sample.starttime[0],sample.endtime[0],file=f)
    with open("case3result1group2_broken.txt",'w') as f:
        for broken in sorted(system.brokens,key=lambda x:x.sampleid):
            print(broken.sampleid+1,broken.CNCid+1,broken.starttime,broken.endtime,file=f)
    print(len(system.samples),"\t",end='')
            
    # case 3 , result 1 , group 3
    system=process_system(
        t_move=t_move3,
        t_process=[t_process_single3]*8,
        tools=[0]*8,
        n_process=1,
        t_load=t_load3,
        t_wash=t_wash3,
        may_broken=True
    )
    system.run(runtime)
    with open("case3result1group3.txt",'w') as f:
        for sample in sorted(system.samples,key=lambda x:x.id):
            print(sample.id+1,sample.CNCid[0]+1,sample.starttime[0],sample.endtime[0],file=f)  
    with open("case3result1group3_broken.txt",'w') as f:
        for broken in sorted(system.brokens,key=lambda x:x.sampleid):
            print(broken.sampleid+1,broken.CNCid+1,broken.starttime,broken.endtime,file=f) 
    print(len(system.samples),"\t")      

    print("c3r2","\t",end='')
    # case 3 , result 2 , group 1
    system=process_system(
        t_move=t_move1,
        t_process=t_process1,
        tools=tools1,
        n_process=2,
        t_load=t_load1,
        t_wash=t_wash1,
        may_broken=True
    )
    system.run(runtime)
    with open("case3result2group1.txt",'w') as f:
        for sample in sorted(system.samples,key=lambda x:x.id):
            print(sample.id+1,sample.CNCid[0]+1,sample.starttime[0],sample.endtime[0],sample.CNCid[1]+1,sample.starttime[1],sample.endtime[1],file=f)  
    with open("case3result2group1_broken.txt",'w') as f:
        for broken in sorted(system.brokens,key=lambda x:x.sampleid):
            print(broken.sampleid+1,broken.CNCid+1,broken.starttime,broken.endtime,file=f) 
    print(len(system.samples),"\t",end='')
    
    # case 2, result 2 , group 2
    system=process_system(
        t_move=t_move2,
        t_process=t_process2,
        tools=tools2,
        n_process=2,
        t_load=t_load2,
        t_wash=t_wash2,
        may_broken=True
    )
    system.run(runtime)
    with open("case3result2group2.txt",'w') as f:
        for sample in sorted(system.samples,key=lambda x:x.id):
            print(sample.id+1,sample.CNCid[0]+1,sample.starttime[0],sample.endtime[0],sample.CNCid[1]+1,sample.starttime[1],sample.endtime[1],file=f)  
    with open("case3result2group2_broken.txt",'w') as f:
        for broken in sorted(system.brokens,key=lambda x:x.sampleid):
            print(broken.sampleid+1,broken.CNCid+1,broken.starttime,broken.endtime,file=f) 
    print(len(system.samples),"\t",end='')
    
    # case 2, result 2 , group 3
    system=process_system(
        t_move=t_move3,
        t_process=t_process3,
        tools=tools3,
        n_process=2,
        t_load=t_load3,
        t_wash=t_wash3,
        may_broken=True
    )
    system.run(runtime)
    with open("case3result2group3.txt",'w') as f:
        for sample in sorted(system.samples,key=lambda x:x.id):
            print(sample.id+1,sample.CNCid[0]+1,sample.starttime[0],sample.endtime[0],sample.CNCid[1]+1,sample.starttime[1],sample.endtime[1],file=f)  
    with open("case3result2group3_broken.txt",'w') as f:
        for broken in sorted(system.brokens,key=lambda x:x.sampleid):
            print(broken.sampleid+1,broken.CNCid+1,broken.starttime,broken.endtime,file=f) 
    print(len(system.samples),"\t",end='')
