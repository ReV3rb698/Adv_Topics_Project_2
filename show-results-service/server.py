from flask import Flask, request, jsonify
import jwt
from flask_pymongo import PyMongo
import datetime
from functools import wraps

app = Flask(__name__)

# Secret key for JWT encoding and decoding
JWT_SECRET_KEY = 'your_jwt_secret_key'

# MongoDB setup
app.config["MONGO_URI"] = "mongodb://mongo:27017/student_results"
mongo = PyMongo(app)

# Middleware to verify JWT token
def verify_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('token')  # Token should be passed in headers

        if not token:
            return jsonify({"message": "Token is missing!"}), 403

        try:
            # Decode the token
            decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            # Attach user information to the request
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 403

        return f(*args, **kwargs)

    return decorated_function

# Create a route to fetch results for the authenticated user
@app.route('/show-results', methods=['GET'])
@verify_token
def show_results():
    # Get studentId from decoded token
    student_id = request.user.get('id')

    # Query MongoDB for the student's results
    result = mongo.db.results.find_one({"studentId": student_id})

    if not result:
        return jsonify({"message": "Results not found"}), 404

    # Return the results as JSON
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
