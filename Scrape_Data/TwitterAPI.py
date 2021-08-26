import requests
import time
import sys
from typing import Dict, List, Tuple

class TwitterAPI:

    """
    Controls the interaction between the program and the twitter api
    """

    def __init__(self, bearer_token: str, filter_people: bool):
        """
        @params
        bearer_token: unique token required to use twitter api
        filter_people: Automatically removes any people who don't match requirements
        """
        self.bearer_token = bearer_token
        self.filter_people = filter_people
    
    def is_valid_user(self, user: Dict):
        """ Function: is_valid_user
        @params
        user: info of user, including name, username, id, followers

        Checks if user meets requirements
        REQUIREMENTS:
        user.followers > 500,000
        user.verified == True
        """

        return user["verified"] and user["public_metrics"]["followers_count"] > 500000
    
    def create_usr_dict(self, usr: Dict):
        """ Fucntion: create_usr_dict
        @params
        usr: Full user info from twitter api

        Creates a user object with specifically neeeded info
        """

        return {
            "id": usr["id"],
            "username": usr["username"],
            "name": usr["name"],
            "followers": usr["public_metrics"]["followers_count"]
        }
            

    def create_url(self, usr_id: int) -> str:
        """ Function: create_url
        @params
        usr_id: id of user

        gets the endpoint of the twitter api
        """
        return f"https://api.twitter.com/2/users/{usr_id}/following"
    
    def get_params(self, pagination_token: (str or None) = None) -> Dict:
        """ Function: get_params
        @params
        pagination_token: token for next page of requests (1000 people per request)

        Creates a dictionary of all parameters for the twitter api, ready for request
        """
        params = {"user.fields": "id,verified,public_metrics", "max_results": "1000"}
        if (pagination_token != None):
            params["pagination_token"] = pagination_token
        return params


    def bearer_oauth(self, r):
        """ Function: bearer_oauth
        @params
        r: No idea????? TODO

        Copy and pasted from Twitter Api docs
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2FollowingLookupPython"
        return r

    def connect_to_endpoint(self, url: str, params: Dict) -> Dict:
        """ Function: connect_to_endpoint
        @params
        url: url of endpoint (see create_url)
        params: parameters of request (see get_params)
        """
        while True:
            try:
                response = requests.request("GET", url, auth=self.bearer_oauth, params=params)
                if response.status_code != 200:
                    time.sleep(910)
                else:
                    return response.json()
            except Exception as e:
                print(e)
                return {}

    def get_followings(self, data: Dict, usr_id: int, pagination_token: (str or None)=None) -> Tuple[Dict, (str or None)]:
        """ Function get_following
        @params
        data: entire data so far
        usr_id: id of user
        pagination_token: token of next page of requests

        Function that handles retrieving all the people the user followers
        """
        url: str = self.create_url(usr_id)
        params: Dict = self.get_params(pagination_token)
        response_json = self.connect_to_endpoint(url, params)
        if "data" in response_json: 
            for user in response_json["data"]:
                if not self.filter_people or self.is_valid_user(user):
                    data.append(self.create_usr_dict(user))
            if ("next_token" in response_json["meta"]):
                return data, response_json["meta"]["next_token"]
        return data, None
    
    def get_links(self, nodes: List[Dict]) -> Dict[str, str]:
        """ Function: get_links
        @params
        nodes: List of all nodes (people who the user follows)

        Function that gets all the links inbetween the people the user follows
        """
        ids: List = list(map(lambda x: x["id"], nodes))
        links: List = []
        for i in range(len(ids)):
            length: int = 50
            dots: float = round((i+1)/len(ids) * 50)
            space: int = length - dots
            sys.stdout.write("\r" + f"[{'.' * dots}{' ' * space}]")
            id: int = ids[i]
            individual_followings: List = []
            next_token: (str or None) = None
            for _ in range(3):
                individual_followings, next_token = self.get_followings(individual_followings, id, pagination_token=next_token)
                if (next_token == None):
                    break
            for user in map(lambda x: x["id"], individual_followings):
                if user in ids and user != id:
                    links.append({
                        "source": id,
                        "target": user
                    })
            sys.stdout.flush()
        return links