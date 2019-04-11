import numpy as np


def getIput(filename):

    # m Tasks
    m = 3
    # duration of tasks
    t_duration = np.ones(m);
    # n Resources
    n = 2
    # p skills
    p = 4
    # task relationship
    D = [(3, 4), (5, 6), (2, 5)]
    #print(D)
    # TREQ matrix
    TREQ = np.zeros((m, p))
    #print(TREQ)
    # LEXP matrix
    LEXP = np.zeros((n, p))
    f = open(filename, "r")
    while f.mode != 'r':
        None
    # first line
    f.readline()
    # read m,n,p
    f.readline()
    m = int(f.readline())
    f.readline()
    n = int(f.readline())
    f.readline()
    p = int(f.readline())
    # task duration
    f.readline()
    t_duration = map(int,f.readline().split())
    #print t_duration.__len__()
    # read dependencies
    f.readline()
    f.readline()
    sizeD = int(f.readline())
    D = []
    for i in range(0,sizeD):
        line = f.readline()
        t_i,t_j = line.split()
        D.append((int(t_i),int(t_j)))
    #print D
    # read TREQ mxp
    f.readline()
    TREQ = []
    for i in range(0,m):
        TREQ.append(map(int, f.readline().split()))
    TREQ = np.array(TREQ)
    # read LEXP mxp
    f.readline()
    LEXP = []
    for i in range(0, n):
        LEXP.append(map(float, f.readline().split()))
    LEXP = np.array(LEXP)

    #print TREQ
    #print LEXP
    return m,n,p,D,t_duration,TREQ,LEXP