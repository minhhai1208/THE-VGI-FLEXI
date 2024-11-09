import pandas as pd
import numpy as np
from optimzation import solve_and_print_results


bus_stop_data = pd.read_excel("D:\\FLEXI_bus_stops.xls")
trips_data = pd.read_excel("D:\\FLEXI_trip_data.xls")

# replace the columns name with white space to _
trips_data.columns = trips_data.columns.str.replace(' ', '_')
trips_data = trips_data[trips_data["Dropoff_ID"] <= 69]
trips_data = trips_data[trips_data["Pickup_ID"] <= 69]

print(trips_data)

trip_matrix = pd.crosstab(trips_data['Pickup_ID'], trips_data['Dropoff_ID'])

start = trip_matrix.index.to_numpy()
destination = trip_matrix.columns.to_numpy()
bus_stop_data = bus_stop_data.set_index("index").to_dict()
names = bus_stop_data["name"]

vectorized_func = np.vectorize(lambda x: names.get(x))
start = vectorized_func(start)
destination = vectorized_func(destination)
print(start.shape)
print(destination.shape)
print(trip_matrix.to_numpy().shape)
demands = trip_matrix.to_numpy().flatten().tolist()
print(trip_matrix.to_numpy().flatten().shape)
print(demands)

print(solve_and_print_results(start, destination, demands))