import pymysql
import pymongo
import time
from pymongo import MongoClient
from flask import Flask, request, jsonify

app = Flask(__name__)

# MySQL connection
mysql_config = {
    'host': 'mysql',
    'user': 'root',
    'password': 'root',
    'database': 'student_db'
}

# Function to create a connection with retry mechanism
def connect_with_retry():
    connection = None
    while connection is None:
        try:
            connection = pymysql.connect(**mysql_config)
            print('Connected to MySQL')
        except pymysql.MySQLError as err:
            print(f'Error connecting to MySQL: {err}')
            time.sleep(5)  # Retry after 5 seconds
    return connection

# Create a connection
mysql_connection = connect_with_retry()

# MongoDB connection
try:
    mongo_client = MongoClient("mongodb://mongo:27017")
    db = mongo_client.gpa_analytics_db
    gpas_collection = db.gpas
    print('Connected to MongoDB')
except pymongo.errors.ConnectionError as err:
    print(f'Error connecting to MongoDB: {err}')
    mongo_client = None

# Function to get grades and credit_hours from MySQL
def get_grades_and_credit_hours(student_id):
    conn = pymysql.connect(**mysql_config)
    cursor = conn.cursor()
    query = "SELECT grade, credit_hours FROM grades WHERE student_id = %s"
    cursor.execute(query, (student_id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Function to calculate GPA
def calculate_gpa(grades_and_credit_hours):
    total_grades = 0
    total_credit_hours = 0
    for grade, credit_hours in grades_and_credit_hours:
        total_grades += grade * credit_hours
        total_credit_hours += credit_hours
    if total_credit_hours == 0:
        return 0  # Avoid division by zero if no credit hours
    return total_grades / total_credit_hours

# Route to get GPA for a student and store in MongoDB
@app.route('/calculate_gpa', methods=['GET'])
def calculate_and_store_gpa():
    student_id = request.args.get('student_id')
    
    if not student_id:
        return jsonify({'error': 'Student ID is required'}), 400

    # Get grades and credit_hours from MySQL
    grades_and_credit_hours = get_grades_and_credit_hours(student_id)
    
    if not grades_and_credit_hours:
        return jsonify({'error': 'No grades found for this student'}), 404

    # Calculate GPA
    gpa = calculate_gpa(grades_and_credit_hours)

    # Insert GPA into MongoDB
    gpas_collection.insert_one({
        'student_id': student_id,
        'gpa': gpa
    })

    # Return the calculated GPA as a response
    return jsonify({'student_id': student_id, 'gpa': gpa})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
