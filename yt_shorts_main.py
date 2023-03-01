from video_processor import trimmer
from video_downloader import youtube_downloader
import argparse
import json

import time

start = time.time()

with open("../data/videos/scraped_videos.json", "r") as f:
    available_videos = json.load(f)
    available_video_ids = available_videos.keys()

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--url", help="the url of the video to be trimmed")
parser.add_argument("-s", "--start", help="start time in the format hh.mm.ss", default=None)
parser.add_argument("-e", "--end", help="start time in the format hh.mm.ss", default=None)
parser.add_argument("-vid", "--video_id", help="the id of the video to be trimmed")
parser.add_argument("-c", "--count", help="the number of times the video should be trimmed")
args = parser.parse_args()

if args.url or args.video_id:
    if args.url:
        # extract the youtube video id from the url
        video_id = args.url.split("=")[1]
    elif args.video_id:
        video_id = args.video_id
    else:
        raise ValueError("Please enter a valid url or video id")
    
    
start_time = args.start
end_time = args.end
print(f"end_time: {end_time}")
url = args.url


if not video_id in available_video_ids:
    print(f">>> Video with id {video_id} not found in the available videos list. Downloading now...")
    youtube_downloader.download(url)

if args.count:
    count = int(args.count)
    for i in range(count):
    
        trimmer.get_video_clip(video_id, start_time, end_time)
else:
    trimmer.get_video_clip(video_id, start_time, end_time)
    

print(f">>> Done trimming. Time taken: {time.time() - start} seconds")