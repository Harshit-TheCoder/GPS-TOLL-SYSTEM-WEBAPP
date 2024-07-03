import numpy as np
import pandas as pd
data = {
    1:{
        'Owner Name': 'Raashi Khanna',
        'User Id': 'RK1234S',
        'Owner Account Number': '2342567899126969',
        'Toll price per km': [0.0,8.5, 12.5],
        'Account Balance': [50000.0, 49946.35, 49867.91],
        'Amount Charged': [0.0,53.65, 132.91],
        'Entry Time Stamp': ['qww','ert','asdfgh'],
        'Entry Gate Coordinates': ['qww','ert','asdfgh'],
        'Exit Time Stamp': ['qww','ert','asdfgh'],
        'Exit Gate Coordinates': ['qww','ert','asdfgh'],
        'Distance Travelled': [0.0,6.29,6.29]
    },
    2:{
        'Owner Name': 'Ramesh Kale',
        'User Id': 'RK1235H',
        'Owner Account Number': '2342567099126969',
        'Toll price per km': [0.0],
        'Account Balance': [50000.0],
        'Amount Charged': [0.0],
        'Entry Time Stamp': [''],
        'Entry Gate Coordinates': [''],
        'Exit Time Stamp': [''],
        'Exit Gate Coordinates': [''],
        'Distance Travelled': [0.0]
    },
    3:{
        'Owner Name': 'Karan Dogra',
        'User Id': 'KD1236T',
        'Owner Account Number': '2342567899123969',
        'Toll price per km': [0.0],
        'Account Balance': [50000.0],
        'Amount Charged': [0.0],
        'Entry Time Stamp': [''],
        'Entry Gate Coordinates': [''],
        'Exit Time Stamp': [''],
        'Exit Gate Coordinates': [''],
        'Distance Travelled': [0.0]
    },
    4:{
        'Owner Name': 'Champak Singh',
        'User Id': 'CS1237B',
        'Owner Account Number': '2342564899126969',
        'Toll price per km': [0.0],
        'Account Balance': [50000.0],
        'Amount Charged': [0.0],
        'Entry Time Stamp': [''],
        'Entry Gate Coordinates': [''],
        'Exit Time Stamp': [''],
        'Exit Gate Coordinates': [''],
        'Distance Travelled': [0.0]
    },
    5:{
        'Owner Name': 'Ram Sharma',
        'User Id': 'RS1238S',
        'Owner Account Number': '2342569899126969',
        'Toll price per km': [0.0],
        'Account Balance': [50000.0],
        'Amount Charged': [0.0],
        'Entry Time Stamp': [''],
        'Entry Gate Coordinates': [''],
        'Exit Time Stamp': [''],
        'Exit Gate Coordinates': [''],
        'Distance Travelled': [0.0]
    },
    6:{
        'Owner Name': 'Shyam Verma',
        'User Id': 'SV1239S',
        'Owner Account Number': '2342567800126969',
        'Toll price per km': [0.0],
        'Account Balance': [50000.0],
        'Amount Charged': [0.0],
        'Entry Time Stamp': [''],
        'Entry Gate Coordinates': [''],
        'Exit Time Stamp': [''],
        'Exit Gate Coordinates': [''],
        'Distance Travelled': [0.0]
    },
    7:{
        'Owner Name': 'Prem Kuute',
        'User Id': 'PK1240M',
        'Owner Account Number': '2342567012126969',
        'Toll price per km': [0.0],
        'Account Balance': [50000.0],
        'Amount Charged': [0.0],
        'Entry Time Stamp': [''],
        'Entry Gate Coordinates': [''],
        'Exit Time Stamp': [''],
        'Exit Gate Coordinates': [''],
        'Distance Travelled': [0.0]
    },
    8:{
        'Owner Name': 'Champu Singh',
        'User Id': 'CS1241C',
        'Owner Account Number': '2342567333326969',
        'Toll price per km': [0.0],
        'Account Balance': [50000.0],
        'Amount Charged': [0.0],
        'Entry Time Stamp': [''],
        'Entry Gate Coordinates': [''],
        'Exit Time Stamp': [''],
        'Exit Gate Coordinates': [''],
        'Distance Travelled': [0.0]
    },
    9:{
        'Owner Name': 'Narendra Modi',
        'User Id': 'NM1242C',
        'Owner Account Number': '2342560018126969',
        'Toll price per km': [0.0],
        'Account Balance': [50000.0],
        'Amount Charged': [0.0],
        'Entry Time Stamp': [''],
        'Entry Gate Coordinates': [''],
        'Exit Time Stamp': [''],
        'Exit Gate Coordinates': [''],
        'Distance Travelled': [0.0]
    },
    10:{
        'Owner Name': 'Rahul Gandhi',
        'User Id': 'RG1243V',
        'Owner Account Number': '2342523899126969',
        'Toll price per km': [0.0],
        'Account Balance': [50000.0],
        'Amount Charged': [0.0],
        'Entry Time Stamp': [''],
        'Entry Gate Coordinates': [''],
        'Exit Time Stamp': [''],
        'Exit Gate Coordinates': [''],
        'Distance Travelled': [0.0]
    }
}
df = pd.DataFrame.from_dict(data, orient='index')

# for col in ['Toll price per km', 'Account Balance', 'Amount Charged', 'Distance Travelled']:
#     df[col] = df[col].apply(lambda x: [float(i) for i in x] if isinstance(x, list) else x)

# Convert columns to desired data types
# df = df.astype({
#     'Owner Name': str,
#     'User Id': str,
#     'Owner Account Number': str,
#     'Entry Time Stamp': str,
#     'Entry Gate Coordinates': str,
#     'Exit Time Stamp': str,
#     'Exit Gate Coordinates': str,
# })
print(df)

user_data = data[1]
print(user_data)
user_data_df = pd.DataFrame(user_data)
print(user_data_df)
df.to_csv('GPS_based_Toll_System_User_Transaction_Data.csv', index=False)

length = len(data)
print(length)

new_data = {
    'Owner Name': 'Sonia Gandhi',
    'User Id': 'RG1243T',
    'Owner Account Number': '2342500009126969',
    'Toll price per km': [0.0],
    'Account Balance': [59000.0],
    'Amount Charged': [0.0],
    'Entry Time Stamp': [''],
    'Entry Gate Coordinates': [''],
    'Exit Time Stamp': [''],
    'Exit Gate Coordinates': [''],
    'Distance Travelled': [0.0]
}

# dataset = pd.read_csv('GPS_based_Toll_System_User_Transaction_Data.csv')
# print(dataset)
# new_data_df = pd.DataFrame.from_dict({len(data) + 1: new_data}, orient='index')
# dataset = pd.concat([dataset, new_data_df], ignore_index=True)
# print(dataset)
# dataset.to_csv('GPS_based_Toll_System_User_Transaction_Data.csv', index=False)
name_of_logged_in_user = 'Raashi Khanna'

# Boolean indexing to retrieve the dictionary corresponding to the logged-in user
user_dict = df[df['Owner Name'] == name_of_logged_in_user].to_dict(orient='records')[0]

print(user_dict)
user_dict_df = pd.DataFrame(user_dict)
print(user_dict_df)