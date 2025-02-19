const express = require('express');
const mysql = require('mysql2');
const jwt = require('jsonwebtoken');

const app = express();
app.use(express.json());

const db = mysql.createConnection({
    host: 'mysql',
    user: 'root',
    password: 'root',
    database: 'data_db'
});

app.post('/enter-data', (req, res) => {
    const { token, value } = req.body;
    try {
        jwt.verify(token, "supersecret");
        db.query("INSERT INTO records (value) VALUES (?)", [value], (err, result) => {
            if (err) return res.status(500).json({ message: err.message });
            res.json({ message: "Data added" });
        });
    } catch (err) {
        res.status(401).json({ message: "Unauthorized" });
    }
});

app.listen(5001, () => console.log("Data Entry Service running on port 5001"));
