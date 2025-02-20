import pymysql
import pymongo
import time

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
mongo_client = pymongo.MongoClient('mongodb://mongo:27017')
mongo_db = mongo_client['gpa_analytics_db']
mongo_collection = mongo_db['gpa_analytics']

def calculate_gpa(student_id):
    with mysql_connection.cursor() as cursor:
        cursor.execute("SELECT grade, credit_hours FROM grades WHERE student_id = %s", (student_id,))
        grades = cursor.fetchall()

        total_weighted_grades = sum([grade * credit for grade, credit in grades])
        total_credit_hours = sum([credit for _, credit in grades])

        gpa = total_weighted_grades / total_credit_hours if total_credit_hours != 0 else 0

        # Store in MongoDB
        mongo_collection.insert_one({
            'student_id': student_id,
            'gpa': gpa
        })
        return gpa

def store_analytics():
    # Retrieve all GPAs from MongoDB for analytics
    gpas = [record['gpa'] for record in mongo_collection.find()]
    
    if gpas:
        max_gpa = max(gpas)
        min_gpa = min(gpas)
        avg_gpa = sum(gpas) / len(gpas)

        # Store in MongoDB analytics collection
        mongo_db['analytics'].insert_one({
            'max_gpa': max_gpa,
            'min_gpa': min_gpa,
            'avg_gpa': avg_gpa
        })
