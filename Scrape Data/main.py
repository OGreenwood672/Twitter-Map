from collections import defaultdict
from decouple import Undefined, UndefinedValueError, config
import json
import os

from TwitterAPI import TwitterAPI

from edit_raw_data import edit

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

def checkForFile(input_file):
    if os.path.exists(input_file):
        return True
    print("Please create file 'peopleToScrape'\nFill file with '<name>=<user_id>'\nE.g. ElonMusk=44196397")

def getIds(input_file):
    with open(input_file, "r") as f:
        return list(map(int, [line.split("=")[1] for line in f.read().split("\n")]))

def getNames(input_file):
    with open(input_file, "r") as f:
        return [line.split("=")[0] for line in f.read().split("\n")]

def main():
    try:
        API = TwitterAPI(config("TWITTER_BEARER_TOKEN"), True)
    except UndefinedValueError:
        print("Please create config file with TWITTER_BEARER_TOKEN")

    input_file = "./peopleToScrape.txt"
    checkForFile(input_file)

    user_ids = getIds(input_file)
    user_names = getNames(input_file)
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

    for user_name in user_names:
        edit(user_name)
        


if __name__ == "__main__":
    main()
    
    
