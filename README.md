# Twitter-Map

This software allows the user to create maps of Twitter accounts.

<h3>Installation</h3>

`git clone git@github.com:OGreenwood672/Twitter-Map.git`

`cd Twitter-Map`

`npm install`

`pip install python-decouple requests`

<h3>To create new map:</h3>

IMPORTANT:

To create a map you will need a unique Twitter API token

you can get a Twitter API token here: https://twitter.com/login?redirect_after_login=https%3A%2F%2Fdeveloper.twitter.com%2Fapp%2Fnew

Once you have a Twitter API token, place a '.env' file in the main folder and add:

`TWITTER_BEARER_TOKEN=<TOKEN>`

TWITTER-ID:

To find the user's Twitter id, enter their handle at this website: https://tweeterid.com/

TIMING:

The Twitter API, sadly limits the number of requests. This means that loading an account can take a long time. 
The API allows 15 requests every 15 minutes. For a good idea of timeing:

number_of_people_the_user_follows + 1 < minutes_left < number_of_people_the_user_follows * 3 + 1

The error margin all depends on how many people the people the user follows follows. (No, it's not a typo)

`python3 ./Scrape_Data/main.py --name <name_of_map> --twitter-id <twitter_id> [optional --collect-only-verified <bool> --remove-non-mutual <bool>]`

<h3>To display map:</h3>

`npm run show <map_name> [optional <mode: ("3D" | "2D")>]`

<h3>Example Maps:</h3>

<h4>Entire Twitter Map</h4>

This example map has used the twitter verified account to get all the accounts which are verified and over 2,000,000 followers.
This allows you to see Twitter's major communities and see how they all interconnect.

To run the example your self, use the command:

`npm run show Twitter`

or have a look at this already served version:

https://ogreenwood672.github.io/algorithms/#/twitter/verified/2d

![communities_twitter](https://user-images.githubusercontent.com/22611951/131020634-951c329d-cb63-486a-917a-1959c5a1592b.png)

<h4>Elon Musk's Account</h4>

This is a much smaller account but still is able to show you the communities that Elon Musk follows


To run the example your self, use the command:

`npm run show ElonMusk`

or have a look at this already served version:

https://ogreenwood672.github.io/algorithms/#/twitter/elonMusk/2d

![image](https://user-images.githubusercontent.com/22611951/130952310-7dd1d84f-fc0a-4104-9cab-9acc9801f0b7.png)

# Issues

If you would like to suggest any improvements, fix any issues or clean the code, you can:

 - Post an issue in the issues tab in github
 - Message me on Discord at: Greenwood#6835

