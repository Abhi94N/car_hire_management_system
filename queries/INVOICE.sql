USE CAR_HIRE_MANAGEMENT;

DROP TABLE IF EXISTS INVOICE;
CREATE TABLE INVOICE (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL UNIQUE,
    customer_id INT NOT NULL,
    invoice_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_status ENUM('Paid', 'Unpaid') NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id),
    FOREIGN KEY (customer_id) REFERENCES CUSTOMER(customer_id)
);