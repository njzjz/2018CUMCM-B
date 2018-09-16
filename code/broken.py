# Last line of the result:
# 10000000000 0.0099099874

import random,math
p_final=0.01
timestep=1
t_fix_ava=15*60
time=0
p=p_final/t_fix_ava*timestep

state=0
t_fixing=0
t_fixtotal=0

while time<10**10:
    if state==1:
        if t_fixing<t_fix:
            t_fixing+=timestep
            t_fixtotal+=timestep
        else:
            state=0
    else:
        if random.random()<p:
            state=1
            t_fixing=0
            t_fix=random.randint(10*60,20*60)

    time+=timestep
    if time%1000==0:
        print(time,t_fixtotal/time)
