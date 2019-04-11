import plotly.plotly as py
import plotly.figure_factory as ff

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

def initRandomElement(params, maxRandom):
    # maxRandom is used for generating next t_sched
    m,n,p,D,t_duration,TREQ,LEXP = params
    # topo sort tasks in D // already sorted because dependency generated consists of (ti,tj) such as ti<tj
    prevTasks = getPrevTasks(params)
    #print prevTasks
    element = np.empty(shape = (2,m), dtype=int)
    # element[1] = bit represent resource selection
    # init element[0] = {ti_sched}
    t_sched = np.empty(shape=m, dtype=int)
    t_assign = np.empty(shape=m, dtype=int)
    for j in range(1,m+1):
        tj_sched = 1
        for i in prevTasks[j]:
            tj_sched = max(tj_sched,t_sched[i-1]+t_duration[i-1])
        t_sched[j-1] = tj_sched + random.randint(0,maxRandom);
    #print t_duration
    #print t_sched
    # init element[0] = {ti_assign}
    # assume that n <= 63
    # random from 1 to 2^n-1 because at least one resource is assigned to each task
    for i in range(0,m):
        t_assign[i] = random.randint(1,(1<<n)-1)
        #print "(", "{0:b}".format(t_assign[i]).zfill(n) , ")"

    element[0] = t_sched
    element[1] = t_assign

    return element

def initPopulation(pop_size, params):
    m, n, p, D, t_duration, TREQ, LEXP = params
    maxDuration = 0
    for ti_duration in t_duration:
        maxDuration = max(maxDuration,ti_duration)

    pop = [];
    for i in range(0,pop_size):
        element = initRandomElement(params,math.ceil(maxDuration * i *1.0/ pop_size))
        pop.append(element)
    return pop

def printPop(populationInfo, numResource):
    x = populationInfo.__len__()
    print " Population include % d element " % x
    ind = 1
    for ele,ob_constr in populationInfo:
        print "\n\n element %5d. \n t_sched  : " % ind, ele[0]
        print "t_assign  : " ,
        for i in range(0, ele[1].__len__()):
            print "(", "{0:b}".format(ele[1][i]).zfill(numResource), ")" ,
        ind += 1
        print "\nobjective :  ",ob_constr[0]
        print "constraint : ",ob_constr[1]

def drawGanttChart(element, params, filename):
    m, n, p, D, t_duration, TREQ, LEXP = params
    (t_sched,t_assign),(obj,constr) = element
    df = []
    # df = [dict(Task="Job-1", Start='2017-01-01', Finish='2017-02-02', Resource='Complete'),
    #       dict(Task="Job-1", Start='2017-02-15', Finish='2017-03-15', Resource='Incomplete'),
    #       dict(Task="Job-2", Start='2017-01-17', Finish='2017-03-17', Resource='Not Started'),
    #       dict(Task="Job-2", Start='2017-01-17', Finish='2017-02-28', Resource='Complete'),
    #       dict(Task="Job-3", Start='2017-03-10', Finish='2017-03-20', Resource='Not Started'),
    #       dict(Task="Job-3", Start='2017-04-01', Finish='2017-07-20', Resource='Not Started'),
    #       dict(Task="Job-3", Start='2017-05-18', Finish='2017-06-18', Resource='Not Started'),
    #       dict(Task="Job-4", Start='2017-01-14', Finish='2017-03-14', Resource='Complete')]

    for i in range(0,m):
        df.append(dict(Task="Task-%d"%i , Start=getDateString(t_sched[i]), Finish=getDateString(t_sched[i]+t_duration[i]+1), Resource='Complete'))
    colors = {'Not Started': 'rgb(220, 0, 0)',
              'Incomplete': (1, 0.9, 0.16),
              'Complete': 'rgb(0, 255, 100)'}

    fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=True)
    fig['layout'].update(legend={'x': 1, 'y': 1})
    fig['data'][10].update(text="hello")
    fig['layout']['annotations'] = [
        dict(x='2019-01-3', y=10, text="This is a label", showarrow=False, font=dict(color='red'))]
    py.plot(fig, filename=filename, world_readable=True)
