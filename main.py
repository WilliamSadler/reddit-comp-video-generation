import json
import random, os, glob, time
from redvid import Downloader
import random

#Grab a random line from the given text file
def random_line(fname):
    lines = open(fname).read().splitlines()
    return random.choice(lines)

#Downloads the reddit a reddit video to the temporary clip folder.
def download_reddit_video(url, config):
    clip_length_limit = config["clip_length_limit"]

    reddit = Downloader(max_q=True)
    reddit.path = os.getcwd() + "/temp/clips/"
    reddit.url = url

    reddit.check()
    if reddit.duration <= clip_length_limit:
        reddit.download()
        #clips_string = clips_string + url + "\n"
    else:
        print('Duration > 20 seconds')

def get_config(path):
    with open(path) as json_file:
        data = json.load(json_file)

    return data

if __name__ == "__main__":
    config = get_config("example-config.json")

    download_reddit_video("https://www.reddit.com/r/perfectlycutscreams/comments/auyisc/asmr_in_the_kitchen/", config)
