import numpy as np
import pandas as pd
data = np.array([
    ['WB 001 1234', 'Sedan','Raashi Khanna','RK1234S', '2342567899126969',60.0, 8.50, 50000.0,0.0,"","","","",0.0 ],
    ['WB 002 1235', 'HatchBack','Ramesh Kale','RK1235H', '2342567099126969',60.0, 7.50, 50000.0, 0.0,"","","","",0.0 ],
    ['WB 003 1236', 'Truck','Karan Dogra','KD1236T','2342567899123969',40.0, 35.0, 50000.0, 0.0,"","","","",0.0 ],
    ['WB 004 1237', 'Bus','Champak Singh','CS1237B', '2342564899126969',40.0, 30.0, 50000.0 , 0.0,"","","","",0.0],
    ['WB 005 1238', 'SUV','Ram Sharma','RS1238S', '2342569899126969',55.0, 10.0, 50000.0, 0.0,"","","","",0.0 ],
    ['WB 006 1239', 'Sport','Shyam Verma','SV1239S', '2342567800126969',75.0, 9.0, 50000.0, 0.0,"","","","",0.0 ],
    ['WB 007 1240', 'Micro','Prem Kuute','PK1240M', '2342567012126969',60.0, 7.0, 50000.0 , 0.0,"","","","",0.0],
    ['WB 008 1241', 'Coupe','Champu Singh','CS1241C', '2342567333326969',65.0, 8.0, 50000.0 , 0.0,"","","","",0.0],
    ['WB 009 1242', 'Crossover','Narendra Modi','NM1242C', '2342560018126969',70.0, 9.5, 50000.0, 0.0,"","","","",0.0 ],
    ['WB 010 1243', 'Van','Rahul Gandhi','RG1243V', '2342523899126969',50.0, 6.0, 50000.0 , 0.0,"","","","",0.0],
])
df = pd.DataFrame(data, columns=['Vehicle Number', 'Category','Owner Name','User Id', 'Owner Account Number','Average Speed of vehicle', 'Toll price per km','Account Balance','Amount Charged','Entry Time Stamp', 'Entry Gate Coordinates'
                                ,'Exit Time Stamp', 'Exit Gate Coordinates', 'Distance Travelled'])
df = df.astype({
    'Amount Charged':float,
    'Entry Time Stamp':str,
    'Entry Gate Coordinates':str,
    'Exit Time Stamp':str,
    'Exit Gate Coordinates':str,
    'Distance Travelled':float,
})
print(df)
df.to_csv('GPS_based_Toll_System_Data.csv', index=False)