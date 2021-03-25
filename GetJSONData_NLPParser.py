#Import required modules
import requests
import json

# Get json results for the required input 

InputString = "kobe is a basketball player"

headers = {
    'Content-type': 'application/json',
}

data = '{"text":InputString = '+ InputString + '}'

response = requests.post('http://66.76.242.198:9888/', data=data).json()

#Adding a test comment to check if the automatic git pull is working or not

#print(json.dumps(response, indent=4, sort_keys=True))
