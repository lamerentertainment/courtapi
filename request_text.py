import requests
import json

url = 'http://localhost:8000/api/v1/transform_text'
payload = {'text': 'dies ist ein text'}

# Convert payload to JSON
json_payload = json.dumps(payload)

# Set the Content-Type header to indicate JSON data
headers = {'Content-Type': 'application/json'}

# Send the POST request
response = requests.post(url, data=json_payload, headers=headers)

# Print the response
print(response.json())