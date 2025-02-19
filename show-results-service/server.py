from flask import Flask, jsonify
import pymongo

app = Flask(__name__)

mongo_client = pymongo.MongoClient("mongodb://mongo:27017/")
mongo_db = mongo_client["analytics_db"]
analytics_collection = mongo_db["stats"]

@app.route('/results', methods=['GET'])
def get_results():
    result = analytics_collection.find_one(sort=[("_id", -1)])
    if not result:
        return jsonify({"message": "No analytics available"})
    
    del result["_id"]  # Remove MongoDB ObjectId
    return jsonify(result)

app.run(host='0.0.0.0', port=5003)
