#!/bin/bash

# Variables
AUTH_SERVICE_URL="http://localhost:5000/login"
DATA_ENTRY_SERVICE_URL="http://localhost:5001/enter-data"
ANALYTICS_SERVICE_URL="http://localhost:5002/calculate_gpa"
SHOW_RESULTS_SERVICE_URL="http://localhost:5003/gpa-statistics"
USERNAME="testuser"
PASSWORD="password"
STUDENT_ID="1"

# Function to get JWT token
get_jwt_token() {
    response=$(curl -s -X POST $AUTH_SERVICE_URL -H "Content-Type: application/json" -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")
    token=$(echo $response | jq -r '.token')
    echo $token
}

# Function to insert grade data (no bearer)
insert_grade_data() {
    local token=$1
    read -p "Enter subject: " SUBJECT
    read -p "Enter grade: " GRADE
    read -p "Enter credit hours: " CREDIT_HOURS
    response=$(curl -s -X POST $DATA_ENTRY_SERVICE_URL -H "Content-Type: application/json" -H "Authorization: $token" -d "{\"subject\": \"$SUBJECT\", \"grade\": \"$GRADE\", \"creditHours\": $CREDIT_HOURS, \"studentId\": \"$STUDENT_ID\"}")   
    echo $response
}

# Function to analyze data
analyze_data() {
    response=$(curl -s -X GET "$ANALYTICS_SERVICE_URL?student_id=$STUDENT_ID")
    echo $response
}

# Function to get GPA statistics
get_gpa_statistics() {
    local token=$1
    response=$(curl -s -X GET $SHOW_RESULTS_SERVICE_URL -H "Authorization: Bearer $token")
    echo $response
}

# Main script
echo "Getting JWT token..."
token=$(get_jwt_token)
if [ "$token" == "null" ]; then
    echo "Failed to get JWT token"
    exit 1
fi
echo "JWT token obtained: $token"

echo "Inserting grade data..."
response=$(insert_grade_data $token)
echo "Response: $response"

# # fake it till you make it
# echo "Getting GPA statistics... "
# response=$(analyze_data)
# echo "Response: $response"

echo "Analyzing data..."
response=$(analyze_data)
echo "Response: $response"

echo "Getting GPA statistics..."
response=$(get_gpa_statistics $token)
echo "Response: $response"