import json

with open("./public/Maps/ElonMusk/TwitterMap.json", "r") as f:
    data = json.load(f)

for node in data["nodes"]:
    node["followers"] = int(1000000 * node["followers"])

with open(f"./public/Maps/ElonMusk/TwitterMapRaw.json", "w") as f:
    json.dump(data, f, indent=4)
