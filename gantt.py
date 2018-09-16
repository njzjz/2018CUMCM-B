import matplotlib.pyplot as plt
import numpy as np

height=16
interval=4
colors = ("turquoise","crimson","black","red","yellow","green","brown","blue")

for table,n_process in zip(["case1group1","case1group2","case1group3","case2group1","case2group2","case2group3","case3result1group1","case3result1group2","case3result1group2","case3result2group1","case3result2group2","case3result2group3"],([1]*3+[2]*3)*2):
    df=np.loadtxt(table+".txt")
    df=df[np.where(df[:,3]<3600*8)]
    
    fig,ax=plt.subplots(figsize=(6,3))
    labels=[]
    count=0;
    for i,machine in enumerate(range(8)):
        labels.append(str(i+1))
        data=str(i+1)
        rows=df[np.where(df[:,1]==i+1)]
        for row in rows:        
            ax.broken_barh([(row[2],row[3]-row[2])], ((height+interval)*i+interval,height), facecolors=colors[i])
            plt.text(row[2], (height+interval)*(i+1),int(row[0]),fontsize=2)  
            if(row[3]>count):
                count=row[3]
    if n_process==2:
        for i,machine in enumerate(range(8)):
            labels.append(str(i+1))
            data=str(i+1)
            rows=df[np.where(df[:,4]==i+1)]
            for row in rows:        
                ax.broken_barh([(row[5],row[6]-row[5])], ((height+interval)*i+interval,height), facecolors=colors[i])
                plt.text(row[5], (height+interval)*(i+1),int(row[0]),fontsize=2)  
                if(row[6]>count):
                    count=row[6]
    ax.set_ylim(0, (height+interval)*len(labels)+interval)
    ax.set_xlim(0, count+2)
    ax.set_yticks(range(interval+height//2,(height+interval)*len(labels),(height+interval)))
    ax.set_yticklabels(labels)
    ax.xaxis.grid(True)
    plt.savefig(table+'.png',dpi=800)
    plt.clf()