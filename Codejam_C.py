from fractions import gcd
t = input()
data =[]
for k in range(0,t):
    n,l = map(int,raw_input().split())
    a = map(int,raw_input().split())
    data.append((n,l,a))
for k in range(0,t):
    # n,l = map(int,raw_input().split())
    # a = map(int,raw_input().split())
    n,l,a = data[k]
    b = []
    ans = []
    for i in range(0,l+1):
        ans.append(0);
    for i in range(0,l-1):
        if (a[i]==a[i+1]):
            b.append(1)
        else:
            b.append(gcd(a[i],a[i+1]))
    ind = 0
    for i in range(0,l-1):
        if(b[i]!=1):
            ind = i
            break
    ans[ind] = a[ind]/b[ind]
    for i in range(ind+1,l+1):
        ans[i] = a[i-1]/ans[i-1];
    for i in range(ind-1,-1,-1):
        ans[i] = a[i+1]/ans[i+1]

    temp = []
    for i in range(0,l+1):
        temp.append(ans[i])
    ans.sort()
    map = {}
    char = 'A'
    for i in range(0,l):
        if ans[i]!= ans[i+1]:
            map[ans[i]] = char
            char = chr(ord(char) + 1)
    map[ans[l]] = 'Z'
    s = ""
    for i in range(0,l+1):
        s += map[temp[i]]
    print "Case #%d:" %(k+1), s

