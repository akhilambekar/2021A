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


#print(json.dumps(response, indent=4, sort_keys=True))
