# choose tool for case 2
# Result:
# group1 [0, 1, 0, 1, 0, 1, 0, 1] 253
# group2 [1, 0, 1, 0, 1, 0, 1, 0] 211
# group3 [0, 1, 0, 0, 1, 0, 0, 1] 244

from system import process_system
if __name__=='__main__':
    # group1
    t_move1=[20,33,46]
    t_load1=[28,31]*4
    t_wash1=25    

    # group2
    t_move2=[23,41,59]
    t_load2=[30,35]*4
    t_wash2=30
    
    # group3
    t_move3=[18,32,46]
    t_load3=[27,32]*4
    t_wash3=25

    runtime=8*60*60
    
    # case 2, group 1  
    max1=0
    for i in range(2**8):
        tools=[int(x) for x in bin(i)[2:].zfill(8)]
        t_process1=[400 if tool==0 else 378 for tool in tools]
        system=process_system(
            t_move=t_move1,
            t_process=t_process1,
            tools=tools,
            n_process=2,
            t_load=t_load1,
            t_wash=t_wash1
        )
        system.run(runtime)
        if len(system.samples)>max1:
            max1=len(system.samples)
            tools1=tools
        
    print("group1",tools1,max1)
    
    # case 2, group 2
    max2=0
    for i in range(2**8):
        tools=[int(x) for x in bin(i)[2:].zfill(8)]
        t_process2=[280 if tool==0 else 500 for tool in tools]
        system=process_system(
            t_move=t_move2,
            t_process=t_process2,
            tools=tools,
            n_process=2,
            t_load=t_load2,
            t_wash=t_wash2
        )
        system.run(runtime)
        if len(system.samples)>max2:
            max2=len(system.samples)
            tools2=tools
        
    print("group2",tools2,max2)
    
    # case 2, group 3
    max3=0
    for i in range(2**8):
        tools=[int(x) for x in bin(i)[2:].zfill(8)]
        t_process3=[455 if tool==0 else 182 for tool in tools]
        system=process_system(
            t_move=t_move3,
            t_process=t_process3,
            tools=tools,
            n_process=2,
            t_load=t_load3,
            t_wash=t_wash3
        )
        system.run(runtime)
        if len(system.samples)>max3:
            max3=len(system.samples)
            tools3=tools
        
    print("group3",tools3,max3)