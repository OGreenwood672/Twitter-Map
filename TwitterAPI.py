import requests
import requests_oauthlib
import os
import json
import time
import sys

class TwitterAPI:
    def __init__(self, bearer_token, filterPeople):
        self.bearer_token = bearer_token
        self.filterPeople = filterPeople
    
    def isValidUser(self, user):
        return user["verified"] and user["public_metrics"]["followers_count"] > 500000
    
    def create_usr_dict(self, usr):
        return {
            "id": usr["id"],
            "username": usr["username"],
            "name": usr["name"],
            "followers": usr["public_metrics"]["followers_count"]
        }
            

    def create_url(self, usr_id):
        return f"https://api.twitter.com/2/users/{usr_id}/following"
    
    def get_params(self, pagination_token=None):
        params = {"user.fields": "id,verified,public_metrics", "max_results": "1000"}
        if (pagination_token != None):
            params["pagination_token"] = pagination_token
        return params


    def bearer_oauth(self, r):

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2FollowingLookupPython"
        return r
    
    def connect_to_endpoint(self, url, params):
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

    def getFollowings(self, data, usr_id, pagination_token=None):
        url = self.create_url(usr_id)
        params = self.get_params(pagination_token)
        response_json = self.connect_to_endpoint(url, params)
        if "data" in response_json: 
            for user in response_json["data"]:
                if not self.filterPeople or self.isValidUser(user):
                    data.append(self.create_usr_dict(user))
            if ("next_token" in response_json["meta"]):
                return data, response_json["meta"]["next_token"]
        return data, None
    
    def getLinks(self, nodes):
        ids = list(map(lambda x: x["id"], nodes))
        links = []
        for i in range(len(ids)):
            length = 50
            dots = round((i+1)/len(ids) * 50)
            space = length - dots
            sys.stdout.write("\r" + f"[{'.' * dots}{' ' * space}]")
            id = ids[i]
            individual_followings = []
            next_token = None
            for _ in range(3):
                individual_followings, next_token = self.getFollowings(individual_followings, id, pagination_token=next_token)
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


if __name__ == "__main__":
    create_map = TwitterAPI()
    next_token = True
    while next_token != None:
        DATA["nodes"], next_token = create_map.getVerifiedFollowings(DATA["nodes"], verified_id, max_followers=1000, pagination_token=next_token)
    create_map.getLinks(DATA)
    save()
