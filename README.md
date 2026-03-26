# EVRP
S8 EVRP Project

# 📄 SECTION TO ADD TO YOUR REPORT

## EV Routing Model Development (Python Implementation)

### Overview

During this phase of the project, we focused on developing a **Vehicle Routing Problem (VRP)** model as a foundation for the **Electric Vehicle Routing Problem (EVRP)**. The objective was to design a routing system that minimizes energy consumption while considering constraints such as battery capacity and charging stations.

---

### Dataset Utilization

We used the **EV Energy Consumption Dataset from Kaggle** as the primary data source. 

From the dataset, the following attributes were extracted:

* Distance travelled (km)
* Energy consumption (kWh)

For initial testing, a subset of **15 nodes** was selected to construct the routing problem.

---

### Problem Formulation

The routing problem was modeled as a **graph-based optimization problem**, where:

* Nodes represent locations (including depot and charging stations)
* Edges represent travel paths between locations
* Cost function represents **energy consumption**

The objective is:

[
\text{Minimize total energy cost}
]

subject to:

* Each node is visited exactly once
* Vehicles start and end at the depot
* Battery capacity constraints are respected

---

### Distance Matrix Construction

A distance matrix was generated using the dataset:

[
D_{ij} = |distance_i - distance_j|
]

This matrix represents the cost of traveling between any two nodes and is later used to compute energy consumption.

---

### Energy-Based Cost Function

Instead of minimizing distance, we defined an **energy-based cost function**:

[
Energy = Distance \times Consumption_Factor
]

In the current implementation:

* A simplified constant factor was used
* This approximates real EV energy usage

---

### Model Implementation

The routing model was implemented using **Google OR-Tools**, which provides efficient solvers for combinatorial optimization problems.

Key components:

* RoutingIndexManager → maps nodes
* RoutingModel → defines the optimization problem
* Callback function → computes energy cost
* Solver → finds optimal routes

---

### EV-Specific Constraints

To extend the classical VRP into EVRP, we incorporated:

#### 1. Battery Constraint

Each vehicle is assigned a maximum battery capacity:

* Battery capacity = **50 kWh**

This ensures that routes remain feasible for electric vehicles.

---

#### 2. Charging Stations

Specific nodes were designated as charging stations:

* Example nodes: **3, 7, 12**

These nodes simulate locations where vehicles can recharge.

---

### Results

The solver successfully generated an optimized routing solution.

Example output:

* Only one vehicle was used to minimize total energy cost
* Other vehicles remained unused as they were not required

This behavior indicates that the solver prioritizes **global optimality over vehicle utilization**, which is consistent with VRP formulations.

---

### Observations

* The current model successfully integrates:

  * energy-aware routing
  * battery constraints
  * multi-vehicle routing

* However, the energy model is still simplified and does not yet include:

  * traffic conditions
  * road slope
  * dynamic energy consumption

---

### Limitations

* Distance matrix is artificially constructed (not based on real coordinates)
* Charging stations are predefined and not optimized
* Battery recharge behavior is not yet dynamically modeled

---

### Future Work

The next steps in the project include:

* Integrating **real geographic coordinates** and map-based routing
* Improving the **energy consumption model** using dataset features
* Implementing **charging decision logic**
* Exploring **AI techniques (Reinforcement Learning)** for adaptive routing
* Visualizing routes using **OpenStreetMap**

---

### Conclusion

This implementation establishes a strong foundation for solving the **Electric Vehicle Routing Problem (EVRP)**. By extending classical VRP with energy and battery constraints, we move closer to developing an intelligent routing system suitable for real-world EV applications.

---

# ✅ What You Should Do Now

1. Copy this into your **Report11.docx**
2. Put it under a section like:

   ```
   EV Routing / Python Implementation
   ```
3. Add:

   * your **code (optional appendix)**
   * a **screenshot of your output**
   * (bonus) your **map visualization**
