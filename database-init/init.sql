-- Create the database (this is done by the Dockerfile, but we can leave it here just in case)
CREATE DATABASE IF NOT EXISTS student_db;

-- Use the created database
USE student_db;

-- Create the grades table
CREATE TABLE IF NOT EXISTS grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject VARCHAR(255) NOT NULL,
    grade FLOAT NOT NULL,
    credit_hours INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
