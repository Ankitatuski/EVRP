import map
import numpy as np


def dist_path(r,m):
    total = 0
    for a in range(0,len(r)-1):
        total+=m[r[a],r[a+1]]
    return total

def merge (new_path, new_index, old_index):
    d = dist_path(new_path,m)
    if d<=rang:
        print ("\t",d)
        vehs[new_index] = new_path
        cargo[new_index] += cargo[old_index]
        distance[new_index] = d
        del cargo[old_index]
        del vehs[old_index]
        del distance[old_index]
    else:
        print("\tabv ",d)


#%%
#___________parameters
n = 18       #num of points
nv = 2      #num of vehicles
cv = 20     #capacity of vehicles
map_size = 8
rang = 4*map_size   #vehicle range

#_________setup
cost = 0 
p,m = map.carte(n,map_size, demand=7)

#%%
# we have n vehicles
vehs = {i: [0, i, 0] for i in range(1, n)}
cargo = {i: p[i][2] for i in range(1, n)}
distance = {i: 2*m[0][i] for i in range(1, n)}
print(distance)

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


    if ra != rb and cargo[ia]+cargo[ib]<=cv:    #if not already in one route
        if ra[-2] == a and rb[1] == b:    #possible connection ra ->rb
            ra = ra[:-1] + rb[1:]
            merge(ra,ia,ib)
            """if dist_path(ra,m)<=rang:
                vehs[ia] = ra
                cargo[ia] += cargo[ib]
                del cargo[ib]
                del vehs[ib]
                del distance[ib]"""
        elif ra[1] == a and rb[-2] == b:    #possible connection rb ->ra
            rb = rb[:-1] + ra[1:]
            merge(rb,ib,ia)
            """if dist_path(rb,m)<=rang:
                vehs[ib] = rb
                cargo[ib] += cargo[ia]
                del cargo[ia]
                del vehs[ia]
                del distance [ia]
            else:
                print("aaaaaaaaaaaaaaa")"""
        elif ra[-2] == a and rb[-2] == b:    #possible connection ra ->br
            ra = ra[:-1] + (rb[:-1])[::-1]
            merge(ra,ia,ib)
            """if dist_path(ra,m)<=rang:
                vehs[ia] = ra
                cargo[ia] += cargo[ib]
                del cargo[ib]
                del vehs[ib]
                del distance[ib]"""
        elif ra[1] == a and rb[1] == b:    #possible connection br ->ra
            rb = (rb[1:])[::-1] + ra[1:]
            merge(rb,ib,ia)
            """if dist_path(rb,m)<=rang:
                vehs[ib] = rb
                cargo[ib] += cargo[ia]
                del cargo[ia]
                del vehs[ia]
                del distance [ia]"""

    print("vehs:",vehs,"\n")

    if len(vehs)==1:
        break

print("\n______THE FINAL ANSWER___________")
print("\nvehs:",vehs)
print("cargo: ",cargo)
print("range: ",distance)
print()



# %%
