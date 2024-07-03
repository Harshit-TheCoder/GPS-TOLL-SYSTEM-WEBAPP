from flask import Flask, abort, render_template, redirect, request, url_for, jsonify, send_file
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import ast
from gpscode import startSimulation
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
user_data = pd.read_csv('GPS_based_Toll_System_Data.csv')
user_auth_data = pd.read_csv('GPS_based_Toll_System_User_Auth_Data.csv')
user_transaction_data = pd.read_csv('GPS_based_Toll_System_User_Transaction_Data.csv')
print(user_auth_data)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
class User(UserMixin):
    def __init__(self, id, username, password, user_id, email_id):
        self.id = id
        self.username = username
        self.password = password
        self.user_id = user_id
        self.email_id = email_id

    def get_id(self):
        return self.id


users = {}
for index, row in user_auth_data.iterrows():
    users[row['Owner Name']] = User(index + 1, row['Owner Name'], row['Password'], row['User Id'], row['Email Id'])

class ManageLoginSignIn:
    def __init__(self):
        self.users = users

    def updateDataFrame(self, new_row):
        global user_auth_data
        new_df = pd.DataFrame([new_row])
        user_auth_data = pd.concat([user_auth_data, new_df], ignore_index=True)
        user_auth_data.to_csv('GPS_based_Toll_System_User_Auth_Data.csv', index=False)
        user_auth_data = pd.read_csv('GPS_based_Toll_System_User_Auth_Data.csv')

        new_users = {}
        for index, row in user_auth_data.iterrows():
            self.users[row['Owner Name']] = User(index + 1, row['Owner Name'], row['Password'], row['User Id'], row['Email Id'])
        self.users = new_users

    def registerUser(self, entered_username, entered_email, entered_password):
        if entered_username in user_auth_data['Owner Name'].values:
            return "Error: Username already exists. Please choose a different username."
        if entered_email in user_auth_data['Email Id'].values:
            return "Error: Email already exists. Please choose a different email address."
        if entered_password in user_auth_data['Password'].values:
            return "Error: Password already taken. Please choose a different password."
        new_row = {
            "Owner Name": entered_username,
            "User Id": len(users)+1,  # Generate a new user ID
            "Email Id": entered_email,
            "Password": entered_password,
        }
        self.updateDataFrame(new_row)
        return redirect(url_for('login'))

    def loginUser(self, entered_username, entered_password):
         # Ensure we are using the updated users dictionary
        user = self.users.get(entered_username)
        # print(user.password)
        # print(entered_password)
        if user:
            if user.password == entered_password:
                login_user(user)
                check_vehicle_registered = user_data.loc[user_data['Owner Name'] == entered_username, 'Vehicle Number']
                if not check_vehicle_registered.empty:
                    return redirect(url_for('profile'))
                else:
                    return redirect(url_for("register_vehicle"))
            else:
                # flash('Invalid password')
                return "Error: Invalid Password"
        else:
            # flash('Invalid username')
            return "Error: Invalid Username"
        
class RegisterNewVehicle:
    def __init__(self):
        self.avg_speed = 0.0
        self.toll_price = 0.0

    def updateUserDataFrame(self, new_row):
        global user_data
        global user_transaction_data
        new_df = pd.DataFrame([new_row])
        new_transaction_row = {
            'Owner Name': new_row['Owner Name'],
            'User Id': new_row['User Id'],
            'Owner Account Number': new_row['Owner Account Number'],
            'Account Balance': [new_row['Account Balance']],
            'Toll price per km': [0.0],
            "Amount Charged": [0.0],
            "Entry Time Stamp": [""],
            "Entry Gate Coordinates": [""],
            "Exit Time Stamp": [""],
            "Exit Gate Coordinates": [""],
            "Distance Travelled": [0.0], 
            "Receipt":[''],
        }
        length = len(user_transaction_data)
        new_transaction_df =  pd.DataFrame.from_dict({length + 1: new_transaction_row}, orient='index')
        user_transaction_data = pd.concat([user_transaction_data, new_transaction_df], ignore_index=True)
        user_transaction_data.to_csv('GPS_based_Toll_System_User_Transaction_Data.csv', index=False)
        user_transaction_data = pd.read_csv('GPS_based_Toll_System_User_Transaction_Data.csv')
        # print(f"New transaction row\n{new_transaction_row} ")
        # new_transaction_df = pd.DataFrame([new_transaction_row])
        # print(f"New transaction dataframe\n{new_transaction_df} ")
        # user_transaction_data = pd.concat([user_transaction_data, new_transaction_df], ignore_index=True)
        # user_transaction_data.to_csv('GPS_based_Toll_System_User_Transaction_Data.csv', index=False)
        # user_transaction_data = pd.read_csv('GPS_based_Toll_System_User_Transaction_Data.csv')

        user_data = pd.concat([user_data, new_df], ignore_index=True)
        user_data.to_csv('GPS_based_Toll_System_Data.csv', index=False)
        user_data = pd.read_csv('GPS_based_Toll_System_Data.csv')

    def updateAuthDataFrame(self, loggedInUsername, userid):
        global user_auth_data
        user_auth_data.loc[user_auth_data['Owner Name'] == loggedInUsername, 'User Id'] = userid
        user_auth_data.to_csv('GPS_based_Toll_System_User_Auth_Data.csv', index=False)
        user_auth_data = pd.read_csv('GPS_based_Toll_System_User_Auth_Data.csv')

    
    def findAvgSpeed(self, vehicle_category):
        if vehicle_category in ['Sedan', 'HatchBack', 'Micro']:
            avg_speed = 60.0
        elif vehicle_category in ['Truck', 'Bus']:
            avg_speed = 40.0
        elif vehicle_category == 'SUV':
            avg_speed = 55.0
        elif vehicle_category == 'Sport':
            avg_speed = 75.0
        elif vehicle_category == 'Coupe':
            avg_speed = 65.0
        elif vehicle_category == 'Crossover':
            avg_speed = 70.0
        elif vehicle_category == 'Van':
            avg_speed = 50.0
        else:
            avg_speed = 80.0
        return avg_speed
    
    def calTollPrice(self, vehicle_category):
        if vehicle_category == 'Sedan':
            toll_price = 8.5
        elif vehicle_category == 'HatchBack':
            toll_price = 7.5
        elif vehicle_category == 'Micro':
            toll_price = 7.0
        elif vehicle_category == 'Bus':
            toll_price = 30.0
        elif vehicle_category == 'Truck':
            toll_price = 35.0
        elif vehicle_category == 'SUV':
            toll_price = 10.0
        elif vehicle_category == 'Sport':
            toll_price = 9.0
        elif vehicle_category == 'Coupe':
            toll_price = 8.0
        elif vehicle_category == 'Crossover':
            toll_price = 9.5
        elif vehicle_category == 'Van':
            toll_price = 6.0
        else:
            toll_price = 8.0
        return toll_price
    
    def addNewRow(self, vehicle_number, vehicle_category, account_number, account_balance):
        loggedInUsername = current_user.username
        self.avg_speed = self.findAvgSpeed(vehicle_category)
        self.toll_price = self.calTollPrice(vehicle_category)
        userid = loggedInUsername[0] + vehicle_category[0] + vehicle_number[-4:]
        update_user_data = user_auth_data.loc[user_auth_data['Owner Name'] == loggedInUsername]
        update_user_data['User Id'] = userid
        new_row = {
            'Vehicle Number': vehicle_number,
            'Category': vehicle_category,
            'Owner Name': loggedInUsername,
            'User Id': userid,
            'Owner Account Number': account_number,
            'Account Balance': account_balance,
            'Average Speed of vehicle': self.avg_speed,
            'Toll price per km': self.toll_price,
            "Amount Charged": 0.0,
            "Entry Time Stamp": "",
            "Entry Gate Coordinates": "",
            "Exit Time Stamp": "",
            "Exit Gate Coordinates": "",
            "Distance Travelled": 0.0,
        }
        
        self.updateUserDataFrame(new_row)
        self.updateAuthDataFrame(loggedInUsername, userid)

    @login_required
    def registerVehicle(self, owner_name, vehicle_number, vehicle_category, account_number, account_balance):
        # self.addNewRow(vehicle_number, vehicle_category, account_number, account_balance)
        # return redirect(url_for('profile'))
        loggedInUsername = current_user.username
        registered_username = user_auth_data.loc[user_auth_data['Owner Name'] == owner_name]
        existing_vehicle = user_data.loc[user_data['Owner Name'] == loggedInUsername]
        if owner_name == loggedInUsername and existing_vehicle.empty:
            if vehicle_number in user_data['Vehicle Number'].values:
                return "Please check your vehicle number"
            elif str(account_number) in user_data['Owner Account Number'].astype(str).values:
                return "Please check your Account number"
            elif float(account_balance) < 30000.0:
                return "Minimum balance should be 30000.0"
            self.addNewRow(vehicle_number, vehicle_category, account_number, account_balance)
            return redirect(url_for('profile'))
        if not existing_vehicle.empty and owner_name == loggedInUsername:
            # flash('You already have a registered vehicle. Multiple registrations are not allowed.')
            return "You already have a registered vehicle. Multiple registrations are not allowed."
        elif owner_name != loggedInUsername:
            return "This username is not present in data of Registered Users. Please logout and register first"
    


@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == int(user_id):
            return user
    return None

@app.route("/profile")
@login_required
def profile():
    logged_in_user = current_user.username
    user_auth_data_row = user_auth_data.loc[user_auth_data['Owner Name'] == logged_in_user]
    user_data_row = user_data.loc[user_data['Owner Name'] == logged_in_user]
    user_info={
        "Username": logged_in_user,
        "Email": user_auth_data_row['Email Id'],
        "User Id": user_auth_data_row['User Id'],
        "Password": user_auth_data_row['Password'],
        "Vehicle Number":user_data_row['Vehicle Number'],
        "Vehicle Category": user_data_row['Category'],
    }
    return render_template("profile.html",user_info = user_info, bootstrap=bootstrap)

@app.route("/register_vehicle", methods=['GET', 'POST'])
def register_vehicle():
    newVehicle = RegisterNewVehicle()
    if request.method == 'POST':
        owner_name = request.form['name']
        vehicle_number = request.form['vnumber']
        vehicle_category = request.form['vcategory']
        account_number = request.form['acctnumber']
        account_balance = request.form['acctbalance']
        return newVehicle.registerVehicle(owner_name,vehicle_number, vehicle_category, account_number, account_balance)
    if request.method == 'GET':
        return render_template('register_vehicle.html')
    

@app.route("/profile/transactions")
@login_required
def transactions():
    logged_in_user = current_user.username
    user_dict = user_transaction_data[user_transaction_data['Owner Name'] == logged_in_user].to_dict(orient='records')[0]
    # print(user_dict)
    # user_dict_df = pd.DataFrame([user_dict])
    

    user_dict['Toll price per km']= ast.literal_eval(user_dict['Toll price per km'])
    user_dict['Account Balance']= ast.literal_eval(user_dict['Account Balance'])
    user_dict['Amount Charged']= ast.literal_eval(user_dict['Amount Charged'])
    user_dict['Entry Time Stamp']= ast.literal_eval(user_dict['Entry Time Stamp'])
    user_dict['Entry Gate Coordinates']= ast.literal_eval(user_dict['Entry Gate Coordinates'])
    user_dict['Exit Time Stamp']= ast.literal_eval(user_dict['Exit Time Stamp'])
    user_dict['Exit Gate Coordinates']= ast.literal_eval(user_dict['Exit Gate Coordinates'])
    user_dict['Distance Travelled']= ast.literal_eval(user_dict['Distance Travelled'])
    
    user_dict['Receipt'] = ast.literal_eval(user_dict['Receipt'])
    print(user_dict['Receipt'])
    return render_template("transactions.html", data=user_dict, bootstrap=bootstrap)



    
@app.route("/simulation")
def simulation():
    loggedInUser = current_user.username
    loggedInUser_vnum = user_data.loc[user_data['Owner Name'] == current_user.username, 'Vehicle Number'].values[0]
    return render_template("simulation.html",vnum = loggedInUser_vnum, bootstrap=bootstrap)

@app.route("/start_simulation")
def start_simulation():
    global user_transaction_data
    global user_data
    loggedInUser = current_user.username
    print(loggedInUser)
    lt = startSimulation(loggedInUser,user_data)
    transaction_df = lt[0]
    user_df = lt[1]
    user_transaction_data = transaction_df.copy()
    user_data = user_df.copy()
    return redirect(url_for('transactions'))

@app.route('/show_map/<int:position_id>', methods=['GET', 'POST'])
def show_map(position_id):
    vnum = user_data.loc[user_data['Owner Name'] == current_user.username, 'Vehicle Number'].values[0]
    map_filename = f'vehicle_{vnum}_position_{position_id}.html'
    try:
        # return render_template(f'Output_HTML_files/{map_filename}')
        # map_filepath = os.path.join('Output_HTML_files', map_filename)
        map_filepath = 'Output_HTML_files/'+map_filename
        print(map_filepath)
        return send_file(map_filepath)
    except:
        abort(404)  

@app.route('/login_status')
def login_status():
    return jsonify({'logged_in': current_user.is_authenticated})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    login_object = ManageLoginSignIn()
    if request.method == 'POST':
        entered_username = request.form['name']
        entered_password = request.form['password']
    
        return login_object.loginUser(entered_username, entered_password)
    return render_template('login.html', bootstrap=bootstrap)

@app.route("/register", methods=['GET', 'POST'])
def register():
    register_object = ManageLoginSignIn()
    if request.method == 'POST':
        entered_username = request.form['name']
        entered_password = request.form['password']
        entered_email = request.form['email']

        return register_object.registerUser(entered_username, entered_email, entered_password)
    return render_template('register.html', bootstrap=bootstrap)

@app.route("/")
def home():
    return render_template('index.html', bootstrap=bootstrap)

if __name__ == '__main__':
    app.run(debug=True)
