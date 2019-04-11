import numpy as np
import random
import Objectives

INFINITY = 10000
def getDominateState(obj_constr1, obj_constr2):
    # 1 dominate 2 : return 1
    # 2 dominate 1 : return -1
    # ono-dominate : return 0
    obj1, constr1 = obj_constr1
    obj2, constr2 = obj_constr2
    first_dominate = False
    second_dominate = False
    for i in range(0,obj1.__len__()):
        if obj1[i] > obj2[i]:
            first_dominate = True
        if obj2[i] > obj1[i]:
            second_dominate = True
    # for i in range(0,constr1.__len__()):
    #     if constr1[i] > constr2[i]:
    #         first_dominate = True
    #     if constr2[i] > constr1[i]:
    #         second_dominate = True
    if first_dominate==True and second_dominate == False:
        return 1
    if second_dominate == True and first_dominate == False:
        return -1
    return 0

def fast_nondominated_sort(obj_constr):
    # obj_constr[i] contain all objective and constraint value of i-th element
    # return the indices after sorted by front
    # F[i-1] is the indices of i-th non-dominated front of population
    size = obj_constr.__len__()
    # n[i-1] : number of current element dominate the i-th element
    n = np.zeros(shape=size)
    S = []
    firstFront = []
    for i in range(0,size):
        S.append([])
    for i in range(0,size):
        for j in range(0,size):
            if i == j:
                continue
            comp = getDominateState(obj_constr[i], obj_constr[j])
            if comp == 1:
                S[i].append(j)
            elif comp == -1:
                n[i] += 1
        if n[i] == 0:
            firstFront.append(i)

    F = []
    ind = 0
    nextFront = firstFront
    while nextFront.__len__()>0:
        F.append(nextFront)
        nextFront = []
        for i in F[ind]:
            for j in S[i]:
                n[j] -= 1
                if n[j]==0:
                    nextFront.append(j)
        ind += 1

    return F

def sort_by_crowding_distance(obj_constr):
    # obj_constr[i] contain all objective and constraint value of i-th element
    # return the indices after sorted by crowing distance
    # TODO : implement
    objects = []
    constraints = []
    for obj, constr in obj_constr:
        objects.append(obj)
        constraints.append(constr)
    m = objects[0].__len__()
    pop_size = objects.__len__()
    distance = np.zeros(pop_size)
    for t in range(0,m):
        def cmp(ind1,ind2):
            diff = objects[ind1][t] - objects[ind2][t]
            if diff > 0:
                return 1
            if diff < 0:
                return -1
            return 0
        sortedIndices = list(range(pop_size)) # init array 0,1,2,..,popsize
        sortedIndices.sort(cmp)
        distance[sortedIndices[0]] += INFINITY
        distance[sortedIndices[pop_size-1]] += INFINITY
        for i in range(1,pop_size-1):
            distance[sortedIndices[i]] += objects[sortedIndices[i+1]][t] + objects[sortedIndices[i-1]][t]

    def cmp_by_distance(ind1,ind2):
        diff = distance[ind1] - distance[ind2]
        if diff < 0:
            return 1
        if diff > 0:
            return -1
        return 0
    sortedIndices = list(range(pop_size))
    sortedIndices.sort(cmp_by_distance)
    return sortedIndices

def crowding_distance_selection(obj_constrs, frontIndices, max_element):

    # select max_element best element
    if(frontIndices.__len__() <= max_element):
        return frontIndices
    # sort and select
    obj_constrs_front = []
    cnt = 0
    mapping = np.empty(shape=frontIndices.__len__(), dtype=int)
    for index in frontIndices:
        obj_constrs_front.append(obj_constrs[index])
        mapping[cnt] = index
        cnt += 1

    sortedIndices = sort_by_crowding_distance(obj_constrs_front)
    ans = []
    for i in range(0,max_element):
        ans.append(mapping[sortedIndices[i]])
    return ans

def selection(populationInfo, popSize):
    # select pop_size elements from population
    obj_constrs = []
    for data,obj_constr in populationInfo:
        obj_constrs.append(obj_constr)
    F = fast_nondominated_sort(obj_constrs)
    n_front = F.__len__();
    result = []
    for i in range(0,n_front):
        current_len = result.__len__()
        if current_len < popSize:
            result += crowding_distance_selection(obj_constrs,F[i],popSize - current_len)
        if result.__len__() >= popSize:
            break
    ans = []
    for index in result:
        ans.append(populationInfo[index])
    return ans

def make_new_pop(populationInfo,Pc,Pm,input_params):
    # TODO : crossover, mutation
    # expect Pc + Pm <= 1
    def copyParent(p_data):
        p_sched,p_assign = p_data
        t_sched =[]
        t_assign = []
        for i in range(0,p_sched.__len__()):
            t_sched.append(p_sched[i])
            t_assign.append(p_assign[i])
        return [t_sched,t_assign]
    def find2DifferentRandomPos(maxPos):
        pos1 = random.randint(0, maxPos-1)
        pos2 = random.randint(1, maxPos-1)
        if pos2 == pos1:
            pos2 = 0
        if pos1 > pos2:
            temp = pos1
            pos1 = pos2
            pos2 = temp
        return pos1,pos2

    newPopInfo = []
    popSize = populationInfo.__len__()
    indices = list(range(popSize))
    random.shuffle(indices)
    numCross = int(popSize*Pc/2)
    numMutate = int(popSize*Pm/2)
    for i in range(0,numCross):
        ind1 = indices[(2 * i)%popSize]
        ind2 = indices[(2 * i + 1)%popSize]
        data1, _ = populationInfo[ind1]
        data2, _ = populationInfo[ind2]
        # dont change data1 and data2, make the copy and cross it
        child1 = copyParent(data1)
        child2 = copyParent(data2)
        t_sched1, t_assign1 = child1
        t_sched2, t_assign2 = child2
        n = t_sched1.__len__()
        pos1,pos2 = find2DifferentRandomPos(n)
        for pos in range(pos1,pos2):
            dif = t_sched1[pos]-t_sched2[pos]
            amount = int(abs(dif)*10/100)
            if dif>0:
                amount = -amount
            t_sched1[pos] += amount
            t_sched2[pos] -= amount
            #switch t_assign
            temp = t_assign1[pos]
            t_assign1[pos] = t_assign2[pos]
            t_assign2[pos] = temp
        newPopInfo.append((child1,Objectives.objectives_constraints(child1,input_params)))
        newPopInfo.append((child2,Objectives.objectives_constraints(child2,input_params)))
    for i in range(0,numMutate):
        ind = indices[(2 * numCross + i) % popSize]
        data,_ = populationInfo[ind]
        child = copyParent(data)
        t_sched, t_assign = child
        n = t_sched.__len__()
        pos = random.randint(0, n-1)
        if pos >= t_assign.__len__():
            print "pos " , pos , "    " , t_assign.__len__()
        t_assign[pos] = random.randint(1, (1 << n) - 1)
        newPopInfo.append((child,Objectives.objectives_constraints(child,input_params)))

    return newPopInfo

def algorithm(pop_init, alg_params, input_params):
    pop_size, Pc, Pm, max_gen = alg_params
    populationInfo = []
    for i in range(0, pop_size):
        populationInfo.append((pop_init[i], Objectives.objectives_constraints(pop_init[i],input_params)))

    P = [populationInfo]
    Q = [[]]
    for t in range(max_gen):
        print "gen " , t
        Rt = P[t] + Q[t]
        new_P = selection(Rt, pop_size)
        P.append(new_P)
        Q.append(make_new_pop(new_P,Pc,Pm,input_params))
    return P[max_gen]
