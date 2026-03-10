import map
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

#___________parameters
n = 5       #num of points
nv = 2      #num of vehicles

#_______map
size = 10
p,m = map.carte(n,size)#, map = True)

manager = pywrapcp.RoutingIndexManager(n, nv, 0)
routing = pywrapcp.RoutingModel(manager)

def distance (a,b):
    a = manager.IndexToNode(a)
    b = manager.IndexToNode(b)
    return m[a,b]

callback_index = routing.RegisterUnaryTransitCallback(distance)

routing.AddDimensionWithVehicleCapacity(
    callback_index,
    0,
    [100],
    True,
    "Capacity"
    )

search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
)

solution = routing.SolveWithParameters(search_parameters)

if solution:
    for vehicle_id in range(n):
        index = routing.Start(vehicle_id)
        route_distance = 0

        route = []
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route.append(node)
            
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id
            )
        
        route.append(manager.IndexToNode(index))

        print(f"Route for vehicle {vehicle_id}: {route}")
        print(f"Distance: {route_distance}\n")
        
        total_distance += route_distance

    print("Total distance:", total_distance)
