import Utils
import numpy as np

def F_duration(x, params):
    t_sched = x[0]
    m, n, p, D, t_duration, TREQ, LEXP = params
    prevTasks = Utils.getPrevTasks(params)
    t_start = np.empty(shape=m, dtype=int)
    for j in range(1,m+1):
        tj_start = 1
        for i in prevTasks[j]:
            tj_start = max(tj_start,t_sched[i-1]+t_duration[i-1])
        t_start[j-1] = tj_start;
    Fduration = 0.0
    for i in range(0,m):
        ti_idle = t_sched[i]-t_start[i]
        if ti_idle >=0:
            ti_delay =  1.0/(1+ti_idle);
            Fduration += ti_delay
    return Fduration/m

def F_experience__G_skill(x, params):
    # F_experience in range [0;2] because treq_ik_exp in range [0;2]
    m, n, p, D, t_duration, TREQ, LEXP = params
    Gskill = 0.0
    t_sviolation = np.empty(shape=m)
    Fexperience = 0.0
    t_assign = x[1]
    TREQ_exp = np.empty(shape=(m,p))
    for i in range(0,m):
        ti_exp = 0
        # calculate ti_assigned
        ti_assigned = 0
        for j in range(0, n):
            if ((t_assign[i] & (1 << j)) != 0):
                ti_assigned += 1

        ti_skills = 0
        ti_sviolation = 0
        for k in range(0,p):
            if TREQ[i][k]!=1:
                continue
            ti_skills += 1
            lexp_ik_max = 0
            sum_lexp_ik = 0
            TREQ_exp[i][k] = 0

            for j in range(0,n):
                if((t_assign[i] & (1<<j))==0):
                    continue
                lexp_ik_max = max(lexp_ik_max, LEXP[j][k])
                sum_lexp_ik += LEXP[j][k]
            if ti_assigned > 0:
                TREQ_exp[i][k] = lexp_ik_max + sum_lexp_ik/ti_assigned
            else    :
                TREQ_exp[i][k] = 0
            ti_exp += TREQ_exp[i][k]
            if TREQ_exp[i][k] == 0:
                # sviolation : TREQ_ik = 1 & TREQ_ik_exp = 0
                ti_sviolation += 1
        if ti_skills > 0 :
            t_sviolation[i] = ti_sviolation/ti_skills
            ti_exp /= ti_skills
        else:
            t_sviolation[i] = 0
            ti_exp = 0
        Fexperience += ti_exp
        Gskill += t_sviolation[i]
    return Fexperience/m, Gskill/m

def F_size(x, params):
    Fsize = 0.0
    m, n, p, D, t_duration, TREQ, LEXP = params
    t_assign = x[1]
    t_size = np.empty(shape=m)
    m, n, p, D, t_duration, TREQ, LEXP = params
    for i in range(0, m):
        ti_assigned = 0
        for j in range(0, n):
            if ((t_assign[i] & (1 << j)) != 0):
                ti_assigned += 1
        t_size[i] = 1.0/(1+ti_assigned)
        Fsize += t_size[i]
    return Fsize/m

def G_dependency(x, params):
    # need to minimize G_dependency -> 0
    m, n, p, D, t_duration, TREQ, LEXP = params
    Gdependency = 0.0
    t_dviolations = np.empty(shape=m)
    t_sched = x[0]
    prevTasks = Utils.getPrevTasks(params)
    t_start = np.empty(shape=m, dtype=int)
    for j in range(1, m + 1):
        tj_start = 1
        for i in prevTasks[j]:
            tj_start = max(tj_start, t_sched[i - 1] + t_duration[i - 1])
        t_start[j - 1] = tj_start;
    for i in range(0, m):
        ti_idle = t_sched[i] - t_start[i]
        if ti_idle >= 0:
            t_dviolations[i] = 0
        else:
            t_dviolations[i] = - ti_idle * prevTasks[i+1].__len__()
        Gdependency += t_dviolations[i]
    return Gdependency / m

def G_assignment(x, params):
    Gassignment = 0
    m, n, p, D, t_duration, TREQ, LEXP = params
    segmentTimes = []
    for j in range(0, n):
        segmentTimes.append([])
    t_assign = x[1]
    t_sched = x[0]
    for i in range(0,m):
        for j in range(0,n):
            if (t_assign[i] & (1 << j)) != 0:
                segmentTimes[j].append((t_sched[i],t_sched[i]+t_duration[i]-1))

    def cmp_items(a, b):
        start_a,end_a = a
        start_b,end_b = b
        if start_a > start_b:
            return 1
        elif start_a < start_b:
            return -1
        else:
            if end_a>end_b:
                return 1
            elif end_a<end_b:
                return  -1
            return 0
    for j in range(0,n):
        segmentTimes[j].sort(cmp_items)
        rj_aviolation = 0
        rj_conflict = 0.0
        rj_totalassigned = 0.0
        endTime = 0
        for start_seg, end_seg in segmentTimes[j]:
            if start_seg <= endTime:
                rj_conflict += min(endTime,end_seg)-start_seg+1
            endTime = max(endTime,end_seg)
            rj_totalassigned += end_seg-start_seg+1
        if rj_totalassigned == 0:
            rj_aviolation = 0
        else:
            rj_aviolation = rj_conflict / rj_totalassigned
        Gassignment += rj_aviolation
    return Gassignment/n

def objectives_constraints(x, params):
    F_exp, Gskill = F_experience__G_skill(x,params)
    objectives = [F_duration(x,params), F_exp, F_size(x,params),-G_dependency(x,params), -Gskill, -G_assignment(x,params)]
    constraints = []
    return objectives,constraints