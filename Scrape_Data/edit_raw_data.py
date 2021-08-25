import json
from typing import Dict, List

def set_min_followers(data: Dict[List, List], min_followers: int) -> Dict[List, List]:
    """ Function set_min_followers

    @params
    data: Entire dataset of Twitter Map
    followers: minimum amount of followers to survive the PURGE

    Function removes all nodes and links which don't match required min followers
    """
    
    removedIds = [user["id"] for user in data["nodes"] if user["followers"] < min_followers]
    data["nodes"] = list(filter(lambda x: x["followers"] >= min_followers, data["nodes"]))
    data["links"] = list(filter(lambda x: not (x["source"] in removedIds or x["target"] in removedIds), data["links"]))

    return data

def remove_solos(data: Dict[List, List]) -> List[Dict]:
    """ Function remove_solos

    @params
    data: Entire dataset of Twitter Map

    Function removes nodes which don't share any links with anyone else
    """

    sources = list(map(lambda x: x["source"], data["links"]))
    targets = list(map(lambda x: x["target"], data["links"]))
    data["nodes"] = list(filter(lambda x: (x["id"] in sources or x["id"] in targets), data["nodes"]))

    return data["nodes"]


def shrink(links: List[Dict], chance_of_removal: int) -> List[Dict]:
    """Function shrink
    
    @params
    links: Entire set of links from the dataset
    chance_of_removal: Inversly proportional to chance of removal TODO Need better name (also change name of line 71 (same name issue))

    For large set of data, this function removes links to reduce lag
    """
    
    new_links = []
    for index, link in enumerate(links):
        if index % chance_of_removal == 0:
            new_links.append(link)
    
    return new_links


def edit(nameOfFolder: str):
    """ Function edit
    
    @params
    nameOfFolder: folder to save the map in

    This function allows the user to select edit options.
    """

    with open(f"./public/Maps/{nameOfFolder}/TwitterMapRaw.json", "r") as f:
        data = json.load(f)

    print(f"Editing data of {nameOfFolder}:")

    if "y" in input("    Would you like to shrink number of links (recommended for graphs above 750 nodes) (y/N)"):
        print("    Shrinking nodes to fit screen...")
        while not (chance_of_removal := input("  What is your chance of removal 1/x: ").isdigit()):
            print("    That is not a valid number")
        data["links"] = shrink(data["links"], chance_of_removal)
    
    if "y" in input("    Would you like to set a minimum followers for nodes (y/N)"):
        while not (min_followers := input("  What is your minimum followers required for node on map: ").isdigit()):
            print("    That is not a valid number")
        data = set_min_followers(data, min_followers / 1000000)
    
    if "y" in input("   Would you like to remove the nodes who don't connect with anyone (y/N)"):
        data["nodes"] = remove_solos(data)

    with open(f"./public/{nameOfFolder}/TwitterMap.json", "w") as f:
        json.dump(data, f, indent=4)