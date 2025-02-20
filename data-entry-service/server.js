const express = require('express');
const Grade = require('./models/grade');
const jwt = require('jsonwebtoken');
const app = express();
app.use(express.json());

// Authentication middleware (simplified)
const authenticate = (req, res, next) => {
    const token = req.headers['authorization'];
    if (!token) return res.status(403).json({ message: 'No token provided' });

    jwt.verify(token, 'secretkey', (err, decoded) => {
        if (err) return res.status(401).json({ message: 'Invalid token' });
        req.user = decoded;  // Attach user info to request
        next();
    });
};

app.post('/enter-grade', authenticate, (req, res) => {
    const { subject, grade, creditHours } = req.body;
    const studentId = req.user.studentId;

    Grade.create(subject, grade, creditHours, studentId, (err, result) => {
        if (err) return res.status(500).json({ message: 'Error adding grade' });
        res.status(200).json({ message: 'Grade added' });
    });
});

app.listen(5001, () => console.log('Data entry service running on port 5001'));
