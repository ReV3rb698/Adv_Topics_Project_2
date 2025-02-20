from flask import Flask
from models.analytics import calculate_gpa, store_analytics

app = Flask(__name__)

@app.route('/analyze/<student_id>', methods=['GET'])
def analyze_data(student_id):
    gpa = calculate_gpa(student_id)
    store_analytics()
    return {"gpa": gpa}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
