USE CAR_HIRE_MANAGEMENT;

DROP TABLE IF EXISTS BOOKING;
CREATE TABLE BOOKING (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL, 
    vehicle_id INT NOT NULL,  
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id),
    FOREIGN KEY (vehicle_id) REFERENCES VEHICLE(vehicle_id),
    date_of_hire DATE,
    date_of_return DATE
);