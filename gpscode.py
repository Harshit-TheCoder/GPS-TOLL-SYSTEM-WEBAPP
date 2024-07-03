# IMPORTING LIBRARIES
import io
import os
import googlemaps
from googlemaps.convert import decode_polyline
import simpy
import geopy.distance
import folium
from folium import Marker
from IPython.display import display
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import requests
import time as t
import math
import ast
import random
from dotenv import load_dotenv
from vehicle_average_speed import vehicleAvgSpeedDf

load_dotenv()

API_KEY = os.getenv('API_KEY')
gmaps = googlemaps.Client(key=API_KEY)
central_point=(28.39576241152042, 76.98194106683556)
radius_km = 0.5
vehicle_data=pd.read_csv('GPS_based_Toll_System_Data.csv',index_col=False)
vehicle_transaction_data=pd.read_csv('GPS_based_Toll_System_User_Transaction_Data.csv',index_col=False)
high_speed_penalty = 0.0

class Vehicle:
    def __init__(self,env,vehicle_id,path,speed,map_obj):
        self.env=env
        self.vehicle_id = vehicle_id
        self.path = path
        self.speed = speed
        self.position_index=0
        self.distance_traveled=0
        self.map_obj = map_obj
        self.marker = Marker(location=self.path[0], popup=f'Vehicle {self.vehicle_id}')
        self.marker.add_to(self.map_obj)
        self.action = env.process(self.run())
        self.entry_point = path[0]
        self.entry_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.exit_point=path[-1]
        self.exit_date_time=""
        self.previous_position = None  # Store previous position
        self.stationary_duration = 5  # Specify duration for stationary (in minutes)
        self.stationary_time = 0  

    def distance(self, point1, point2):
        return geopy.distance.geodesic(point1, point2).km
    
    def updateTransactionData(self, name, col_name, value):
        print(f"Before:{vehicle_transaction_data.loc[vehicle_transaction_data['Owner Name'] == name, col_name].values[0]}")
        lt = vehicle_transaction_data.loc[vehicle_transaction_data['Owner Name'] == name, col_name].values[0]
        lt = ast.literal_eval(lt)
        lt.append(value)
        vehicle_transaction_data.loc[vehicle_transaction_data['Owner Name'] == name, col_name] = str(lt)
        print(f"After:{vehicle_transaction_data.loc[vehicle_transaction_data['Owner Name'] == name, col_name].values[0]}")

    def run(self):
        global vehicle_data
        global vehicle_transaction_data
        global high_speed_penalty

        vehicle_data = pd.read_csv('GPS_based_Toll_System_Data.csv',index_col=False)
        vehicle_transaction_data = pd.read_csv('GPS_based_Toll_System_User_Transaction_Data.csv',index_col=False)

        while self.position_index < len(self.path)-1:
            start_point = self.path[self.position_index]
            end_point = self.path[self.position_index+1]
            segment_distance = self.distance(start_point, end_point)
            travel_time = segment_distance/(self.speed/60)
            yield self.env.timeout(travel_time)
            self.distance_traveled += segment_distance
            self.position_index += 1
            self.marker.location = end_point
            # self.capture_map(f'vehicle_{self.vehicle_id}_pos_{self.position_index}.png')
            print(f"Time {self.env.now:.2f}: Vehicle {self.vehicle_id} moved to position {self.position_index}.")
            if self.previous_position == self.marker.location:
                self.stationary_time += travel_time
            else:
                # If the vehicle moved, reset stationary time
                self.stationary_time = 0

            # Check if the vehicle has been stationary for the specified duration
            if self.stationary_time >= self.stationary_duration:
                print(f"Vehicle {self.vehicle_id} is stationary for {self.stationary_duration} minutes.")

            # Update previous position
            self.previous_position = self.marker.location


            display(self.map_obj) # Display updated map
            filename = f"static/Output_HTML_files/vehicle_{self.vehicle_id}_position_{self.position_index}.html"
            self.map_obj.save(filename)

            row = vehicle_data.loc[vehicle_data['Vehicle Number'] == self.vehicle_id]
            # print(row)
            index = row.index[0]
            speed = vehicle_data.loc[index, 'Average Speed of vehicle']
            if speed > 50 and speed <= 55:
                t.sleep(3)
            elif speed > 55 and speed <= 60:
                t.sleep(2.5)
            elif speed > 60 and speed <= 65:
                t.sleep(2)
            elif speed > 65 and speed <= 70:
                t.sleep(1.5)
            else:
                t.sleep(1)
        
        self.exit_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.exit_point = self.path[-1]

        # Update the DataFrame using .loc
        vehicle_data.loc[vehicle_data['Vehicle Number'] == self.vehicle_id, 'Entry Time Stamp'] = self.entry_date_time
        vehicle_data.loc[vehicle_data['Vehicle Number'] == self.vehicle_id, 'Entry Gate Coordinates'] = str(self.entry_point)
        vehicle_data.loc[vehicle_data['Vehicle Number'] == self.vehicle_id, 'Distance Travelled'] = round(self.distance_traveled,2)
        vehicle_data.loc[vehicle_data['Vehicle Number'] == self.vehicle_id, 'Exit Time Stamp'] = self.exit_date_time
        vehicle_data.loc[vehicle_data['Vehicle Number'] == self.vehicle_id, 'Exit Gate Coordinates'] = str(self.exit_point)

        user = vehicle_data.loc[vehicle_data['Vehicle Number'] == self.vehicle_id, 'Owner Name'].values[0]

        self.updateTransactionData(user, 'Entry Time Stamp', str(self.entry_date_time) )
        self.updateTransactionData(user, 'Entry Gate Coordinates', str(self.entry_point) )
        self.updateTransactionData(user, 'Exit Time Stamp', str(self.exit_date_time) )
        self.updateTransactionData(user, 'Exit Gate Coordinates', str(self.exit_point))
        self.updateTransactionData(user, 'Distance Travelled', round(self.distance_traveled,2) )
        
        toll_rate = row['Toll price per km'].values[0]
        current_datetime = datetime.now()
        time = current_datetime.strftime("%H:%M:%S")
        category = row['Category'].values[0]
        if (time > "08:00:00" and time < "10:00:00") or (time > "18:00:00" and time < "21:00:00"):
            if category == 'Truck' or category == 'Bus':
                toll_rate += 10.0
            elif category == 'SUV' or category == 'Crossover' or category == 'Sport':
                toll_rate += 8.0
            elif category == 'Sedan' or category == 'Coupe':
                toll_rate += 7.0
            elif category == 'Micro' or category == 'HatchBack':
                toll_rate += 5.0
            elif category == 'Van':
                toll_rate += 3.0
        dicti = vehicleAvgSpeedDf[category]

        if (time > "08:00:00" and time < "10:00:00") or (time > "18:00:00" and time < "21:00:00"):
            if self.speed > dicti['Congestion']:
                if category == 'Truck' or category == 'Bus':
                    high_speed_penalty = 70.0
                elif category == 'SUV' or category == 'Crossover' or category == 'Sport':
                    high_speed_penalty = 60.0
                elif category == 'Sedan' or category == 'Coupe':
                    high_speed_penalty = 55.0
                elif category == 'Micro' or category == 'HatchBack':
                    high_speed_penalty = 50.0
                elif category == 'Van':
                    high_speed_penalty = 40.0
                else:
                    high_speed_penalty = 40.0
        else:
            if self.speed > dicti['Normal']:
                if category == 'Truck' or category == 'Bus':
                    high_speed_penalty = 60.0
                elif category == 'SUV' or category == 'Crossover' or category == 'Sport':
                    high_speed_penalty = 50.0
                elif category == 'Sedan' or category == 'Coupe':
                    high_speed_penalty = 45.0
                elif category == 'Micro' or category == 'HatchBack':
                    high_speed_penalty = 40.0
                elif category == 'Van':
                    high_speed_penalty = 30.0
                else:
                    high_speed_penalty = 30.0
            # vehicle_data.loc[vehicle_data['Vehicle Number'] == self.vehicle_id, 'Amount Charged'] += high_speed_penalty

        generated_toll = self.distance_traveled * toll_rate
        print(f"Initial Account Balance:{row['Account Balance'].values[0]}")
        print(f"New Account Balance:{round((row['Account Balance'].values[0] - generated_toll),2)}")
        vehicle_data.loc[vehicle_data['Vehicle Number'] == self.vehicle_id, 'Amount Charged'] = (round(generated_toll,2) + high_speed_penalty)
        vehicle_data.loc[vehicle_data['Vehicle Number'] == self.vehicle_id, 'Account Balance'] = round((row['Account Balance'].values[0] - generated_toll),2)
        self.updateTransactionData(user, 'Amount Charged', round(generated_toll,2) )
        self.updateTransactionData(user, 'Account Balance', round((row['Account Balance'].values[0] - generated_toll),2) )
        self.updateTransactionData(user, 'Toll price per km', toll_rate )

        vehicle_data.to_csv('GPS_based_Toll_System_Data.csv', index=False)
        vehicle_transaction_data.to_csv('GPS_based_Toll_System_User_Transaction_Data.csv', index=False)

        # vehicle_data = pd.read_csv('GPS_based_Toll_System_Data.csv',index_col=False)
        # vehicle_transaction_data = pd.read_csv('GPS_based_Toll_System_User_Transaction_Data.csv',index_col=False)

        print(f"Vehicle {self.vehicle_id} reached its destination. Total distance traveled: {self.distance_traveled:.2f} km.\n\n\n\n")

def generate_receipt(env, vehicle_number, new_path, loggedInUser_avgspeed, map_obj):
        global vehicle_transaction_data
        global high_speed_penalty 

        vehicle_transaction_data = pd.read_csv('GPS_based_Toll_System_User_Transaction_Data.csv',index_col=False)
        v = Vehicle(env, vehicle_number, new_path, loggedInUser_avgspeed, map_obj)
        row = vehicle_data[vehicle_data['Vehicle Number'] == vehicle_number]
        user = row['Owner Name'].values[0]

        if row.empty:
            return "Item not found in the dataset."
        index = row.index[0]
        current_datetime = datetime.now()
        date_only = current_datetime.strftime("%Y-%m-%d")
        time_only = current_datetime.strftime("%H:%M:%S")
        time = current_datetime.strftime("%H:%M:%S")
        # receipt = f"********TOLL RECEIPT********\n\n"
        # receipt += f"Date:{date_only}\n"
        # receipt += f"Time:{time_only}\n"
        # receipt += f"Vehicle Number: {vehicle_number}\n"
        # receipt += f"Vehicle Owner Name: {row['Owner Name'].values[0]}\n"
        # receipt += f"Vehicle Category: {row['Category'].values[0]}\n"
        # receipt += f"Distance Travelled: {row['Distance Travelled'].values[0]} km\n"
        # receipt += f"Average Speed:{row["Average Speed of vehicle"].values[0]}\n"
        # receipt += f"Entry Point Coordinates:{row['Entry Gate Coordinates'].values[0]}\n"
        # receipt += f"Entry Date and Time:{row['Entry Time Stamp'].values[0]}\n"
        # receipt += f"Exit Point Coordinates:{row['Exit Gate Coordinates'].values[0]}\n"
        # receipt += f"Exit Date and Time:{row['Exit Time Stamp'].values[0]}\n"
        # category = row['Category'].values[0]
        # toll_rate = row['Toll price per km'].values[0]
        # if (time > "08:00:00" and time < "10:00:00") or (time > "18:00:00" and time < "21:00:00"):
        #     if category == 'Truck' or category == 'Bus':
        #         toll_rate += 10.0
        #     elif category == 'SUV' or category == 'Crossover' or category == 'Sport':
        #         toll_rate += 8.0
        #     elif category == 'Sedan' or category == 'Coupe':
        #         toll_rate += 7.0
        #     elif category == 'Micro' or category == 'HatchBack':
        #         toll_rate += 5.0
        #     elif category == 'Van':
        #         toll_rate += 3.0
        #     receipt += f"Toll Price(Traffic Congestion) (per km): {toll_rate} rupees per km\n"
        # else:
        #     receipt += f"Toll Price (per km): {toll_rate} rupees per km\n"
        # receipt += f"High Speed Penalty: {high_speed_penalty} rupees \n"
        # receipt += f"Amount Charged: {row['Amount Charged'].values[0]} rupees\n"
        # receipt += f"Current Balance: {row['Account Balance'].values[0]} rupees\n\n"
        # receipt += f"********Thank You,Visit Again!!********\n"

        receipt_dict = {
            'Date': date_only,
            'Time': time_only,
            'Vehicle Number': vehicle_number,
            'Vehicle Owner Name': row['Owner Name'].values[0],
            'Vehicle Category': row['Category'].values[0],
            'Distance Travelled': f"{row['Distance Travelled'].values[0]} km",
            'Average Speed': row["Average Speed of vehicle"].values[0],
            'Entry Point Coordinates': row['Entry Gate Coordinates'].values[0],
            'Entry Date and Time': row['Entry Time Stamp'].values[0],
            'Exit Point Coordinates': row['Exit Gate Coordinates'].values[0],
            'Exit Date and Time': row['Exit Time Stamp'].values[0],
        }

        category = row['Category'].values[0]
        toll_rate = row['Toll price per km'].values[0]

        if (time > "08:00:00" and time < "10:00:00") or (time > "18:00:00" and time < "21:00:00"):
            if category == 'Truck' or category == 'Bus':
                toll_rate += 10.0
            elif category == 'SUV' or category == 'Crossover' or category == 'Sport':
                toll_rate += 8.0
            elif category == 'Sedan' or category == 'Coupe':
                toll_rate += 7.0
            elif category == 'Micro' or category == 'HatchBack':
                toll_rate += 5.0
            elif category == 'Van':
                toll_rate += 3.0
            receipt_dict['Toll Price(Traffic Congestion)'] = f"{toll_rate} rupees per km"
        else:
            receipt_dict['Toll Price'] = f"{toll_rate} rupees per km"

        receipt_dict['High Speed Penalty'] = f"{high_speed_penalty} rupees"
        receipt_dict['Amount Charged'] = f"{row['Amount Charged'].values[0]} rupees"
        receipt_dict['Current Balance'] = f"{row['Account Balance'].values[0]} rupees"

        # Optionally add a 'Thank You' message
        

        # print(receipt_dict)


        v.updateTransactionData(user, 'Receipt', receipt_dict )
        vehicle_transaction_data.to_csv('GPS_based_Toll_System_User_Transaction_Data.csv', index=False)
        return receipt_dict

def get_static_map_url(bounding_box,zoom,size=(640,640),maptype='roadmap',paths=[],markers=[]):
    base_url="https://maps.googleapis.com/maps/api/staticmap?"
    southwest, northeast = bounding_box
    # Calculate the center of the bounding box
    center_lat = (southwest[0] + northeast[0]) / 2
    center_lon = (southwest[1] + northeast[1]) / 2
    center = (center_lat, center_lon)
    # Define the path for the bounding box (rectangle)
    path_coords = [
        southwest,                         # SW corner
        (southwest[0], northeast[1]),      # NW corner
        northeast,                         # NE corner
        (northeast[0], southwest[1]),      # SE corner
        southwest                          # Back to SW corner to close the box
    ]
    params={
        'center':f"{center[0]},{center[1]}",
        'zoom':zoom,
        'size':f"{size[0]}x{size[1]}",
        'maptype':maptype,
        'key':API_KEY
    }
    if markers:
        markers_str = '|'.join([f"{lat},{lon}" for lat,lon in markers])
        params['markers'] = markers_str
    if paths:
        path_str = 'color:0x0000ff|weight:5|'+'|'.join([f"{lat},{lon}" for lat,lon in paths])
        params['path'] = path_str
    return base_url+'&'.join(f"{key}={value}" for key,value in params.items())

def startSimulation(loggedInUser, user_data):
    global vehicle_data
    markers=[(28.39576241152042, 76.98195179567065),(28.374618304249985, 76.95245083216956),(28.382600603605226, 76.96910623465669),(28.35707241618491, 76.93860342434418)]
    start_point = markers[3] #Manesar dhaba
    end_point = markers[0] #kherki dhula toll plaza
    # 28.374618304249985, 76.95245083216956 #Mcdonalds India Gurugram
    # 28.382600603605226, 76.96910623465669 #Last entry point

    directions_result = gmaps.directions(start_point, end_point, mode="driving")
    route = directions_result[0]['overview_polyline']['points']
    path_coordinates = decode_polyline(route)
    # print("Path coordinates:", path_coordinates)

    bounding_box=((28.348413936050553, 76.91040008806508),(28.40758480090512, 77.01143068746502))
    map_url = get_static_map_url(bounding_box, 14.2,paths=path_coordinates, markers=markers)
    print(map_url)
    response = requests.get(map_url)
    print(response.status_code)
    img = Image.open(BytesIO(response.content))

    #SAVE THE IMAGE OF THE MAP
    # img_path = 'static/images/route_map_image.png'
    # img.save(img_path)

    # DISPLAY MAP USING MATPLOTLIB
    # print(f"Image format:{img.format}")
    # plt.figure(figsize=(10,10))
    # plt.imshow(img)
    # plt.axis('off')
    # plt.show()

    #BOUNDING BOX COORDINATES
    # 28.39758480090512, 77.00143068746502 #top right
    # 28.358413936050553, 77.00143068746502 #top left
    # 28.358413936050553, 76.93040008806508 #bottom left
    # 28.39758480090512, 76.93040008806508 #bottom right

    print(vehicle_data)

    path_coordinates_tuple = [tuple(d.values()) for d in path_coordinates]
    print(path_coordinates_tuple)

    path = [(28.357090000000003, 76.93855), (28.358050000000002, 76.93894), (28.359050000000003, 76.93937000000001), (28.35986, 76.93968000000001), (28.361570000000004, 76.94035000000001), (28.363840000000003, 76.94130000000001), (28.36576, 76.94214000000001), (28.36784, 76.94302), (28.36915, 76.94353000000001), (28.369470000000003, 76.94368), (28.369930000000004, 76.94393000000001), (28.370310000000003, 76.94421000000001), (28.370590000000004, 76.94449), (28.370800000000003, 76.94474000000001), (28.37104, 76.94510000000001), (28.371240000000004, 76.94546000000001), (28.371480000000002, 76.94602), (28.37207, 76.94741), (28.374000000000002, 76.95125), (28.375120000000003, 76.9535), (28.375700000000002, 76.95462), (28.37733, 76.95790000000001), (28.378320000000002, 76.9598), (28.379150000000003, 76.96142), (28.381210000000003, 76.96549), (28.382540000000002, 76.96804), (28.383070000000004, 76.96915000000001), (28.38331, 76.96964000000001), (28.383490000000002, 76.96992), (28.38379, 76.97032), (28.38406, 76.97064), (28.384780000000003, 76.97134000000001), (28.386390000000002, 76.97290000000001), (28.387980000000002, 76.97445), (28.3896, 76.97606), (28.392650000000003, 76.97901), (28.392920000000004, 76.97923), (28.393050000000002, 76.97934000000001), (28.393760000000004, 76.97996), (28.394450000000003, 76.98053), (28.394930000000002, 76.9809), (28.39579, 76.98176000000001), (28.395860000000003, 76.98184)]
    
    southwest, northeast = bounding_box

        # Calculate the center of the bounding box
    center_lat = (southwest[0] + northeast[0]) / 2
    center_lon = (southwest[1] + northeast[1]) / 2
    center = (center_lat, center_lon)
    map_obj = folium.Map(location=center, zoom_start = 14.2)
    folium.Marker(location=path[0], popup='Start', icon=folium.Icon(color='green')).add_to(map_obj)
    folium.Marker(location=(28.374618304249985, 76.95245083216956), popup='Start', icon=folium.Icon(color='orange')).add_to(map_obj)
    folium.Marker(location=(28.382600603605226, 76.96910623465669), popup='Start', icon=folium.Icon(color='orange')).add_to(map_obj)
    folium.Marker(location=path[-1], popup='End', icon=folium.Icon(color='red')).add_to(map_obj)

    env = simpy.Environment()
    vehicle_data = user_data.copy()
    loggedInUser_vnum = vehicle_data.loc[vehicle_data['Owner Name'] == loggedInUser, 'Vehicle Number'].values[0]
    loggedInUser_avgspeed = vehicle_data.loc[vehicle_data['Owner Name'] == loggedInUser, 'Average Speed of vehicle'].values[0]
    starting_point_list=[(28.374000000000002, 76.95125),(28.382540000000002, 76.96804),(28.357090000000003, 76.93855)]
    coord = random.choice(starting_point_list)
    idx = path.index(coord)
    new_path = path[idx:]
    vehicles = [
        Vehicle(env, loggedInUser_vnum, new_path, int(loggedInUser_avgspeed), map_obj),
    ]
    env.run()
    receipt = generate_receipt(env,loggedInUser_vnum, new_path, int(loggedInUser_avgspeed), map_obj)
    print(receipt)
    return [vehicle_transaction_data, vehicle_data]
