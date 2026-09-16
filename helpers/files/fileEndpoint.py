import json

def read(fileName):
    try:
        with open(fileName, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Error: 'data.json' file was not found.")

def update(fileName, data):
    try:
        with open(fileName, "w") as file:
            json.dump(data, file)
    except:
        print("Error: 'data.json' file was not found.")