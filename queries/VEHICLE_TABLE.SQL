USE CAR_HIRE_MANAGEMENT;

DROP TABLE IF EXISTS VEHICLE;
CREATE TABLE VEHICLE (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    make VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    seats TINYINT NOT NULL,
    category  ENUM('Small Car', 'Family Car', 'Van') NOT NULL,
    year YEAR NOT NULL,
    registration_number VARCHAR(20) UNIQUE NOT NULL
);

INSERT INTO VEHICLE (make, model, seats, category, year, registration_number)
VALUES ('Toyota', 'Corolla', 4, 'Small Car', 2022, 'ABC123');

INSERT INTO VEHICLE (make, model, seats, category, year, registration_number)
VALUES ('Honda', 'Odyssey', 7, 'Family Car', 2021, 'XYZ456');

INSERT INTO VEHICLE (make, model, seats, category, year, registration_number)
VALUES ('Ford', 'Transit', 9, 'Van', 2020, 'DEF789');