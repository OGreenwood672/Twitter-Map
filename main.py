from collections import defaultdict
from decouple import config
import json
import os

from TwitterAPI import TwitterAPI

def removeNonMutuals(links):
    dic = defaultdict(list)
    mutuals = []
    for link in links:
        dic[link["source"]].append(link["target"])
    for link in links:
        if link["source"] in dic[link["target"]]:
            mutuals.append(link)
            dic[link["source"]].remove(link["target"])
    return mutuals


def save(folderName, DATA):
    newFolderPath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), folderName)
    try:
        os.remove(newFolderPath)
    except:
        pass
    os.mkdir(newFolderPath)
    with open(f"../{folderName}/TwitterMutualMap.json", "w") as f:
        json.dump(DATA, f, indent=4)


def refactorFollowers(nodes, scale):
    for node in nodes:
        node["followers"] *= scale
    return nodes

def getUserFollowings(API, nodes, user_id, next_token=None):
    nodes, next_token = API.getFollowings(nodes, user_id, pagination_token=next_token)
    if next_token != None:
        nodes, next_token = getUserFollowings(API, nodes, user_id, next_token)
    return nodes, next_token

def getIds():
    with open("./peopleToScrape.txt", "r") as f:
        return list(map(int, [line.split("=")[1] for line in f.read().split("\n")]))

def getNames():
    with open("./peopleToScrape.txt", "r") as f:
        return [line.split("=")[0] for line in f.read().split("\n")]

def main():
    API = TwitterAPI(config("TWITTER_BEARER_TOKEN"), True)

    user_ids = getIds()
    user_names = getNames()
    for user_id, user_name in zip(user_ids, user_names):
        print(f"{user_name}:")
        _map = {"nodes": [], "links": []}
        _map["nodes"], _ = getUserFollowings(API, _map["nodes"], user_id)
        _map["links"] = API.getLinks(_map["nodes"])
        print("\nFinished Links for: " + user_name)
        _map["nodes"] = refactorFollowers(_map["nodes"], 0.000001)
        _map["links"] = removeNonMutuals(_map["links"])
        save(user_name, _map)
        print(f"User id: {user_name} has been completed")
    
    print("All your raw data has been succesfully farmed")
        


if __name__ == "__main__":
    main()
    
    
