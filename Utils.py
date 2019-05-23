# import plotly.figure_factory as ff
# import plotly
import datetime

import numpy as np
import random
import math

START_DATE = datetime.datetime.strptime("2019-01-01", "%Y-%m-%d")

def getDateString(daysAfter):
    date = START_DATE + datetime.timedelta(days=daysAfter)
    return date.strftime("%Y-%m-%d")

def getPrevTasks(params):
    m, n, p, D, t_duration, TREQ, LEXP = params
    prevTasks = [{}]
    for i in range(1, m + 1):
        prevTasks.append([])
    for ti, tj in D:
        prevTasks[tj].append(ti)
    return prevTasks

def getNextTask(params):
    m, n, p, D, t_duration, TREQ, LEXP = params
    nextTasks = [{}]
    for i in range(1, m + 1):
        nextTasks.append([])
    for ti, tj in D:
        nextTasks[ti].append(tj)
    return nextTasks

def myInitRandomElement(params, maxRandom, valid):
    # maxRandom is used for generating next t_sched
    m,n,p,D,t_duration,TREQ,LEXP = params
    # topo sort tasks in D // already sorted because dependency generated consists of (ti,tj) such as ti<tj
    prevTasks = getPrevTasks(params)
    element = np.empty(shape = (2,m), dtype=int)
    # init element[0] = t_sched
    t_sched = np.empty(shape=m, dtype=int)
    t_assign = np.empty(shape=m, dtype=int)
    for j in range(1,m+1):
        tj_sched = 1
        for i in prevTasks[j]:
            tj_sched = max(tj_sched,t_sched[i-1]+t_duration[i-1])
        t_sched[j-1] = tj_sched + random.randint(0,maxRandom);
    # init element[1] = ti_assign
    # assume that n <= 63
    # random from 1 to 2^n-1 because at least one resource is assigned to each task
    for i in range(0,m):
        t_assign[i] = random.randint(1,(1<<n)-1)
        for bit in range(0,n):
            if (1<<bit & t_assign[i]) > 0 and (valid[i][j] != 1):
                # if bit is set but resource is useless for task, delete that resource from task
                t_assign[i] -= 1<<bit

        #print "(", "{0:b}".format(t_assign[i]).zfill(n) , ")"

    element[0] = t_sched
    element[1] = t_assign

    return element

def myInitPopulation(pop_size, params):
    m, n, p, D, t_duration, TREQ, LEXP = params
    maxDuration = 0
    for ti_duration in t_duration:
        maxDuration = max(maxDuration,ti_duration)
    pop = [];

    valid = np.zeros((m,n))
    for i in range(0,m):
        for j in range(0,n):
            for k in range(0,p):
                if TREQ[i][k] == 1 and LEXP[j][k]>0:
                    valid[i][j] = 1
                    break

    # print valid
    for i in range(0,pop_size):
        element = myInitRandomElement(params, math.ceil(maxDuration * i * 1.0 / pop_size), valid)
        pop.append(element)
    return pop



def oldInitRandomElement(params, totalDuration):
    # maxRandom is used for generating next t_sched
    m,n,p,D,t_duration,TREQ,LEXP = params
    # topo sort tasks in D // already sorted because dependency generated consists of (ti,tj) such as ti<tj
    prevTasks = getPrevTasks(params)
    element = np.empty(shape = (2,m), dtype=int)
    # init element[0] = t_sched
    t_sched = np.empty(shape=m, dtype=int)
    t_assign = np.empty(shape=m, dtype=int)
    for j in range(1,m+1):
        t_sched[j-1] = random.randint(0,totalDuration)
        # random in range from 0 to totalDuration
    # init element[1] = ti_assign
    # assume that n <= 63
    # random from 1 to 2^n-1 because at least one resource is assigned to each task
    for i in range(0,m):
        t_assign[i] = random.randint(1,(1<<n)-1)
        #print "(", "{0:b}".format(t_assign[i]).zfill(n) , ")"

    element[0] = t_sched
    element[1] = t_assign

    return element

def oldInitPopulation(pop_size, params):
    m, n, p, D, t_duration, TREQ, LEXP = params
    totalDuration = 0
    for ti_duration in t_duration:
        totalDuration += ti_duration

    pop = [];
    for i in range(0, pop_size):
        element = oldInitRandomElement(params, totalDuration)
        pop.append(element)
    return pop


def printPop(populationInfo, numResource):
    x = populationInfo.__len__()
    print "\n Done \n Population include % d element " % x
    ind = 0
    s = []
    numObj = 6
    for i in range(0,numObj):
        s.append(0.0)
    for ele,ob_constr in populationInfo:
        ind += 1
        if(ind < 0):
            print "\n solution %4d. \n t_sched  : " % ind, ele[0]
            print "t_assign  : " ,
            for i in range(0, ele[1].__len__()):
                print "(", ("{0:b}".format(ele[1][i])).zfill(numResource), ")" ,

            print "\nobjective :  ",ob_constr[0]
        for i in range(0, numObj):
            s[i] += ob_constr[0][i]
        # print "constraint : ",ob_constr[1]
    print "\n Average values : [",
    for i in range(0, numObj):
        s[i] /= x
        print format(s[i], '.3f'), "," ,
    print "]"


def drawGanttChart(element, params, filename):
    m, n, p, D, t_duration, TREQ, LEXP = params
    (t_sched,t_assign),(obj,constr) = element
    df = []
    # df = [dict(Task="Job-1", Start='2017-01-01', Finish='2017-02-02', Resource='Complete',.....]
    prevTasks = getPrevTasks(params)
    for i in range(0,m):
        df.append(dict(Task="Task-%d"%(i+1) , Start=getDateString(t_sched[i]), Finish=getDateString(t_sched[i]+t_duration[i]+1), Resource='Complete'))
    colors = {'Not Started': 'rgb(220, 0, 0)',
              'Incomplete': (1, 0.9, 0.16),
              'Complete': 'rgb(0, 255, 100)'}

    fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=False, group_tasks=True, showgrid_x = True, showgrid_y = True)
    #fig['layout'].update(legend={'x': 1, 'y': 1})
    for i in range(1,m+1):
        prevTaskText = 'prevTasks : '
        if(prevTasks[i].__len__()==0):
            prevTaskText += 'none'
        else:
            prevTaskText += str(prevTasks[i])
        fig['data'][i-1].update(text=prevTaskText)

    # save online: plotly.plotly.plot
    # py.plot(fig, filename=filename, world_readable=True, auto_open = False)
    # save offline on local : plotly.offline.plot
    plotly.offline.plot(fig, filename=filename, auto_open=False)