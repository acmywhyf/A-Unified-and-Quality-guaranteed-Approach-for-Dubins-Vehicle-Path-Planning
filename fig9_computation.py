
import gurobipy as gp  
import numpy as np  
from gurobipy import GRB
import matplotlib.pyplot as plt
import time
import math


st_time = time.time()


env = gp.Env('mohuhua_log.log')
env.setParam("NodefileStart", 0.5)
env.setParam("NodefileDir", '.')  

env.start()


scenario_no = 4
allpoints = [[(0., 0.), (30., -20)], [(0., 0.), (30., 20)],
             [(0., 0.), (-30., 20)],[(0., 0.), (-30., -20)]]  
alljiaodu = [[math.pi / 2, None], [math.pi / 2, None],
             [math.pi / 2, None], [math.pi / 2, None]]



for lo in range(scenario_no):  
    points = allpoints[lo]
    jiaodu = alljiaodu[lo]
    

    m = gp.Model('bizhang_inner' + str(lo), env)
    m.reset()
    m.setParam('NonConvex', 2)  
    m.setParam(GRB.param.IntFeasTol, 1e-2)  
    m.setParam(GRB.param.FeasibilityTol, 1e-6)  
    m.setParam(GRB.param.TimeLimit, 7200)
    

    usepwl = True

    
    num_city = len(points)  
    theta = m.addVars(num_city, lb=0., ub=2. * math.pi, vtype=GRB.CONTINUOUS, name='theta')  
    fw = 1. + 1e-1  
    sin_theta = m.addVars(num_city, lb=-fw, ub=fw, vtype=GRB.CONTINUOUS, name='sin_theta')
    cos_theta = m.addVars(num_city, lb=-fw, ub=fw, vtype=GRB.CONTINUOUS, name='cos_theta')
    seglen = 0.01  
    segnum = math.ceil(2.1 * math.pi / seglen)  
    print(seglen, segnum * 2)

    ptx = [-seglen, 0.]  

    for i in range(1, segnum):  
        ptx.append(seglen * i)
        

    ptsx = [math.sin(x) for x in ptx]  
    ptcx = [math.cos(x) for x in ptx]

    ''''''
    for _ in range(num_city):
        if usepwl:
            m.addGenConstrPWL(theta[_], sin_theta[_], xpts=ptx, ypts=ptsx)  
            m.addGenConstrPWL(theta[_], cos_theta[_], xpts=ptx, ypts=ptcx)
        else:
            m.addGenConstrSin(theta[_], sin_theta[_])
            m.addGenConstrCos(theta[_], cos_theta[_])

    M = 1e3  
    eps = 1e-5  
    impo = 1000.  
    twopib = 2 * math.pi + eps


    def CSDSC(i, yi=None):  

        
        
        tpqrs = m.addVars(3, lb=0, ub=[twopib, impo, twopib], vtype=GRB.CONTINUOUS,
                          name='tpqrs__' + str(i))

        
        xy = m.addVars(2, 2, lb=-impo, ub=impo, vtype=GRB.CONTINUOUS, name='xy1__' + str(i))

        
        theta_o = m.addVars(1, lb=0, ub=twopib, vtype=GRB.CONTINUOUS, name='theta_o' + str(i))

        
        zhengshu = m.addVars(2, lb=-1, ub=1, vtype=GRB.INTEGER, name='zhengshu' + str(i))  

        
        f = m.addVars(3, lb=-1, ub=1, vtype=GRB.INTEGER, name='type' + str(i))

        

        
        m.addConstr(f[0] * f[0] >= 1e-2, name='firstseg' + str(i))  
        m.addConstr(f[1] == 0, name='secondseg' + str(i))  
        m.addConstr(f[2]*f[2]>=1e-2,name='thirdseg'+str(i)) 
        
        

        m.addConstr(theta_o[0] + 2 * math.pi * zhengshu[0] == theta[i] + f[0] * tpqrs[0],name='zs0' + str(i))  
        m.addConstr(2 * math.pi * zhengshu[0] <= theta[i] + f[0] * tpqrs[0], name='zs0sj' + str(i))
        m.addConstr(theta[i] + f[0] * tpqrs[0] - 2 * math.pi + eps <= 2 * math.pi * zhengshu[0], name='zs0xj' + str(i))

        cat = m.addVar(name='cos_alpha_pminus_t' + str(i), lb=-fw, ub=fw, vtype=GRB.CONTINUOUS)
        sat = m.addVar(name='sin_alpha_pminus_t' + str(i), lb=-fw, ub=fw, vtype=GRB.CONTINUOUS)

        if not usepwl:
            m.addGenConstrCos(theta_o[0], cat, name='cat__' + str(i))
            m.addGenConstrSin(theta_o[0], sat, name='sat__' + str(i))  
        else:
            m.addGenConstrPWL(theta_o[0], cat, xpts=ptx, ypts=ptcx, name='pwlcat__' + str(i))
            m.addGenConstrPWL(theta_o[0], sat, xpts=ptx, ypts=ptsx, name='pwlsat__' + str(i))

        
        

        
        m.addConstr(xy[1, 0] == points[i][0] + f[0] * 1 * sat - f[0] * 1 * sin_theta[i] + tpqrs[1] * cat, name='xy1x' + str(i))
        m.addConstr(xy[1, 1] == points[i][1] - f[0] * 1 * cat + f[0] * 1 * cos_theta[i] + tpqrs[1] * sat, name='xy1y' + str(i))

        
        finalLR = m.addVar(lb=0, ub=1, vtype=GRB.BINARY, name='finalcircle' + str(i))  

        finalyuanxin = m.addVars(2, lb=-impo, ub=impo, name='finalyuanxin' + str(i))

        m.addConstr(finalyuanxin[0] == points[(i+1) % num_city][0] + 1 * (-sin_theta[(i+1) % num_city]) * (2 * finalLR - 1), name='fyuanxinx' + str(i))
        m.addConstr(finalyuanxin[1] == points[(i+1) % num_city][1] + 1 * (cos_theta[(i+1) % num_city]) * (2 * finalLR - 1), name='fyuanxiny' + str(i))

        
        m.addConstr((xy[1, 0] - finalyuanxin[0]) * (xy[1, 0] - finalyuanxin[0]) + (xy[1, 1] - finalyuanxin[1]) * (
                    xy[1, 1] - finalyuanxin[1])
                    == 1 * 1, name='onfinal' + str(i))  

        
        m.addConstr(cat * (finalyuanxin[0] - xy[1, 0]) + sat * (finalyuanxin[1] - xy[1, 1]) == 0,name='chuizhi2' + str(i))  
        

        
        chaji=m.addVar(lb=-impo,ub=impo,vtype=GRB.CONTINUOUS,name='chaji')
        
        m.addConstr(chaji == cat * (finalyuanxin[1] - xy[1, 1]) - sat * (finalyuanxin[0] - xy[1, 0]),'chaji' + str(i))

        linshi2 = m.addVars(3, lb=0, ub=1, vtype=GRB.INTEGER, name='linshi2sgn' + str(i))
        m.addConstr(linshi2[0] + linshi2[1] + linshi2[2] == 1)
        m.addConstr(f[2] + 1 <= M * (1 - linshi2[0]))
        m.addConstr(-M * (1 - linshi2[0]) <= f[2] + 1)
        m.addConstr(f[2] <= M * (1 - linshi2[1]))
        m.addConstr(-M * (1 - linshi2[1]) <= f[2])
        m.addConstr(f[2] - 1 <= M * (1 - linshi2[2]))
        m.addConstr(-M * (1 - linshi2[2]) <= f[2] - 1)
        m.addConstr(chaji <= -eps + M * (1 - linshi2[0]))
        m.addConstr(chaji <= eps + M * (1 - linshi2[1]))
        m.addConstr(-M * (1 - linshi2[1]) - eps <= chaji)
        m.addConstr(-M * (1 - linshi2[2]) + eps <= chaji)

        m.addConstr(2 * finalLR - 1 == f[2])

        m.addConstr(theta[(i + 1) % num_city] + 2 * math.pi * zhengshu[1] == theta_o[0] + f[2] * tpqrs[2],
                    name='zs2' + str(i))
        m.addConstr(2 * math.pi * zhengshu[1] <= theta_o[0] + f[2] * tpqrs[2], name='zs2sj' + str(i))
        m.addConstr(theta_o[0] + f[2] * tpqrs[2] - 2 * math.pi + eps <= 2 * math.pi * zhengshu[1],
                    name='zs2xj' + str(i))

        

        

        

        

        

        if yi is not None:
            pass
        return gp.quicksum(tpqrs) 
        


    m.addConstr(theta[0] == jiaodu[0])
    

    

    
    tlen0 = CSDSC(0)  
    tlen1 = CSDSC(1)  
    
    
    m.setObjective(tlen0 + tlen1, GRB.MINIMIZE)  
    
    

    
    m.optimize()  
    print('optimization terminated')

    
    if m.status != gp.GRB.INFEASIBLE:  
        print('cost=', m.ObjVal)
        
        for v in m.getVars():
            
            print('%s %lf' % (v.varName, v.x))
        m.printQuality()

        mi = m.ConstrVioIndex
        print(m.ConstrVioIndex)  

        lc = m.getConstrs()
        lq = m.getQConstrs()
        ls = m.getSOSs()
        lg = m.getGenConstrs()
        if (mi < len(lc)):
            print('linear')
            print(lc[mi])
        elif mi < len(lc) + len(lq):
            print('quadratic')
            print(lq[mi - len(lc)])
        elif mi < len(lc) + len(lq) + len(ls):
            print('sos')
            print(ls[mi - len(lc) - len(lq)])
        else:
            print('general')
            print(lg[mi - len(lc) - len(lq) - len(ls)])

        '''根据获得的值，利用dfs或者并查集求出连通块'''
    else:
        print(m.status)
        m.computeIIS()
        m.write('inner1e-2forrelax' + str(lo) + '.ilp')
        print('IIS writed')
