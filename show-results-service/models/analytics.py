import pymongo

# MongoDB connection
mongo_client = pymongo.MongoClient('mongodb://mongo:27017')
mongo_db = mongo_client['gpa_analytics_db']
mongo_collection = mongo_db['analytics']

def get_gpa(student_id):
    result = mongo_collection.find_one({'student_id': student_id}, sort=[('_id', -1)])  # Get latest GPA
    return result['gpa'] if result else None

def get_analytics():
    result = mongo_db['analytics'].find_one({}, sort=[('_id', -1)])  # Latest analytics
    return result if result else {}
