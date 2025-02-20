from flask import Flask
from models.analytics import get_gpa, get_analytics

app = Flask(__name__)

@app.route('/results/<student_id>', methods=['GET'])
def show_results(student_id):
    gpa = get_gpa(student_id)
    if gpa is None:
        return {"message": "No GPA data available"}
    
    analytics = get_analytics()
    return {"gpa": gpa, "analytics": analytics}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
