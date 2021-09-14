# Reddit to Youtube
Reddit to Youtube is a small project with the intent to be able to upload content from a subreddit directly to youtube.
The script takes a subreddit, takes the first 25 posts in the "hot" section of the subreddit, and uploads any videos 
found directly to youtube. The first time when you run the program you are asked to log in into youtube, after that it
will automatically be able to log you in from the cookies of the browser.

## Requirements

The program uses the following:
`praw`, `os`, `argparse`, `json`, `redvid` and `youtube_uploader_selenium`

Make sure to install all of them in order to be able to run it. On top of that, `redvid` itself uses `FFmpeg` for video
downloading. This can be installed on your own OS (refer to How downloading works chapter).

## Usage
First clone the project somewhere:

`git clone https://github.com/isvora/reddit-to-youtube.git`

Then, you have to go into `constants\Credentials.py` and replace the api keys with your own api key from your reddit app.
Refer to the next chapter on how to create a reddit app.

Then, you can run the script like in the example below

`python RedditToYoutube.py --subreddit "leagueoflegends" --submissions 10`

This will take the subreddit /r/leagueoflegends, it will look through the first 10 submission in the 'hot' section and, 
if any of them are videos, it will download the video to your disk, upload it to youtube and then delete it from the
disk.

## How to setup a reddit application
You need to have a reddit account for this, if you don't have one create one first.

Then go to: https://ssl.reddit.com/prefs/apps/

At the bottom you will have the "create another app..." button

Put the name to whatever you desire, this will be used as the `user_agent` in the `Credentials.py` file

Select 'script' on the app type

Leave about url empty

Put `http://www.example.com/unused/redirect/uri` in the redirect uri

Once the app is created, under the name you will find the personal use script, this goes into `client_id`

Below you will find the 'secret' field, that will go under `client_secret`

That's it!

## How downloading works
Downloading works thanks to an existing library already made called redvid: https://github.com/elmoiv/redvid
For this library you need `requests` and `FFmpeg`. There's a tutorial for windows/linux in the redvid repository showing
you how to get FFmpeg working.

## How uploading works
Uploading works via selenium thanks to an open source project that can be found here: https://github.com/linouk23/youtube_uploader_selenium
