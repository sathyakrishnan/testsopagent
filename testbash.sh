curl http://localhost:8000/api/health

# Get token
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=mendix_client&password=secret" | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")


  # Submit FNOL
curl -X POST "http://localhost:8000/api/v1/claims/fnol" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "claimType": "ACCIDENT",
    "jurisdiction": "UK",
    "policyHolder": {
      "policyNumber": "POL-123",
      "firstName": "John",
      "lastName": "Doe",
      "contactInformation": {"primaryPhone": "+1-555-555-1234"}
    },
    "incidentDetails": {
      "incidentDate": "2026-01-10T10:00:00Z",
      "incidentType": "MOTOR_VEHICLE_ACCIDENT",
      "incidentDescription": "Rear-ended at stop light"
    },
    "submissionMetadata": {
      "submittedBy": "John Doe",
      "submissionTimestamp": "2026-01-10T10:00:00Z"
    }
  }'


# Make 12 rapid requests - 11th and 12th should fail - update rate limit to 10 in environment file
for i in {1..12}; do
  echo "Request $i"
  curl -X POST "http://localhost:8000/api/v1/claims/fnol" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"claimType":"ACCIDENT", ...}'
done
