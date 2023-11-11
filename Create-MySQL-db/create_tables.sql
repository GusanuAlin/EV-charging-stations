CREATE SCHEMA `clever_database_int_12` ;
USE clever_database_int_12;
CREATE TABLE customers(
	user_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 user_email VARCHAR(45),
	first_name VARCHAR(45),
	last_name VARCHAR(45),
	subscription_type VARCHAR(45),
	vehicle_id INT UNSIGNED,
	total_time_current_month DECIMAL(10,2),
	card_id INT UNSIGNED);

CREATE TABLE charging_session (session_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
charging_station_id INT UNSIGNED,
user_id INT UNSIGNED,
energy_consumed DECIMAL(10,2),
start_time TIME,
end_time TIME,
total_time_minutes INT,
energy_price_per_kWh DECIMAL(10,2),
total_price DECIMAL(10,2));

CREATE TABLE charging_station (
  charging_station_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  hub_id INT UNSIGNED NOT NULL,
  connector_type VARCHAR(45),
  kw_hour_capacity INT,
  is_on TINYINT);

CREATE TABLE vehicle(
vehicle_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
car_manufacturer VARCHAR(45),
car_model VARCHAR(45),
port_type VARCHAR(45));

CREATE TABLE bookings(
booking_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
user_id INT UNSIGNED,
start_time TIME,
end_time TIME,
charging_station_id INT UNSIGNED);

CREATE TABLE charging_hub(
hub_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
hub_accessability VARCHAR(45),
hub_name VARCHAR(255),
hub_longitude FLOAT,
hub_latitude FLOAT,
street_name VARCHAR(255),
street_number VARCHAR(45),
postal_code INT UNSIGNED,
city VARCHAR(45),
capacity VARCHAR(45),
number_of_ports INT,
connector_type VARCHAR(45));

CREATE TABLE card(
card_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
account_number INT,
registration_number INT,
debit_number INT,
expiration_date DATE,
card_cvv INT,
first_name VARCHAR(45),
last_name VARCHAR(45),
Bank VARCHAR(45),
Bank_Location VARCHAR(45));


ALTER TABLE customers ADD CONSTRAINT FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id);
ALTER TABLE customers ADD CONSTRAINT FOREIGN KEY (card_id) REFERENCES card(card_id);
ALTER TABLE bookings ADD CONSTRAINT FOREIGN KEY (user_id) REFERENCES customers(user_id);
ALTER TABLE bookings ADD CONSTRAINT FOREIGN KEY (charging_station_id) REFERENCES charging_station(charging_station_id);
ALTER TABLE charging_session ADD CONSTRAINT FOREIGN KEY (charging_station_id) REFERENCES charging_station(charging_station_id);
ALTER TABLE charging_session ADD CONSTRAINT FOREIGN KEY (user_id) REFERENCES customers(user_id);
ALTER TABLE charging_station ADD CONSTRAINT FOREIGN KEY (hub_id) REFERENCES charging_hub(hub_id);

