import numpy as np
import random


# number of task
m = 19

# number of resources
n = 30

# number of skills
p = 11


ti_duration = [3,5,5,22,22,22,5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5]

D = [];
probD = 0.1
for i in range(0,m):
    for j in range(i+1,m):
        if random.uniform(0, 1) < probD:
            D.append((i+1,j+1));

print D

percentSkill = np.array([7, 10, 43, 5, 10, 15, 1, 1, 5, 2, 1])
percentSkill = percentSkill * 2;
print percentSkill

TREQ = np.zeros((m,p))

low = 5
high = 15

for i in range(0,p):
    k = m * percentSkill[i] / 100
    k = min(k, high)
    k = max(k, low)
    remain = m
    print k, remain
    for j in range(0,m):
        if k <= 0:
            break
        if random.randint(0,100) > k*100/remain:
            remain -= 1
            continue
        # task j+1 need skill i+1
        TREQ[j,i] = 1
        k -= 1
        remain -= 1

print TREQ

LEXP = np.zeros((n,p))

for i in range(0,n):
    for j in range(0,p):
        LEXP[i,j] = random.randint(0,100) / 100.0;

print LEXP


f= open("data.txt","w+")

f.write("Data for problem : Optimize assignment and schedule for project in software")

# number of task
f.write("\n - number of task :")
f.write("\n%d" % m)

# number of resources
f.write("\n - number of resources :")
f.write("\n%d" % n)

# number of skills
f.write("\n - number of skills ")
f.write("\n%d" % p)

f.write("\n - task duration , 1D array len = %d\n" % m)
for i in range(0,m):
    f.write("%d " % ti_duration[i])

f.write("\n - dependency relationship : D = (t_i,t_j) " )
f.write("\n - size D :" )
f.write("\n %d" % D.__len__())
for (i,j) in D:
    f.write("\n%d %d" %(i,j))

f.write("\n - TREQ matrix : size %dx%d " %(m,p))
for i in range(0,m):
    f.write("\n")
    for j in range(0,p):
        f.write("%d " % TREQ[i,j])

f.write("\n - LEXP matrix : size %dx%d" %(n,p))
for i in range(0,n):
    f.write("\n")
    for j in range(0,p):
        f.write("%5.2f" % LEXP[i,j])