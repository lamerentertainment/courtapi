import requests
import json

url = 'http://localhost:8000/api/v1/transform_text'
weburl = "https://courtapi.applikuapp.com/api/v1/transform_text"
payload = {
    'text': """Ich weiss nicht, was ich sa-
gen soll, es geht mir mies. Morgen werden wir auf den Mond ge-
hen""",
    'geschlecht': "m"
}

# Convert payload to JSON
json_payload = json.dumps(payload)

# Set the Content-Type header to indicate JSON data
headers = {'Content-Type': 'application/json'}

# Send the POST request
response = requests.post(weburl, data=json_payload, headers=headers)

# Print the response
print(response.json())