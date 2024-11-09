import mysql.connector
import pandas as pd
import pymysql


# 

trip_data = pd.read_excel("D:\\FLEXI_trip_data.xls")
bus_stops_data = pd.read_excel("D:\\FLEXI_bus_stops.xls")

trip_data = trip_data.values.tolist()
print(trip_data)
bus_stops_data = bus_stops_data.values.tolist()
# Convert Timestamp to string in correct format for MySQL
for row in trip_data:
    row[6] = row[6].strftime('%Y-%m-%d %H:%M:%S')  # Actual_Pickup_Time
    row[7] = row[7].strftime('%Y-%m-%d %H:%M:%S')  # Actual_Dropoff_Time
    
trip_data =  [entry for entry in trip_data if entry[4] <= 69 and entry[5] <= 69]  
print(trip_data)
# Connect database
db = pymysql.connect(
    host = "localhost",
    port = 3306,
    user = "root",
    password="Yandere128@"
)
cursor = db.cursor()
query = "Use vgiproject;"
cursor.execute(query)

insert_query1 = """
INSERT INTO bus_stops (Bus_stop_id, Name, District, Latitude, Longitude)
VALUES (%s, %s, %s, %s, %s)
"""
insert_query2 = """
INSERT INTO trips (Booking_ID, Status, Passenger_status, 
                Passengers, Pickup_ID, Dropoff_ID, Actual_Pickup_Time,
                Actual_Dropoff_Time)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""
cursor.executemany(insert_query2, trip_data)



# Commit the transaction
db.commit()


# Close the connection
cursor.close()
db.close()
