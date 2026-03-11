import map
import numpy as np
#%%
#___________parameters
n = 4       #num of points
nv = 2      #num of vehicles
map_size = 8

#_________setup
cost = 0 
p,m = map.carte(n,map_size)

#%%
# we have n vehicles
vehs = {i: [0, i, 0] for i in range(1, n)}

sav = []    #savings

for a in range (n):
    for b in range(a+1,n):
        s = m[0][a] + m[0][b] - m[a][b]
        sav.append((s, a, b))

#sort savings
sav.sort(reverse=True)


# we combine 2 vehicle, the ones where saving are the gratest
for s, a, b in sav:
    print("a,b:",a,b)
    for r in vehs:
        #print (r)
        if a in vehs[r]:
            ra = vehs[r]  #vehicle with a in route
            ia = r
        if b in vehs[r]:
            rb = vehs[r]  #vehicle with b in route
            ib = r
    
    print(ra,rb)

    if ra != rb:    #if not already in one route
        if ra[-2] == a and rb[1] == b:    #possible connection ra ->rb
            ra = ra[:-1] + rb[1:]
            vehs[ia] = ra
            del vehs[ib]
        elif ra[1] == a and rb[-2] == b:    #possible connection rb ->ra
            rb = rb[:-1] + ra[1:]
            vehs[ib] = rb
            del vehs[ia]
        elif ra[-2] == a and rb[-2] == b:    #possible connection ra ->br
            #print("aaaa")
            ra = ra[:-1] + (rb[:-1])[::-1]
            vehs[ia] = ra
            del vehs[ib]
        elif ra[1] == a and rb[1] == b:    #possible connection br ->ra
            #print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
            rb = (rb[1:])[::-1] + ra[1:]
            vehs[ib] = rb
            del vehs[ia]

    print("vehs:",vehs,"\n")

    if len(vehs)==1:
        break





# %%
