import requests

response = requests.get(
    "https://publicapis.io/api/careerjet/search",
    params={"keywords": "python developer", "location": "India"}
)
print(response.json())