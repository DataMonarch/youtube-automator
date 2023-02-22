from video_processor import trimmer
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-vid", "--video_id", help="the id of the video to be trimmed")
parser.add_argument("-c", "--count", help="the number of times the video should be trimmed")
args = parser.parse_args()


video_id = args.video_id
count = int(args.count)

for i in range(count):
    trimmer.get_video_clip(video_id)


# a parser to get the arguments video_id and count from the command line and assign them to variables