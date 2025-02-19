from flask import Flask, jsonify
import pymysql
import pymongo

app = Flask(__name__)

mysql_conn = pymysql.connect(host='mysql', user='root', password='root', database='data_db')
mongo_client = pymongo.MongoClient("mongodb://mongo:27017/")
mongo_db = mongo_client["analytics_db"]
analytics_collection = mongo_db["stats"]

@app.route('/analyze', methods=['GET'])
def analyze_data():
    with mysql_conn.cursor() as cursor:
        cursor.execute("SELECT value FROM records")
        data = [row[0] for row in cursor.fetchall()]
    
    if not data:
        return jsonify({"message": "No data available"})
    
    stats = {
        "max": max(data),
        "min": min(data),
        "avg": sum(data) / len(data)
    }

    analytics_collection.insert_one(stats)
    return jsonify(stats)

app.run(host='0.0.0.0', port=5002)
