import json

with open("responsefutbol .json", "r") as f:
    data = json.loads(f)
    
print(data)
