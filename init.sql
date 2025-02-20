-- Create Database
CREATE DATABASE IF NOT EXISTS student_db;

-- Use the created database
USE student_db;

-- Create the grades table
CREATE TABLE IF NOT EXISTS grades (
    id INT AUTO_INCREMENT PRIMARY KEY,   -- Unique ID for each record
    student_id INT NOT NULL,             -- ID of the student (could be a unique identifier)
    subject VARCHAR(255) NOT NULL,       -- Name of the subject/course
    grade FLOAT NOT NULL,                -- Grade received by the student (e.g., 3.5, 4.0)
    credit_hours INT NOT NULL,           -- Number of credit hours for the course
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Time when the record was created
);

-- Optional: Create a sample student entry (for testing purposes)
-- INSERT INTO grades (student_id, subject, grade, credit_hours) 
-- VALUES (1, 'Math', 4.0, 3), (1, 'Science', 3.5, 4), (2, 'History', 3.8, 3);
