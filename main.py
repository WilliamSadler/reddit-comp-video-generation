import json
import random, os, glob, time, shutil
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

#Grab clips from a given text file up to the minimum video length given in the config file.
def grab_clips(filepath, config):
    try:
        shutil.rmtree('./temp/clips')
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

    os.mkdir('./temp/clips')

    target_video_length = config["target_video_length"]
    current_video_length = 0

    for i in range(0, 5):
        random_clip = random_line(filepath)
        download_reddit_video(random_clip, config)

def render_by_ffmpeg():
    print(os.getcwd())

    try:
        shutil.rmtree('./temp/scaled')
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

    try:
        shutil.rmtree('./temp/intermediate')
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    
    os.mkdir('./temp/scaled')
    os.mkdir('./temp/intermediate')

    clips = []

    for f in glob.glob(os.getcwd() + "/temp/clips/*.mp4"):
        print(f.split("\\")[-1])
        clips.append(f.split("\\")[-1])

    for c in clips:
        os.system('ffmpeg -i ./temp/clips/'+c+' -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1" ./temp/scaled/'+c+'.mp4')
    
    clips=[]
    for f in glob.glob(os.getcwd() + "/temp/scaled/*.mp4"):
        print(f.split("\\")[-1])
        clips.append(f.split("\\")[-1])

    for c in clips:
        os.system('ffmpeg -i ./temp/scaled/'+c+ ' -c copy -bsf:v h264_mp4toannexb -f mpegts ./temp/intermediate/bruh'+c.split('.')[0]+'.ts')

    clips_file = open("./temp/clips.txt", "w")

    for f in glob.glob(os.getcwd() + "./temp/intermediate/*.ts"):
        clips_file.write("file '"+ f.split("/")[-1] + "'\n")

    clips_file.close()

    print('ffmpeg -f concat -safe 0 -i ./temp/clips.txt -c copy -bsf:a aac_adtstoasc ./renders/output.mp4')
    os.system('ffmpeg -f concat -safe 0 -i ./temp/clips.txt -c copy -bsf:a aac_adtstoasc ./renders/output.mp4')

    print("pog")
    
    for f in glob.glob(os.getcwd() + "/*.ts"):
        os.remove(f)

#Grab the values from a configuration file
def get_config(path):
    with open(path) as json_file:
        data = json.load(json_file)

    return data

if __name__ == "__main__":
    config = get_config("example-config.json")
    grab_clips(os.getcwd() + "./clips.txt", config)

    #TODO: Fix absolute -> relative path
    os.chdir("D://YouTube//Reddit Compilations//Bots//reddit-comp-video-generation//reddit-comp-video-generation")
    render_by_ffmpeg()
