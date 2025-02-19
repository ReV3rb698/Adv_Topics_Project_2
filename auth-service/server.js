const express = require('express');
const jwt = require('jsonwebtoken');

const app = express();
app.use(express.json());

const users = [{ username: "user1", password: "password" }]; // Dummy users
const SECRET_KEY = "supersecret";

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    const user = users.find(u => u.username === username && u.password === password);
    if (user) {
        const token = jwt.sign({ username }, SECRET_KEY, { expiresIn: '1h' });
        return res.json({ token });
    }
    res.status(401).json({ message: "Invalid credentials" });
});

app.listen(5000, () => console.log("Auth Service running on port 5000"));
