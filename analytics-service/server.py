from flask import Flask, jsonify
from models.analytics import calculate_gpa, store_analytics

app = Flask(__name__)

@app.route('/analyze/<student_id>', methods=['GET'])
def analyze_data(student_id):
    print(f'Analyzing data for student_id {student_id}')
    gpa = calculate_gpa(student_id)
    if gpa is None:
        return jsonify({"error": "Failed to calculate GPA"}), 500

    store_analytics()
    return jsonify({"gpa": gpa})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)