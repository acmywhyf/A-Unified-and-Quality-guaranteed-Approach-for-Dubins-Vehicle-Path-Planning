import matplotlib.pyplot as plt
import math
import numpy as np
import scienceplots

allpoints = [[(0., 0.), (30., -20)], [(0., 0.), (30., 20)],
             [(0., 0.), (-30., 20)],[(0., 0.), (-30., -20)]]
alljiaodu = [[math.pi / 2, 4.116], [math.pi / 2, 5.320],
             [math.pi / 2, 4.089], [math.pi / 2, 5.317]]

alltpqrs=[[2.175,34.227,	1.563+1.578,34.228,0.967],[0.967,34.228,1.566+1.575,34.228,2.174],
          [0.968,34.230,1.550+1.591,34.228,2.174],[2.175,34.228,1.572+1.570,34.228,0.967]]
alltypes=[[-1,0,-1,0,-1],[-1,0,-1,0,-1],[1,0,1,0,1],[1,0,1,0,1]]
scattersize=0.1
fontsi=3
linewidth=0.5
with plt.style.context(['science','ieee']):


    fig, ax = plt.subplots()
    ax.axis('equal')

    for i in range(4):
        points=allpoints[i]

        theta=alljiaodu[i]


        ax.scatter(points[0][0],points[0][1],marker='o',color='g',s=scattersize)
        plt.text(points[0][0]-1.3,points[0][1]+3,s='start',rotation=0,wrap=True,fontdict={'family':'Arial','fontsize':fontsi})
        ax.arrow(x=points[0][0],y=points[0][1],dx=0,dy=2,width=0.01)

        ax.scatter(points[1][0],points[1][1],marker='o',color='g',s=scattersize)
        plt.text(points[1][0]+2.1,points[1][1]-0.1,s='target'+str(i+1),rotation=0,wrap=True,fontdict={'family':'Arial','fontsize':fontsi})
        ax.arrow(x=points[1][0],y=points[1][1],dx=math.cos(theta[1])*2,dy=math.sin(theta[1])*2,width=0.01)


        zhou = np.arange(start=0, stop=2 * math.pi, step=0.01)
        ax.plot(1 + np.cos(zhou), 0 + np.sin(zhou),'r-',linewidth=linewidth)
        ax.plot(-1 + np.cos(zhou), 0 + np.sin(zhou), 'r-',linewidth=linewidth)
        ax.scatter(1,0,marker='o',color='g',s=scattersize)
        ax.scatter(-1, 0, marker='o', color='g', s=scattersize)


        rcircle=points[1][0]+math.sin(theta[1]),points[1][1]-math.cos(theta[1])

        ax.plot(rcircle[0]+np.cos(zhou),rcircle[1]+np.sin(zhou),'r-',linewidth=linewidth)
        ax.scatter(rcircle[0],rcircle[1],marker='o',color='g',s=scattersize)

        lcircle=points[1][0]-math.sin(theta[1]),points[1][1]+math.cos(theta[1])
        ax.plot(lcircle[0]+np.cos(zhou),lcircle[1]+np.sin(zhou),'r-',linewidth=linewidth)
        ax.scatter(lcircle[0],lcircle[1],marker='o',color='g',s=scattersize)
        print(rcircle,lcircle)

        tpqrs=alltpqrs[i]
        types=alltypes[i]
        shibanjing=1

        now=theta[0]
        curjiao=now
        jiaodu=np.arange(start=now,stop=now+types[0]*tpqrs[0],step=types[0]*0.01)

        ax.plot(points[0][0]+types[0]*np.sin(jiaodu)-types[0]*np.sin(now),points[0][1]-types[0]*np.cos(jiaodu)+types[0]*np.cos(now),'b-.',linewidth=linewidth)


        curjiao=curjiao+types[0]*tpqrs[0]

        xq,yq=points[0][0]+types[0]*np.sin(curjiao)-types[0]*np.sin(now),points[0][1]-types[0]*np.cos(curjiao)+types[0]*np.cos(now)
        xz,yz=xq+tpqrs[1]*np.cos(curjiao),yq+tpqrs[1]*np.sin(curjiao)
        print('xq=',xq,yq,xz,yz)
        ax.scatter(xq,yq,marker='*',color='g',s=scattersize)
        ax.scatter(xz,yz,marker='*',color='k',s=scattersize)
        ax.plot([xq,xz],[yq,yz],'b-.',linewidth=linewidth)

        jiaodu_new=np.arange(start=curjiao,stop=curjiao+types[2]*tpqrs[2],step=0.01*types[2])
        ax.plot(xz+shibanjing*types[2]*np.sin(jiaodu_new)-shibanjing*types[2]*np.sin(curjiao),yz-shibanjing*types[2]*np.cos(jiaodu_new)+shibanjing*types[2]*np.cos(curjiao),'b-.',linewidth=linewidth)

        xq_new,yq_new=xz+shibanjing*types[2]*np.sin(curjiao+types[2]*tpqrs[2])-shibanjing*types[2]*np.sin(curjiao),yz-shibanjing*types[2]*np.cos(curjiao+types[2]*tpqrs[2])+shibanjing*types[2]*np.cos(curjiao)
        ax.scatter(xq_new,yq_new,marker='*',color='g',s=scattersize)
        curjiao=curjiao+types[2]*tpqrs[2]

        xz_new,yz_new=xq_new+tpqrs[3]*np.cos(curjiao),yq_new+tpqrs[3]*np.sin(curjiao)
        ax.scatter(xz_new, yz_new, marker='*', color='k', s=scattersize)

        ax.plot([xq_new,xz_new],[yq_new,yz_new],'g:',linewidth=linewidth)


        print('xqnew',xq_new,yq_new,xz_new,yz_new)

        jiaodu_f=np.arange(start=curjiao,stop=curjiao+types[4]*tpqrs[4],step=0.01*types[4])
        ax.plot(xz_new+1*types[4]*np.sin(jiaodu_f)-1*types[4]*np.sin(curjiao),yz_new-1*types[4]*np.cos(jiaodu_f)+1*types[4]*np.cos(curjiao),'g:',linewidth=linewidth)

    plt.legend(handles=[
        plt.Line2D([0], [0], linestyle='dashdot', color='b', label='first trip'),
        plt.Line2D([0], [0], linestyle='dotted', color='g', label='second trip'),
    ], loc='upper center',
        fontsize=5)
    aa,bb=plt.xlim()
    plt.xlim((aa,bb+2.0))
    plt.savefig('./3.png')
    plt.savefig('./3.pdf')


'''
#计算夹角看对不对。
vec_new=(xz_new-29.2,yz_new-(-19.4)) #圆心 29.2 -19.4
print('vec_new=',vec_new,'vec_new len=',vec_new[0]*vec_new[0]+vec_new[1]*vec_new[1])

vec_target=(0.8,-0.6)
cosjiajiao=vec_new[0]*vec_target[0]+vec_new[1]*vec_target[1]
print('xproduct',cosjiajiao,'jiajiao=',np.arccos(cosjiajiao))
'''
