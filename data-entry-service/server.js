const express = require('express');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const Grade = require('./models/grade.js');  // Your Grade model

const app = express();
const port = 5001;  // You can change the port if needed

// Secret Key for JWT (should be the same as in auth-service)
const SECRET_KEY = "my_super_secret_key";

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Authentication middleware
const authenticate = (req, res, next) => {
    const token = req.header('authorization');
    if (!token) {
        return res.status(403).send('Forbidden');
    }

    jwt.verify(token, SECRET_KEY, (err, user) => {
        if (err) {
            return res.status(403).send('Invalid token');
        }
        req.user = user;
        next();
    });
};

// Route to enter grade data
app.post('/enter-data', authenticate, (req, res) => {
    const { subject, grade, creditHours, studentId } = req.body;

    if (!subject || !grade || !creditHours || !studentId) {
        return res.status(400).send('Missing required fields');
    }

    // Use the Grade model to insert the data
    Grade.create(subject, grade, creditHours, studentId, (err, results) => {
        if (err) {
            return res.status(500).send('Error inserting data');
        }
        res.status(201).send({ message: 'Grade added successfully', id: results.insertId });
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});