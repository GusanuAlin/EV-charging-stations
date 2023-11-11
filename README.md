# EV-charging-stations

This program is a proof-of-concept prototype for a suggested reservation/booking feature for the clever mobile app.

Developed and tested in: Windows 10
Language: English
Programing language: 'SQL','Python'
Python version: 3.9.9




## FIRST TIME SETUP
#Database setup:

requires that MYSQL_Workbench and a local MYSQL server are installed and running.
1. Open MySQL Workbench and access your local server.
2. Go to “File” – “Open SQL Script” or press “Ctrl+Shift+O”, select “Create_tables” .
3. Run the script and check into the” Action/Output” box at the bottom og the page for any errors.
4. Press the refresh button into the right-upper corner of the “SCHEMAS” box, now you should be able to see the new database named “clever_database_int_12”.
5. Go to “File” – “Open SQL Script” or press “Ctrl+Shift+O”, select “Insert_data” .
6. Run the script and check into the” Action/Output” box at the bottom of the page for any errors.

#Python setup:

Set your SQL connection credentails such as ' user="root" ' & ' password="1234" ' as commented in script.

Set your geolocation:
You can set your latitude and longitude by replacing the values in 'userlocation = ["latitude","longitude"]' with your own. (Values must be in quotations)


## RUNNING THE PROGRAM

To deploy this program run clever.py with python or drag the script into a terminal window and run.

To exit: Simply close the terminal that you are running the program with or use the stop execution hotkey appropriate for your system.


## Features

- Create and add new users to database
- Log in to existing accounts
- Create reservations on charging stations
- Find charging station nearest to user set location
- Find nearest station without logging in


## For Further help

 - [Getting Started with mysql](https://dev.mysql.com/doc/mysql-getting-started/en/)
 - [Execute a python script](Execute Python scripts)

## Acknowledgements & References

 - [Colored text in terminal](https://stackoverflow.com/a/287944)
 - [Nearest loction with latitude](https://stackoverflow.com/a/5548877)

 
