from collections import defaultdict
from typing import List
from decouple import UndefinedValueError, config
import json
import os
import argparse
from typing import Dict, List, Tuple

from TwitterAPI import TwitterAPI

from edit_raw_data import edit

def remove_non_mutuals(links: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """ Function remove_non_mutuals
    
    @params
    links: list of dictionaries of all sources and targets of node

    This function takes all sources and targets and removes and links which aren't shared
    ie The only links which will remain are ones which are mutuals.
    (duplicates are removed)
    
    """


    dic = defaultdict(list)
    mutuals = []
    for link in links:
        dic[link["source"]].append(link["target"])
    for link in links:
        if link["source"] in dic[link["target"]]:
            mutuals.append(link)
            dic[link["source"]].remove(link["target"])
    return mutuals


def save(folder_name: str, DATA: Dict) -> None:
    """ Function: save

    @params
    folder_name: The name of the folder the maps are saved to.
    DATA: the nodes and link to save
    
    """

    new_folder_path = f"./public/Maps/{folder_name}"#os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), folderName)
    
    try:
        os.remove(new_folder_path)
    except:
        pass

    os.mkdir(new_folder_path)
    with open(f"./public/Maps/{folder_name}/TwitterMapRaw.json", "w") as f:
        json.dump(DATA, f, indent=4)


def refactor_followers(nodes: List[Dict], scale: float) -> List[Dict]:
    """ Function: refactor_followers

    @params
    nodes: All the nodes of the map
    scale: The number to multiply the current followers by so he nodes can fit in the map

    The function changes all of the followers by scale so that they can fit on the map.

    """

    for node in nodes:
        node["followers"] *= scale
    return nodes

def get_user_followings(API: TwitterAPI, nodes: List[Dict], user_id: int, next_token=None) -> Tuple[List[Dict], int]:
    """ Function : get_user_followings

    @params
    API: Your Twitter API instance, with auth set up,
    nodes: Already collected nodes of map,
    user_id: id of user,
    next_token: next page token of the followings list
    
    The function is setup as recursive and collects all followers, regardless of number of pages
    
    """

    nodes, next_token = API.getFollowings(nodes, user_id, pagination_token=next_token)
    if next_token != None:
        nodes, next_token = get_user_followings(API, nodes, user_id, next_token)
    return nodes, next_token

def get_args():
    """ Function : get_args

    parameters used in .add_argument
    1. metavar - Provide a hint to the user about the data type.
    - By default, all arguments are strings.

    2. type - The actual Python data type

    3. help - A brief description of the parameter for the usage

    4. default - (optional) If no argument is passed, the default is used.
    """

    parser = argparse.ArgumentParser(
        description='Arguments for names and id of ',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    #name of user
    parser.add_argument('--name',
        metavar='name',
        type=str,
        help='Name of user'
    )
    #Twitter Id of user
    parser.add_argument('--twitter_id',
        metavar='twitter_id',
        type=int,
        help='Twitter Id of user'
    )
    #Collect only verified people who have 2+ million followers
    parser.add_argument('--collect_only_verified',
        metavar='collect_only_verified',
        type=bool,
        help='Collect only verified people who have 2+ million followers',
        default=False
    )

    return parser.parse_args()

def main():

    args = get_args()
    
    #Create the twitter api instance with the auth token from a .env file
    try:
        API = TwitterAPI(config("TWITTER_BEARER_TOKEN"), args.collect_only_verified)
    except UndefinedValueError:
        print("Please create config file with TWITTER_BEARER_TOKEN")
        raise AssertionError

    print(f"{args.name}:")
    _map = {"nodes": [], "links": []} # Initialize empty map
    _map["nodes"], _ = get_user_followings(API, _map["nodes"], args.twitter_id) # Collect all followers as nodes
    _map["links"] = API.get_links(_map["nodes"]) # Collect links inbetween nodes
    print("\nFinished Links for: " + args.name)
    _map["links"] = remove_non_mutuals(_map["links"])
    save(args.name, _map)
    print(f"User id: {args.name} has been completed")
    
    edit(args.name)
        


if __name__ == "__main__":
    main()