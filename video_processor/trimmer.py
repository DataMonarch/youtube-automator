import json
import toml
import pandas as pd
import numpy as np
import os
import moviepy.editor as mp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import clips_array
from editor import change_aspect_ratio
import math


def time_stamp_to_sec(time_stamp: float) -> float:
    minutes = math.floor(time_stamp)
    seconds = (time_stamp - minutes) * 60.0
    
    return minutes * 60.0 + seconds

with open('../configs/yt_config.toml') as f:
    config = toml.load(f)
    SHORT_VIDEO_LENTGTH = config["video_processing"]["video_len"]


with open("../data/videos/scraped_videos.json") as f:
    videos_dict = json.load(f)


def get_trimmed_video_srt(video_id: str, start_time: float, end_time: float) -> pd.DataFrame:
    video_dict = videos_dict[video_id]    

    srt_df = pd.DataFrame(video_dict["captions"])
    
    if not start_time:
        frame_start_list = srt_df[srt_df["start"] < srt_df.loc[srt_df.index[-1], "start"] - SHORT_VIDEO_LENTGTH]['start'].values
        start_time = np.random.choice(frame_start_list)
    else:
        start_time = time_stamp_to_sec(start_time)
        
    if not end_time:
        end_time = start_time + SHORT_VIDEO_LENTGTH
    else:
        end_time = time_stamp_to_sec(end_time)
        end_time = srt_df[srt_df["start"] >= end_time]["start"].values[0]
        
    print(f"Start and end times: {start_time} - {end_time}")
    
    trimmed_video_srt = srt_df[(srt_df["start"] >= start_time) & (srt_df["start"] <= end_time)]
    
    return trimmed_video_srt


def add_captions(video_clip: VideoFileClip, trimmed_video_srt: pd.DataFrame):
    caption_clips = []
    trimmed_video_srt.reset_index(inplace=True)
    clip_end = video_clip.end
    
    initial_start_time = trimmed_video_srt.iloc[0]['start']
    for i in range(1, len(trimmed_video_srt)-1):
        end_prev_caption = trimmed_video_srt.iloc[i-1]['start'] - initial_start_time + trimmed_video_srt.iloc[i-1]['duration']
        start_curr_caption = trimmed_video_srt.iloc[i]['start'] - initial_start_time
        # end_curr_caption = start_curr_caption + trimmed_video_srt.iloc[i]['duration']
        start_next_caption = trimmed_video_srt.iloc[i+1]['start'] - initial_start_time
        end_curr_caption = start_curr_caption + trimmed_video_srt.iloc[i]['duration']
        
        text = ""
        
        # if start_curr_caption < end_prev_caption:
        #     text += trimmed_video_srt.iloc[i-1]['text']
            
        text += " " + trimmed_video_srt.iloc[i]['text']
        
        # if end_curr_caption > start_next_caption:
        #     text += trimmed_video_srt.iloc[i+1]['text']            
        
        # print(f"text's length: {len(text)}")
        caption_clip = mp.TextClip(text, fontsize=23, color='black', method="caption", size=video_clip.size, align="South", bg_color='white', transparent=False).set_start(start_curr_caption).set_end(end_curr_caption)
        print(caption_clip.size)
        caption_clips.append(caption_clip)
        # print(f"INFO: caption {i} set. Start time: {start_curr_caption}")
        
    print(len(caption_clips))
    captions = clips_array([caption_clips], bg_color="transparent")
    composite_clip = mp.CompositeVideoClip([video_clip, captions.set_pos(("center", "bottom"))], use_bgclip=True, size=video_clip.size).set_duration(video_clip.duration)
    
    return composite_clip

def get_video_clip(video_id: str, start_time: float=None, end_time: float=None):
        
    trimmed_video_srt = get_trimmed_video_srt(video_id, start_time, end_time)
    print(">> generated SRT for the clip")
    
    start_time, end_time = trimmed_video_srt.iloc[0]["start"], trimmed_video_srt.iloc[-1]["start"]
    
    # create a VideoFileClip object
    video_path = videos_dict[video_id]["file_path"]
    video = VideoFileClip(video_path)   

    # set the start and end time
    subclip = video.subclip(start_time, end_time)
    subclip = change_aspect_ratio(subclip)
    # subclip = add_captions(subclip, trimmed_video_srt)
    
    # check for the existence of the output directory
    output_dir = os.path.join("../data/videos/output", video_id + str(start_time))
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # set the output path
    output_path = os.path.join(output_dir, video_id + str(start_time) + ".mp4")  
    
    # extract the trimmed video and preserve the audio
    subclip.write_videofile(output_path, audio=True)
    
    # save the srt file in the output directory
    csv_filename = os.path.join(output_dir, video_id + str(start_time) + ".csv")
    trimmed_video_srt.to_csv(csv_filename, index=False)
    
    print(f">>> A new video clip is created: {output_path}")
    
    
get_video_clip("vIeFt88Hm8s", start_time = 30.18, end_time=30.51)

