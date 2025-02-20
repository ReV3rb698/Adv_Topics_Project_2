#!/bin/bash

# Variables
AUTH_SERVICE_URL="http://localhost:5000/login"
DATA_ENTRY_SERVICE_URL="http://localhost:5001/enter-data"
USERNAME="testuser"
PASSWORD="password"
SUBJECT="Math"
GRADE="85"
CREDIT_HOURS=3
STUDENT_ID="12345"

# Function to get JWT token
get_jwt_token() {
    response=$(curl -s -X POST $AUTH_SERVICE_URL -H "Content-Type: application/json" -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\"}")
    token=$(echo $response | jq -r '.token')
    echo $token
}

# Function to insert grade data
insert_grade_data() {
    local token=$1
    response=$(curl -s -X POST $DATA_ENTRY_SERVICE_URL -H "Content-Type: application/json" -H "Authorization: $token" -d "{\"subject\": \"$SUBJECT\", \"grade\": \"$GRADE\", \"creditHours\": $CREDIT_HOURS, \"studentId\": \"$STUDENT_ID\"}")
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