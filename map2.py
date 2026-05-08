import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

if not hasattr(np, "float_"):
    np.float_ = np.float64

import osmnx as ox
import networkx as nx



# RANDOM MAP
def carte(n, size, demand=0, plot=False):
    pts = points(n, abs(size))
    m = distanceMatrix(pts)

    # Add demand
    if demand > 0:
        for a in pts:
            a.append(random.randrange(0, demand))
    else:
        for a in pts:
            a.append(0)

    # Plot
    if plot:
        x = [point[0] for point in pts]
        y = [point[1] for point in pts]
        plt.scatter(x, y)
        plt.scatter(pts[0][0], pts[0][1], color='red')
        ax = plt.gca()
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_locator(MultipleLocator(1))
        plt.grid(True)
        plt.title("Synthetic Map")
        plt.show()

    return pts, m

def points(n, d):
    r = []
    for _ in range(n):
        r.append([random.randint(-d, d), random.randint(-d, d)])
    return r

def distanceMatrix(p):
    n = len(p)
    m = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            m[i][j] = abs(p[i][0] - p[j][0]) + abs(p[i][1] - p[j][1])

    return m


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


def carte_osm(n, G, demand=0, plot=False):
    """
    OSM-based map generator
    """

    pts, selected_nodes = points_osm(G, n)
    m = distanceMatrix_osm(G, selected_nodes)

    # Add demand
    if demand > 0:
        for p in pts:
            p.append(random.randrange(0, demand))
    else:
        for p in pts:
            p.append(0)

    # Plot
    if plot:
        x = [p[0] for p in pts]
        y = [p[1] for p in pts]

        plt.scatter(x, y)
        plt.scatter(pts[0][0], pts[0][1], color='red')  # depot
        plt.title("OSM Map (Real World)")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.show()

    return pts, m


# TESTING
if __name__ == "__main__":

    print("---- Synthetic Map ----")
    pts, m = carte(10, 20, plot=True)
    print(pts)
    print(m)

    print("\n---- OSM Map ----")
    G = load_map("Lille, France")
    pts_osm, m_osm = carte_osm(10, G, plot=True)
    print(pts_osm)
    print(m_osm)