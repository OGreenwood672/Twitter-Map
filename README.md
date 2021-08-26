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

TWITTER-ID:

To find the user's Twitter id, enter their handle at this website: https://tweeterid.com/

`python3 ./Scrape_Data/main.py --name <name_of_map> --twitter-id <twitter_id> [optional --collect-only-verified <bool> --remove-non-mutual <bool>]`

<h3>To display map:</h3>

`npm run show <map_name> [optional <mode: ("3D" | "2D")>]`

Example Maps:

`npm run show Twitter`

![image](https://user-images.githubusercontent.com/22611951/130952642-c12918f5-ad6d-4ade-9674-82104768b0f6.png)

`npm run show ElonMusk`

![image](https://user-images.githubusercontent.com/22611951/130952310-7dd1d84f-fc0a-4104-9cab-9acc9801f0b7.png)

# Issues

If you would like to suggest any improvements, fix any issues or clean the code, you can:

 - Post an issue in the issues tab in github
 - Message me on Discord at: Greenwood#6835

