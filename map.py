import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from copy import deepcopy
import joblib
import folium

if not hasattr(np, "float_"):
    np.float_ = np.float64

import osmnx as ox
import networkx as nx

def carte(n, size, chargers=0, plot = False, full = True, time = False):
    pts = points(n,abs(size))   #[x,y,demand/-charging_rate]
    m = distanceMatrix(pts)

    if full:
        for a in range (n):
            for b in range (a,n):
                m[b,a] = m[a,b]


    chargers_list = []
    indexes = [i for i in range(1,n)]
    for a in range(chargers):
        i = random.choice(indexes)
        #pts[i][2] = -1
        chargers_list.append(i)
        indexes.remove(i)

    if plot:
        x = [point[0] for point in pts]
        y = [point[1] for point in pts]
        plt.scatter(x, y)
        plt.scatter(pts[0][0],pts[0][1], color = 'red')
        for a in chargers_list:
            plt.scatter(pts[a][0],pts[a][1], color = 'green')
        ax = plt.gca()
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(1))
        plt.grid(True)
        plt.show()
    if chargers>0:
        """if time:
            timetable = deepcopy(m)
            for a in m:
                for b in a:
                    b*=random.uniform(0.9,1.1)
            return pts,m,timetable,chargers_list"""

        return pts,m,chargers_list
    return pts,m
    

def points(x,d):
    r = []
    for a in range (x):
        r.append([random.randint(-d, d),random.randint(-d, d)])
    return r

def distanceMatrix(p):
    n = len(p)
    m = (np.zeros((n,n)))
    for a in range (n):
        for b in range (a,n):
            #m[a,b] = abs(p[a][0]-p[b][0])+abs(p[a][1]-p[b][1])             #manhattan
            m[a,b] = np.sqrt((p[a][0]-p[b][0])**2+(p[a][1]-p[b][1])**2)     #euclidean
    return m

def draw(path, cords, chargers=[]):
    x = [cords[p][0] for p in path]
    y = [cords[p][1] for p in path]

    colors = ([
    'tab:blue',
    'tab:orange',
    #'tab:green',
    'tab:red',
    'tab:purple',
    'tab:brown',
    'tab:pink',
    'tab:gray',
    'tab:olive',
    'tab:cyan'
    ])

    plt.plot(x, y, marker='.', linestyle='-', color=random.choice(colors))
    plt.plot(x[0],y[0], marker='o', color="red")
    for a in chargers:
        plt.scatter(cords[a][0],cords[a][1], color = 'green', marker='o')

def drawVRP(paths,cords, chargers = [],title = ""):
    for path in paths:
        draw(path,cords)
    for a in chargers:
        plt.scatter(cords[a][0],cords[a][1], color = 'green', marker='o')
    plt.title(title)
    plt.show()

# OPENSTREETMAP
def load_map(place="Lille, France"):
    """
    Load OSM road network
    """
    G = ox.graph_from_place(place, network_type='drive')
    return G


def points_osm(G, n):
    """
    Select n random nodes from OSM graph
    """
    nodes = list(G.nodes)
    selected_nodes = random.sample(nodes, n)

    pts = []
    for node in selected_nodes:
        x = G.nodes[node]['x']  # longitude
        y = G.nodes[node]['y']  # latitude
        pts.append([x, y])

    return pts, selected_nodes


def distanceMatrix_osm(G, selected_nodes):
    """
    Compute real road distance matrix
    """
    n = len(selected_nodes)
    m = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            try:
                dist = nx.shortest_path_length(
                    G,
                    selected_nodes[i],
                    selected_nodes[j],
                    weight='length'
                )
                m[i][j] = int(dist)
            except:
                m[i][j] = 999999  # fallback if no path

    return m


def carte_osm(n, G, chargers = 0, plot=False):
    """
    OSM-based map generator
    """

    pts, selected_nodes = points_osm(G, n)
    m = distanceMatrix_osm(G, selected_nodes)

    chargers_list = []
    indexes = [i for i in range(1,n)]
    for a in range(chargers):
        i = random.choice(indexes)
        chargers_list.append(i)
        indexes.remove(i)
    

    # Plot
    if plot:
        x = [p[0] for p in pts]
        y = [p[1] for p in pts]

        plt.scatter(x, y)
        plt.scatter(pts[0][0], pts[0][1], color='red')  # depot
        for a in chargers_list:
            plt.scatter(pts[a][0],pts[a][1], color = 'green')   #chargers
        plt.title("OSM Map (Real World)")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.show()

    if chargers>0:
        return pts,m,chargers_list

    return pts, m

def draw_real(paths,pts,chargers = []):
    colors = [
        "red", "blue",
        #"green",
        "purple", "orange", "darkred", "cadetblue", "darkgreen"
    ]

    for i in range(len(pts)):
        #print(pts[i])
        pts[i] = [pts[i][1],pts[i][0]]
        #print("\t",pts[i])
    

    routes = [[pts[a] for a in path] for path in paths]

    m = folium.Map(location=pts[0], zoom_start=13)

    #for route, color in zip(routes, colors):
    for i, route in enumerate(routes):
        color = colors[i]
        #print(i,colors[i])
        folium.PolyLine(route, color=color, weight=4).add_to(m)
    
    for c in chargers:
        folium.CircleMarker(
                location=pts[c],
                radius=8,
                color="darggreen",
                fill=True,
                fill_color="green",
                fill_opacity=1.0,
                weight=2,
            ).add_to(m)
    folium.CircleMarker(
                location=pts[0],
                radius=8,
                color="darkred",
                fill=True,
                fill_color="red",
                fill_opacity=1.0,
                weight=2,
            ).add_to(m)

    m.save("routes.html")
    print("Visualisation Saved to routes.html")

#for AI calculating energy use

def input_generator(size,speed_range = (1,120), max_slope = 10, temp_range=(-5,40), humidity_range=(20,90),wind_range=(0,15)):
    speed = np.zeros((size,size))
    for a in range(size):
        for b in range(a,size):
            if a!=b:
                r = random.randrange(*speed_range)
                speed[a][b] = r
                speed[b][a] = r
    
    slope = np.zeros((size,size))
    for a in range(size):
        for b in range(a,size):
            if a!=b:
                r = random.randrange(-max_slope,max_slope)
                slope[a][b] = r
                slope[b][a] = -r

    temp = np.zeros((size,size))
    for a in range(size):
        for b in range(a,size):
            if a!=b:
                r = random.randrange(*temp_range)
                temp[a][b] = r
                temp[b][a] = -r

    road = np.zeros((size,size))
    for a in range(size):
        for b in range(a,size):
            if a!=b:
                r = random.randint(1,3)
                road[a][b] = r
                road[b][a] = -r
    
    humidity = np.zeros((size,size))
    for a in range(size):
        for b in range(a,size):
            if a!=b:
                r = random.randint(*humidity_range)
                humidity[a][b] = r
                humidity[b][a] = r

    wind = np.zeros((size,size))
    for a in range(size):
        for b in range(a,size):
            if a!=b:
                r = random.randint(*wind_range)
                wind[a][b] = r
                wind[b][a] = r

    weather = np.zeros((size,size))
    for a in range(size):
        for b in range(a,size):
            if a!=b:
                r = random.randint(1,4)
                weather[a][b] = r
                weather[b][a] = r

    traffic = np.zeros((size,size))
    for a in range(size):
        for b in range(a,size):
            if a!=b:
                r = random.randint(1,3)
                traffic[a][b] = r
                traffic[b][a] = r
    
    return speed, slope, temp, road, humidity, wind, weather, traffic
    
#turns distance matrix into baterry usage matrix
def battery_predictor(dist, speed, slope, temp, road, humidity, wind, weather, traffic):
    model = joblib.load("model.pkl")
    size = len(dist)
    for a in range(size):
        for b in range(size):
            if a!=b:
                #print([speed[a][b], slope[a][b], temp[a][b], road[a][b], humidity[a][b], wind[a][b], weather[a][b], traffic[a][b]])
                prediction = model.predict([[speed[a][b], slope[a][b], temp[a][b], road[a][b], humidity[a][b], wind[a][b], weather[a][b], traffic[a][b]]])
                #print(a,b,prediction[0])
                dist[a][b]*=prediction
    return dist

#turns distance matrix into time matrix
def time_prdictor(dist,speed):
    size = len(dist)
    time = deepcopy(dist)
    for a in range(size):
        for b in range(size):
            if a!=b:
                time[a][b] = (dist[a][b]/speed[a][b])/60    #minutes
    return time

def generate_map(nodes_num,chargers_num,type="random",size=5,city="Lille, France", parameters = "random"):
    if parameters == "random":
        speed, slope, temp, road, humidity, wind, weather, traffic = input_generator(nodes_num)
    if type == "random":
        pts, dist, chargers = carte(nodes_num,size,chargers_num)
        time = time_prdictor(dist,speed)
        batt_usage = battery_predictor(dist, speed, slope, temp, road, humidity, wind, weather, traffic)
        return pts, batt_usage, time, chargers
    if type == "real":
        pts, dist, chargers = carte_osm(nodes_num,load_map(city),chargers_num)
        time = time_prdictor(dist,speed)
        batt_usage = battery_predictor(dist, speed, slope, temp, road, humidity, wind, weather, traffic)
        return pts, batt_usage, time, chargers



if __name__=="__main__":
    #print(carte(5,10,chargers=2,plot = True))
    
    """speed, slope, temp, road, humidity, wind, weather, traffic = input_generator(4)
    dist = np.ones((4,4))
    print(battery_predictor(dist, speed, slope, temp, road, humidity, wind, weather, traffic))"""

    """pts,m = (carte(10,20,plot = True))
    draw([a for a in range(10)],pts)
    plt.show()"""

    #print(generate_map(9,2,type="real")[0])

