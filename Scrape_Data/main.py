from collections import defaultdict
from decouple import UndefinedValueError, config
import json
import os
import argparse
import re

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
    newFolderPath = f"../public/Maps/{folderName}"#os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), folderName)
    try:
        os.remove(newFolderPath)
    except:
        pass
    os.mkdir(newFolderPath)
    with open(f"../public/Maps/{folderName}/TwitterMapRaw.json", "w") as f:
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

def get_args():
    """ Function : get_args
    parameters used in .add_argument
    1. metavar - Provide a hint to the user about the data type.
    - By default, all arguments are strings.

    2. type - The actual Python data type
    - (note the lack of quotes around str)

    3. help - A brief description of the parameter for the usage

    """

    parser = argparse.ArgumentParser(
        description='Arguments for names and id of ',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Adding our first argument player name of type string
    parser.add_argument('--name',
        metavar='name',
        type=str,
        help='Name of user'
    )
    parser.add_argument('--twitter_id',
        metavar='twitter_id',
        type=int,
        help='Twitter Id of user'
    )
    parser.add_argument('--collect_only_verified',
        metavar='collect_only_verified',
        type=bool,
        help='Collect only verified people who have 2+ million followers',
        default=False
    )

    return parser.parse_args()

def main():

    args = get_args()
    
    try:
        API = TwitterAPI(config("TWITTER_BEARER_TOKEN"), args.collect_only_verified)
    except UndefinedValueError:
        print("Please create config file with TWITTER_BEARER_TOKEN")
        raise AssertionError

    return

    print(f"{args.name}:")
    _map = {"nodes": [], "links": []}
    _map["nodes"], _ = getUserFollowings(API, _map["nodes"], args.twitter_id)
    _map["links"] = API.getLinks(_map["nodes"])
    print("\nFinished Links for: " + args.name)
    _map["nodes"] = refactorFollowers(_map["nodes"], 0.000001)
    _map["links"] = removeNonMutuals(_map["links"])
    save(args.name, _map)
    print(f"User id: {args.name} has been completed")
    
    edit(args.name)
        


if __name__ == "__main__":
    main()
    
    
