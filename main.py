import numpy as np
import LoadInput
import Objectives
import Utils
import NSGAII



# load input data

input_params = LoadInput.getIput("data.txt")
m,n,p,D,t_duration,TREQ,LEXP = input_params

print D
# nsga params
pop_size = 100
Pc = 0.9
Pm = 0.1
max_gen = 10
nsga_param = (pop_size, Pc, Pm, max_gen)

#init population
population = Utils.initPopulation(pop_size, input_params)

obj_constr = []
for i in range(0,pop_size):
    obj_constr.append(Objectives.objectives_constraints(population[i],input_params))
# for i in range(0,pop_size):
#     print "%d  : "%i , obj_constr[i]
# print NSGAII.fast_nondominated_sort(obj_constr)
populationInfo = []
for i in range(0,pop_size):
    populationInfo.append((population[i],obj_constr[i]))

# populationSelected = NSGAII.selection(populationInfo,50)
# for data,obj_constr in populationSelected:
#     print "------------------------------------------------------------"
#     print "data " , data
#     print "obj_constr " , obj_constr
    #print Objectives.objectives_constraints(data,input_params)
#Utils.printPop(population,n)
P = NSGAII.algorithm(population, nsga_param, input_params)

Utils.printPop(populationInfo, 30)
for i in range(0,1):
    Utils.drawGanttChart(P[i],input_params, "name%d"%i)