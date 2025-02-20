const mysql = require('mysql2');

// Database connection
const dbConfig = {
    host: 'mysql',
    user: 'root',
    password: 'root',
    database: 'student_db'
};

// Function to create a connection with retry mechanism
function connectWithRetry() {
    const connection = mysql.createConnection(dbConfig);

    connection.connect((err) => {
        if (err) {
            console.error('Error connecting to MySQL:', err);
            setTimeout(connectWithRetry, 5000); // Retry after 5 seconds
        } else {
            console.log('Connected to MySQL');
        }
    });

    return connection;
}

// Create a connection
const connection = connectWithRetry();

// Create Grade model
const Grade = {
    create: (subject, grade, creditHours, studentId, callback) => {
        const query = 'INSERT INTO grades (subject, grade, credit_hours, student_id) VALUES (?, ?, ?, ?)';
        connection.query(query, [subject, grade, creditHours, studentId], callback);
    },
    // Add more methods for reading, updating, deleting grades
};

module.exports = Grade;
