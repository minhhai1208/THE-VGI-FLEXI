from pulp import *
import pandas as pd

def create_transportation_model(starts, destinations, demands_from_begin):
    # Constants
    fixed_seat = 10
    bus_available = 1000
    
    
    # Create demand matrix from the flat list
    demands_flat = demands_from_begin
    demands = {}
    index = 0
    for i in starts:
        for j in destinations:
            demands[(i,j)] = demands_flat[index]
            index += 1
    
    # Create the model
    model = LpProblem("Transportation_Problem", LpMinimize)
    
    # Decision variables
    units = LpVariable.dicts("units",
                           ((i, j) for i in starts for j in destinations),
                           lowBound=0,
                           cat='Integer')
    
    # Objective function: minimize total number of buses
    model += lpSum(units[i,j] for i in starts for j in destinations)
    
    # Constraints
    
    # Capacity constraint for each route
    for i in starts:
        for j in destinations:
            model += fixed_seat * units[i,j] >= demands[i,j]
    
    # Total number of buses constraint
    model += lpSum(units[i,j] for i in starts for j in destinations) <= bus_available
    
    return model, units, demands, destinations

def solve_and_print_results(starts, destinations, demands):
    model, units, demands, destinations = create_transportation_model(starts, destinations, demands)
    
    # Solve the model
    model.solve()
    
    # Print results
    
    bus_needed = value(model.objective)
    keys = ['Start', 'Destination', 'Busses_nedded', 'Demand']

    # Create a dictionary with empty values (None)
    routes = dict.fromkeys(keys, None)
    start_points = []
    destinations_points = []
    values  =[]
    demandss = []
    for i in starts:
        for j in destinations:
            val = value(units[i,j])
            if val > 0:  # Only print non-zero allocations
                start_points.append(i)
                destinations_points.append(j)
                values.append(val)
                demandss.append(demands[i,j])
                print("hello")
    
    print(starts)
    routes["Start"] = start_points
    routes["Destination"] = destinations_points
    routes["Busses_nedded"] = values
    routes["Demand"] = demandss
    routes = pd.DataFrame(routes)
    return bus_needed, routes
