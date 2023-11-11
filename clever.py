import mysql.connector
import sys,time
import datetime
import os
from time import sleep as sleep
from math import cos, asin, sqrt
from datetime import date
from datetime import time               #some of these may be redundant however removing them at the moment is more risky than its worth

#Databse Connection
db = mysql.connector.connect( 
    host = 'localhost',                         ##      Replace if your server is not hosted locally    
    user = 'root',                              ##      Replace with your own server username
    password = '3141',                          ##      Replace with your own server password
    database ='clever_database_int_12'
)
mycursor = db.cursor(buffered=True)   #buffrering prevents some errors with sql

today = date.today()
day = datetime.datetime.strftime(today,'%d/%m/%Y-')


#User session data & variables
new_user = ["null","null","null","null"]                           ###      <--------------------------- ###
create_booking = ["null","null"]                                   ###      <                            ###
evmodel = "null"                                                   ###      <    DO NOT MODIFY THIS!     ###
locuser_email = "null"                                             ###      <                            ###
user_me =    ["null","null","null","null","null","null","null"]    ###      <----------------------------###


usrlocation = ["55.692040745119414","12.554677049074812"]     ##   << Modify to change your longitude and latitude As such userlocation = ["LATITUDE","LONGITUDE"]     ##    


#? Class of codes for formatting text origingal code from https://stackoverflow.com/a/287944
class bcolors:      
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'   

#? Clears console 
def clean():  
    os.system('cls' if os.name == 'nt' else 'clear')


#? Menu for once the user is logged in or has created an account
def submenu():
    global create_booking
    global day
    charging_station_id = ""
    clean()
    mycursor = db.cursor(buffered=True)
    print(bcolors.HEADER + "🗲          🗲          🗲" + bcolors.BOLD + bcolors.ENDC,
    bcolors.OKBLUE + """
    1. <    Find nearest charging station 
    2. <    Reserve a station
    3. <    Check bookings
    _____________________________________
    q. <    Log-out
    """ + bcolors.ENDC)
    key2 = input('   >')
    if key2 == ('1'):
        print("finding your nearest charger")
        sleep(3)
        seek_nearest()

    elif key2 == ('2'):
        clean()
        print(bcolors.OKCYAN + "Select an available charging station" + bcolors.BOLD + bcolors.ENDC)
        print(bcolors.OKBLUE + """ 
        1. <    Meinungsgade 8
        2. <    Martensens Allé 13 - Frederiksberg
        3. <    Malmøgade 1 - København
        4. <    Føtex Nørrebro - København
        ____________________________________________
        q. <    Go back
        """)
        resvst = input("    >")
        if resvst == ("1"):
            charging_station_id = "1"
            
        elif resvst == ("2"):
            charging_station_id = "2"
            
        elif resvst == ("3"):
            charging_station_id = "3"
            
        elif resvst == ("4"):
            charging_station_id = "4"

        elif resvst == ("b"):
            menu()   

        clean()
        print("Please enter your reservation details    (in a HourMinute format!  Eg 13:40 is 13:40)")
        start_time_str = input('Starting at >')
        start_time1 = start_time_str
        
        end_time_str = input('Ending at >')
        end_time1 = end_time_str
        
        user_id = user_me[0]                #fetches user id from user data stored earlier
        create_booking = [start_time1,end_time1,user_id,charging_station_id]                
        mycursor.execute(insert_booking, create_booking)
        db.commit()

        print("booking created, starting at: ",start_time1," and ending at ",end_time1)
        sleep(3)

    elif key2 == ('3'):
        clean()
        if create_booking == ["null","null"]:
            print(bcolors.FAIL +"""
            You have no active bookings
            """ + bcolors.BOLD +bcolors.ENDC)
            input("Enter any key to continue")
        else:
            print("""Here is the last reservation you made
            """,day,create_booking)
            input("Enter any key to continue")

    elif key2 == ('q'):
        menu()

    else:
        print("Invalid input, please try again!")
        sleep(2)
    
    submenu()

#? A menu for whose without a clever account such as one time chargers
def submenu_nonmember():         
    clean()
    mycursor = db.cursor(buffered=True)
    print(bcolors.HEADER + "🗲          🗲          🗲" + bcolors.BOLD + bcolors.ENDC,
    bcolors.OKBLUE + """
    1. <    Find nearest charging station 
    _____________________________________
    q. <    Return to main menu 
    """ + bcolors.ENDC)
    key2n = input('   >')
    if key2n == ('1'):
        print("finding your nearest charger")
        sleep(3)
        mycursor = db.cursor(buffered=True)         # modified to fit our code but original formula is from https://stackoverflow.com/a/5548877
        near_statement = """SELECT hub_name, street_name, street_number, capacity, SQRT(POW(69.1 * (hub_latitude - %s), 2) + POW(69.1 * (%s - hub_longitude) * COS(hub_latitude / 57.3), 2)) AS distance FROM charging_hub HAVING distance < 25 ORDER BY distance;"""

        mycursor.execute(near_statement, usrlocation)               
        myresult = mycursor.fetchone()
        clean()
        print(bcolors.OKCYAN + "Your closest charging station is at:" + bcolors.ENDC)

        for x in myresult:
            print(bcolors.OKGREEN + x + bcolors.ENDC)

            input("Enter any key to proceed >")
            clean()
            submenu_nonmember()
    

    elif key2n == ('q'):
        menu()

    else:
        print("Invalid input, please try again!")
        sleep(2)

    submenu_nonmember()

#? Finds closest charging hub & address to the location given by 'usrlocation'
def seek_nearest():         #This is soo much simpler, it uses the same formula as before but written out differently  # modified to fit our code but original formula is from https://stackoverflow.com/a/5548877
    mycursor = db.cursor(buffered=True)
    near_statement = """SELECT hub_name, street_name, street_number, capacity, SQRT(POW(69.1 * (hub_latitude - %s), 2) + POW(69.1 * (%s - hub_longitude) * COS(hub_latitude / 57.3), 2)) AS distance FROM charging_hub HAVING distance < 25 ORDER BY distance;"""                       

    mycursor.execute(near_statement, usrlocation)               
    myresult = mycursor.fetchone()

    clean()
    print(bcolors.OKCYAN + "Your closest charging station is at:" + bcolors.ENDC)

    for x in myresult:
        print(bcolors.OKGREEN + x + bcolors.ENDC)

        cont = input("Enter any key to proceed >")
        submenu()


#?  User Login prompt
def loginmenu():
    valid_eml = ["null"]
    global locuser_email
    global user_me
    email_ipt = input("Enter your email address  >")
    locuser_email = [email_ipt]
    valid_eml = "select user_email from customers where user_email = %s"
    ulogin = "select * from customers where user_email = %s"
    mycursor.execute(valid_eml,locuser_email)
    dbuser = [row[0] for row in mycursor.fetchall()]
    if dbuser == locuser_email:
        print(bcolors.OKCYAN + "Please click the verication link we have sent to your email" + bcolors.BOLD + bcolors.ENDC)
        sleep(2)
        clean()
        mycursor.execute(ulogin,locuser_email)
        user_me = mycursor.fetchone()

        print ("Logged in!")
        sleep(1)
        submenu()
    elif email_ipt == ("b"):
        menu()
    else:
        pass
    
    while dbuser != locuser_email:
        print(bcolors.FAIL+"""
        Incorrect credentials, please try again! or enter b to go back.
        """+ bcolors.BOLD + bcolors.ENDC)
        loginmenu()
    




#? MAIN MENU
def menu():         
    clean()
    global new_user
    global user_me
    global evmodel
    global locuser_email
    print(bcolors.HEADER + """
  ___  _                     
 / __|| | ___ __ __ ___  _ _ 
| (__ | |/ -_)\ V // -_)| '_|
 \___||_|\___| \_/ \___||_|  

    """ + bcolors.ENDC)
    print(bcolors.OKBLUE + """
    1. <    Sign In
    2. <    Sign Up
    3. <    Charge without an account 
    """ + bcolors.ENDC)

    key = input('   >')
    if key == ('1'):
        loginmenu()

    elif key == ('2'):
        clean()
        print(bcolors.OKCYAN + "Lets get started" + bcolors.BOLD + bcolors.ENDC)
        print("Enter your email to create a new Clever profile")
        nipt_email = input('  >')
        locuser_email = [nipt_email]
        clean()
        print(bcolors.OKCYAN + "Check your email" + bcolors.BOLD + bcolors.ENDC)
        print("""
        We have send an email with an activation link.
        Click on the link to log in - that way you wont have to remember a password.
        """)
        sleep(1)
        clean
        print(bcolors.OKCYAN + "We are Clever - who are you?" + bcolors.BOLD + bcolors.ENDC)
        print("""Enter your name and press "next" """)
        first_name = input('Your first name  >')
        last_name = input('Your second name >')
        clean()
        print(bcolors.OKCYAN + "Please select your vehicle model" + bcolors.BOLD + bcolors.ENDC,
        bcolors.OKBLUE + """
        1. <    Tesla model S
        2. <    Tesla model X22
        3. <    Fiat 500 series
        4. <    Toyota SEV800 series
        5. <    Volvo Hertz series
        """ + bcolors.ENDC)
        evm = input('   >')
        if evm == ('1'):
            evmodel = "1"
        elif evm == ('2'):
            evmodel = "2"
        elif evm == ('3'):
            evmodel = "3"
        elif evm == ('4'):
            evmodel = "4"
        elif evm == ('5'):
            evmodel = "5"
        else:
            print("invalid input, please try again!")
            sleep(2)

        print(bcolors.OKCYAN + "Please wait while we set you up" + bcolors.BOLD + bcolors.ENDC)
        new_user = [nipt_email,first_name,last_name,evmodel]
        mycursor.execute(insert_statement, new_user)
        db.commit()
        ulogin = "select * from customers where user_email = %s"
        mycursor.execute(ulogin,locuser_email)
        user_me = mycursor.fetchone()
        clean()
        print(bcolors.OKCYAN + "Welcome!" + bcolors.BOLD + bcolors.ENDC)
        submenu()
        menu()

    elif key == ('3'):
        submenu_nonmember()
    
    else:
        print("Invalid input, please try again!")
        sleep(2)
    
    menu()
    


#? Statements for inserting data to the database (it wouldnt work if not done this way!)
insert_statement = """
    INSERT INTO customers (user_email, first_name, last_name, vehicle_id)
    VALUES (%s,%s,%s,%s)
"""
insert_booking = """
    INSERT INTO bookings (start_time,end_time,user_id,charging_station_id)
    VALUES (%s,%s,%s,%s)
"""

#Execution
clean()
menu()
quit()