const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');

const app = express();
app.use(express.json());

// Mock User Database (Replace with real DB in production)
const users = [
    { id: 1, username: "testuser", password: bcrypt.hashSync("password", 10) }
];

// Secret Key for JWT
const SECRET_KEY = "my_super_secret_key";

// Login API (User provides username & password)
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    
    // Find user
    const user = users.find(u => u.username === username);
    if (!user || !bcrypt.compareSync(password, user.password)) {
        return res.status(401).json({ message: "Invalid credentials" });
    }

    // Generate JWT Token
    const token = jwt.sign({ userId: user.id, username: user.username }, SECRET_KEY, { expiresIn: '1h' });

    res.json({ token });
});

// Middleware: Validate JWT Token
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1]; // Extract token after "Bearer"

    if (!token) {
        return res.status(403).json({ message: "No token provided" });
    }

    jwt.verify(token, SECRET_KEY, (err, user) => {
        if (err) {
            return res.status(403).json({ message: "Invalid token" });
        }
        req.user = user;
        next();
    });
}

// Verify Token API
app.post('/verify', authenticateToken, (req, res) => {
    res.json(req.user);
});

// Example Protected Route (Just to Test Authentication)
app.get('/protected', authenticateToken, (req, res) => {
    res.json({ message: "You have access!", user: req.user });
});

app.listen(5000, () => console.log("Auth Service running on port 5000"));