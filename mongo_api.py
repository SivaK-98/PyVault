import requests
import json
import os

url = "https://ap-south-1.aws.data.mongodb-api.com/app/data-emqlr/endpoint/data/v1/action/find"
key = os.getenv("vault_key")
payload = json.dumps({
    "collection": "users",
    "database": "auth",
    "dataSource": "Cluster0",
})
headers = {
    'Content-Type': 'application/json',
    'Access-Control-Request-Headers': '*',
    'api-key': key
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
