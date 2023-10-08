USE CAR_HIRE_MANAGEMENT;

DROP TABLE IF EXISTS INVOICE;
DROP TABLE IF EXISTS BOOKING;
DROP TABLE IF EXISTS VEHICLE;
DROP TABLE IF EXISTS CUSTOMER;
CREATE TABLE CUSTOMER (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE
);
INSERT INTO CUSTOMER (name, phone_number, email) VALUES ('Abhilash Nair', '404-202-5249', "abhilashnair1994@gmail.com");
INSERT INTO CUSTOMER (name, phone_number, email) VALUES ('Fred Bob', '777-777-777', "FredBob@gmail.com");


CREATE TABLE VEHICLE (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    seats TINYINT NOT NULL,
    category  ENUM('Small Car', 'Family Car', 'Van') NOT NULL,
    year YEAR NOT NULL,
    license_plate VARCHAR(20) UNIQUE NOT NULL
);

INSERT INTO VEHICLE (make, model, seats, category, year, license_plate)
VALUES ('Toyota', 'Corolla', 4, 'Small Car', 2022, 'ABC123');

INSERT INTO VEHICLE (make, model, seats, category, year, license_plate)
VALUES ('Honda', 'Odyssey', 7, 'Family Car', 2021, 'XYZ456');

INSERT INTO VEHICLE (make, model, seats, category, year, license_plate)
VALUES ('Ford', 'Transit', 9, 'Van', 2020, 'DEF789');





CREATE TABLE BOOKING (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL, 
    vehicle_id INT NOT NULL,  
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id),
    FOREIGN KEY (vehicle_id) REFERENCES VEHICLE(vehicle_id),
    date_of_hire DATE,
    date_of_return DATE
);

CREATE TABLE INVOICE (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    customer_id INT NOT NULL,
    invoice_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_status ENUM('Paid', 'Unpaid') NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id),
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id)
);