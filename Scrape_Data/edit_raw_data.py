import json

def setMinFollowers(data, followers):
    
    removedIds = [user["id"] for user in data["nodes"] if user["followers"] < followers]
    data["nodes"] = list(filter(lambda x: x["followers"] >= followers, data["nodes"]))
    data["links"] = list(filter(lambda x: not (x["source"] in removedIds or x["target"] in removedIds), data["links"]))

    return data

def removeSolos(data):

    sources = list(map(lambda x: x["source"], data["links"]))
    targets = list(map(lambda x: x["target"], data["links"]))
    data["nodes"] = list(filter(lambda x: (x["id"] in sources or x["id"] in targets), data["nodes"]))

    return data["nodes"]


def shrink(links, scale):
    
    new_links = []
    for index, link in enumerate(links):
        if index % scale == 0:
            new_links.append(link)
    
    return new_links


def edit(nameOfFolder):

    with open(f"./public/Maps/{nameOfFolder}/TwitterMapRaw.json", "r") as f:
        data = json.load(f)

    print(f"Editing data of {nameOfFolder}:")

    if "y" in input("    Would you like to shrink number of links (recommended for graphs above 750 nodes) (y/N)"):
        print("    Shrinking nodes to fit screen...")
        data["links"] = shrink(data["links"], 8)
    
    if "y" in input("    Would you like to set a minimum followers for nodes (y/N)"):
        while not (minFollowers := input("  What is your minimum followers required for node on map: ").isdigit()):
            print("    That is not a valid number")
        data = setMinFollowers(data, minFollowers / 1000000)
    
    if "y" in input("   Would you like to remove the nodes who don't connect with anyone (y/N)"):
        data["nodes"] = removeSolos(data)

    with open(f"./public/{nameOfFolder}/TwitterMap.json", "w") as f:
        json.dump(data, f, indent=4)