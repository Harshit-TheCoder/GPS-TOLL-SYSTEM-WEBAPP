import numpy as np
import pandas as pd
import ast
from vehicle_average_speed import vehicleAvgSpeedDf
data = pd.read_csv('GPS_based_Toll_System_Data.csv',index_col=False)
d = pd.read_csv('GPS_based_Toll_System_User_Transaction_Data.csv',index_col=False)

# print(data)
# expected_columns = ['Vehicle Number','Category', 'Owner Name','User Id','Owner Account Number',  'Average Speed of vehicle','Toll price per km', 'Amount Charged', 'Account Balance', 'Entry Time Stamp', 'Entry Gate Coordinates', 'Exit Time Stamp', 'Exit Gate Coordinates',  'Distance Travelled']
# print(data.columns)
# # If the columns are not as expected, rename them
# if list(data.columns) != expected_columns:
#     data.columns = expected_columns

# print(data.head())
# loggedInUser_vnum = data.loc[data['Owner Name'] == "Raashi Khanna", 'Vehicle Number']
# print(loggedInUser_vnum.values[0])
# print(d.loc[d['Owner Name'] == "Raashi Khanna", 'Exit Gate Coordinates'].values[0])
# lt = d.loc[d['Owner Name'] == "Raashi Khanna", 'Exit Gate Coordinates'].values[0]
# print(type(lt))
# lt = ast.literal_eval(lt)
# print(type(lt))
# lt.append("3")
# print(lt)
# d.loc[d['Owner Name'] == "Raashi Khanna", 'Exit Gate Coordinates'] = str(lt)
# print(d.loc[d['Owner Name'] == "Raashi Khanna", 'Exit Gate Coordinates'].values[0])

# def updateTransactionData(name, col_name, value):
#     print(f"Before:{d.loc[d['Owner Name'] == name, col_name].values[0]}")
#     lt = d.loc[d['Owner Name'] == name, col_name].values[0]
#     lt = ast.literal_eval(lt)
#     lt.append(value)
#     d.loc[d['Owner Name'] == name, col_name] = str(lt)
#     print(f"After:{d.loc[d['Owner Name'] == name, col_name].values[0]}")

# updateTransactionData("Raashi Khanna", 'Entry Time Stamp', '12-05-2024 21:00:00')
# updateTransactionData("Raashi Khanna", 'Entry Gate Coordinates', '(45.2345671, 67.89567433)')
# updateTransactionData("Raashi Khanna", 'Exit Time Stamp', '12-05-2024 21:20:00')
# updateTransactionData("Raashi Khanna", 'Exit Gate Coordinates', '(45.78921, 69.876543)')
# updateTransactionData("Raashi Khanna", 'Distance Travelled', '6.29')
# user = data.loc[data['Owner Name'] == 'Raashi Khanna']
# print(user)
print(vehicleAvgSpeedDf)
dicti = vehicleAvgSpeedDf['Sedan']
print(dicti)
print(dicti['Congestion'])
print(d)
receipts = d.loc[d['Owner Name'] == 'Raashi Khanna', 'Receipt'].values[0]
print(receipts)
print(type(receipts))
lt = ast.literal_eval(receipts)
print(lt[1])