import numpy as np
import pandas as pd
data = np.array([
    ['Raashi Khanna','RK1234S','raashikhanna123@gmail.com', 'raashiqwerty123' ],
    ['Ramesh Kale','RK1235H','',''  ],
    ['Karan Dogra','KD1236T','','' ],
    ['Champak Singh','CS1237B','','' ],
    ['Ram Sharma','RS1238S','',''  ],
    ['Shyam Verma','SV1239S','','' ],
    ['Prem Kuute','PK1240M','','' ],
    ['Champu Singh','CS1241C','','' ],
    ['Narendra Modi','NM1242C','','' ],
    ['Rahul Gandhi','RG1243V','','' ],
])
df = pd.DataFrame(data, columns=['Owner Name','User Id','Email Id' ,'Password'])
df = df.astype({
    'Email Id':str,
    'Password':str,
})
print(df)
df.to_csv('GPS_based_Toll_System_User_Auth_Data.csv', index=False)