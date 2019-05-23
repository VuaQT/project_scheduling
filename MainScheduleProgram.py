import numpy as np
import LoadInput
import Objectives
import Utils
import NSGAII



# load input data
g = raw_input("Enter file input name : ")

pop_size = 100
Pc = 0.9
Pm = 0.1
max_gen = 200

print "Please choose algorithm : "
print " 1 : original NSGAII using normal init, mutate, crossover procedure"
print " 2 : NSGAII using new init and crossover in a segment"
print " 3 : NSGAII using new init and crossover with dependence tasks"

algorithmType = int(raw_input("Enter your choice : "))


chooseDefault = int(raw_input("Do you want to choose default parameter for algorithm? (1=Yes, others = No) : "))
if chooseDefault != 1:
    pop_size = int(raw_input("Enter population size (recommend 100) pop_size = "))
    Pc = float(raw_input("Enter crossover probability  (recommend 0.9) Pc = "))
    Pm = float(raw_input("Enter mutate probability  (recommend 0.1) Pm = "))
    max_gen = int(raw_input("Enter number of generation (recommend 1000) max_gen = "))


input_params = LoadInput.getIput(g)
m,n,p,D,t_duration,TREQ,LEXP = input_params

nsga_param = (pop_size, Pc, Pm, max_gen)




if algorithmType == 1:
    # init population
    population = Utils.oldInitPopulation(pop_size, input_params)
    obj_constr = []
    for i in range(0, pop_size):
        obj_constr.append(Objectives.objectives_constraints(population[i], input_params))

    # convert to populationInfo
    populationInfo = []
    for i in range(0, pop_size):
        populationInfo.append((population[i], obj_constr[i]))

    # run algorithm
    P = NSGAII.algorithm(population, nsga_param, input_params,1)

    Utils.printPop(populationInfo, n)

elif algorithmType == 2:
    population = Utils.myInitPopulation(pop_size, input_params)
    obj_constr = []
    for i in range(0, pop_size):
        obj_constr.append(Objectives.objectives_constraints(population[i], input_params))

    # convert to populationInfo
    populationInfo = []
    for i in range(0, pop_size):
        populationInfo.append((population[i], obj_constr[i]))

    # run algorithm
    P = NSGAII.algorithm(population, nsga_param, input_params,2)

    Utils.printPop(populationInfo, n)

elif algorithmType == 3:
    population = Utils.myInitPopulation(pop_size, input_params)
    obj_constr = []
    for i in range(0, pop_size):
        obj_constr.append(Objectives.objectives_constraints(population[i], input_params))

    # convert to populationInfo
    populationInfo = []
    for i in range(0, pop_size):
        populationInfo.append((population[i], obj_constr[i]))

    # run algorithm
    P = NSGAII.algorithm(population, nsga_param, input_params,3)

    Utils.printPop(populationInfo, n)
else:
    print "not valid"


# if plot online : plot under 25 chart because "Account limited"
# print "Plotting Gantt Chart..."
# for i in range(0,10):
#     Utils.drawGanttChart(P[i],input_params, "GanttChart/solution%d.html"%i)
print "\n\nFinished !!"