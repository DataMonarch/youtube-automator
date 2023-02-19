import json
import toml
import pandas as pd
import numpy as np
import os
import moviepy.editor as mp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ColorClip

with open('../configs/yt_config.toml') as f:
    config = toml.load(f)
    SHORT_VIDEO_LENTGTH = config["video_processing"]["video_len"]


with open("../data/videos/scraped_videos.json") as f:
    videos_dict = json.load(f)


def get_trimmed_video_srt(video_id: str, start_time: float) -> pd.DataFrame:
    video_dict = videos_dict[video_id]    

    srt_df = pd.DataFrame(video_dict["captions"])

    if not start_time:
        frame_start_list = srt_df[srt_df["start"] < srt_df.loc[srt_df.index[-1], "start"] - SHORT_VIDEO_LENTGTH]['start'].values
        start_time = np.random.choice(frame_start_list)

    trimmed_video_srt = srt_df[(srt_df["start"] >= start_time) & (srt_df["start"] <= start_time + SHORT_VIDEO_LENTGTH)]
    return trimmed_video_srt


def change_aspect_ratio(video: VideoFileClip, new_aspect_ratio: float = 9/16):
    # Determine the aspect ratio of the input video
    curr_aspect_ratio = video.aspect_ratio
        
    # If the aspect ratio is greater than the indicated ratio (e.g. 9:16 portrait), add black bars to the top and bottom
    if curr_aspect_ratio > new_aspect_ratio: # reverse as in MP aspect ratio is width / height
        video = video.resize(0.5)
        width, height = video.size
        
        bar_height = int((int(width * (1 / new_aspect_ratio)) - height) / 2)
        video = video.margin(left=0, right=0, top=bar_height, bottom=bar_height)
        
        # subclip = subclip.set_duration(subclip.duration)
        return video


def get_video_clip(video_id: str, start_time: float =None):
    
    trimmed_video_srt = get_trimmed_video_srt(video_id, start_time)
    print(">> generated SRT for the clip")
    
    start_time, end_time = trimmed_video_srt.iloc[0]["start"], trimmed_video_srt.iloc[-1]["start"]
    
    # create a VideoFileClip object
    video_path = videos_dict[video_id]["file_path"]
    video = VideoFileClip(video_path)   
    print(type(video)) 

    # set the start and end time
    subclip = video.subclip(start_time, end_time)
    
    
    
    # check for the existence of the output directory
    output_dir = "../data/videos/output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # set the output path
    output_path = os.path.join(output_dir, video_id + str(start_time) + ".mp4")  
    
    # extract the trimmed video and preserve the audio
    subclip.write_videofile(output_path, audio=True)
    
    print(f">>> A new video clip is created: {output_path}")
    
    
get_video_clip("iMyB_8eWfak")