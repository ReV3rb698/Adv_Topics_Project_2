const mysql = require('mysql2');

// Database connection
const connection = mysql.createConnection({
    host: 'mysql',
    user: 'root',
    password: 'root',
    database: 'student_db'
});

// Create Grade model
const Grade = {
    create: (subject, grade, creditHours, studentId, callback) => {
        const query = 'INSERT INTO grades (subject, grade, credit_hours, student_id) VALUES (?, ?, ?, ?)';
        connection.query(query, [subject, grade, creditHours, studentId], callback);
    },
    // Add more methods for reading, updating, deleting grades
};

module.exports = Grade;
