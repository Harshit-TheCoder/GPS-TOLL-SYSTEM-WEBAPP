WELCOME TO TOLLMATE README.
Here you will find all the necessary information regarding this WebApp.👇 

This is GPS BASED TOLL SYSTEM WEB APP made using PYTHON FLASK.

General Information:
This WebApp takes into account the Area around Kherki Daula Toll Plaza on Delhi-Gurgaon Expressway.
The Website assumes that a single user can have only have one vehicle so allows the Logged In to register ONLY ONE vehicle under his/her name.
The following categories of Vehicles are allowed:👇 
1) Sedan
2) Coupe
3) Truck
4) Bus
5) HatchBack
6) Crossover
7) Sport
8) Micro
9) SUV
10) Van

Steps to clone this repository:
1) Ensure git is installed in your PC alongwith Python and Flask module.
2) Create a new folder and open it with VSCode. Then go to the Terminal.
3) You can clone this project by pasting the following command "git clone https://github.com/Harshit-TheCoder/GPS-TOLL-SYSTEM-WEBAPP.git" in your terminal.

Steps to run the Flask App:
1) Go to the main.py file and click the run button.
2) In the terminal you will find this link "http://127.0.0.1:5000/".
3) Click this link and you will be directed to the website.
4) Press Ctrl+C to stop the WebApp from running.

Guidelines:
1) Files are organized as required by the Python Flask Framework
2) You will find the HTML Files in templates folder, CSS and JS files in static folder
3) THE USER DATA IS STORED IN 3 .csv FILES.
   1) General Information is stored in GPS_based_Toll_System_Data.csv
   2) Authentication Related Information is stored in GPS_based_Toll_System_User_Auth_Data.csv
   3) Transactions Related Information is stored in GPS_based_Toll_System_User_Transaction_Data.csv
5) Website Explanation:
   1) After Website gets loaded, a Google Form will pop up to collect general information of the user, you may fill it
   2) You have to FIRST REGISTER, THEN LOGIN, THEN REGISTER YOUR VEHICLE AT /register, /login and /register_vehicle routes respectively
   3) You would be able to access /profile route only after you login
   4) /profile route will have a dashboard with a "Start Simulation" button, /simulation route will display the vehicle movement simulation.
       "Google Cloud Console" Platform API has been used for Generating Maps. GREEN MARKER IS YOUR ENTRY POINT. RED MARKER IS YOUR EXIT POINT. YELLOW MARKERS ARE YOUR CHECK POINTS AND BLUE MARKER IS YOU.
       As you click different buttons, you will see the BLUE MARKER  moving from Source to Destination. /transactions route has all the transaction details of the user.
       This route has "Show Toll Prices" button. It pops a modal containing info about the toll prices depending upon vehicle category and congestion time.
       It also displays the entire transaction history and a Toll Receipt is attached with each transaction.
   5) When you click the "Start Simulation" button, THE BACKEND WILL TAKE 2-3 MINUTES TO RUN THE SIMULATION after which you will be REDIRECTED to /transactions route where you can find the Receipt,
    Transaction History and Toll Info
   6) Then you can check the /simulation route to find the simulation in the form of Maps generated using Folium.
   7) You can Logout once your work is done.

What does the Website try to show:
The Website tries to simulate the upcoming technology of GPS based Toll System in India which will soon replace the Fastag Technology. 
In Real Life Scenario, when vehicle enters the Tollzone, the scanner at entry point will scan the GPS chip, Info Chip in Vehicle's number plate and get information about the gps coordinates, 
car and owner account details.
As soon as the vehicle crosses the exit point, the toll amount is deducted from user account and the receipt is generated and sent to the App alongwith updation of User Transaction History.
In My Web App, as you enter your credentials, you see your dashboard, upon clicking the "Start Simulation" button, the simulation starts in which a car is made to run from a random entry point to the exit point.
This process is similar to the car moving in an actual TollZone. Once your car leaves, the toll zone, the amount is deducted using DISTANCE BASED CALCULATION and /transactions route is updated.
Hence this website is a complete means of visualizing how the GPS based Toll Systems would work in real life.

Modules used:
1) numpy and pandas
2) flask
3) flask_bootstrap
4) flask_login
5) ast
6) googlemaps
7) simpy
8) geopy
9) folium
10) IPython
11) datetime
12) matplotlib
13) io
14) PIL
15) requests
16) time
17) random
18) dot_env

You can install these modules using pip.
THANK YOU!!!! Hope you have a nice experience.
   


