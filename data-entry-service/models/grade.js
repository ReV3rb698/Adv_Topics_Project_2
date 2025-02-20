const mysql = require('mysql2');

// Database connection
const dbConfig = {
    host: 'mysql',
    user: 'root',
    password: 'root',  // Ensure this matches the MySQL container's root password
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

    connection.on('error', (err) => {
        console.error('MySQL connection error:', err);
        if (err.code === 'PROTOCOL_CONNECTION_LOST') {
            connectWithRetry();
        } else {
            throw err;
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
        connection.query(query, [subject, grade, creditHours, studentId], (err, results) => {
            if (err) {
                console.error('Error executing query:', err);
                return callback(err);
            }
            callback(null, results);
        });
    },
    // Add more methods for reading, updating, deleting grades
};

module.exports = Grade;