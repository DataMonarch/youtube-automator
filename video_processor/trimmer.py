import json
import toml
import pandas as pd
import numpy as np
import cv2
import os

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
        
    
    # extract a 60 seconds long video clip from the video

    return trimmed_video_srt


def get_video_clip(video_id: str, start_time: float =None):
    
    trimmed_video_srt = get_trimmed_video_srt(video_id, start_time)
    
    start_time, end_time = trimmed_video_srt.iloc[0]["start"], trimmed_video_srt.iloc[-1]["start"]
    
    video_path = videos_dict[video_id]["file_path"]
    
    video = cv2.VideoCapture(video_path) 
  
    # Find the frame rate of the video 
    fps = int(video.get(cv2.CAP_PROP_FPS)) 
    
    # Calculate the start and end frames 
    start_frame = int(start_time * fps)  
    end_frame = int(end_time * fps)  

    # Create an output video file with fourcc codec  
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  

    # Create a VideoWriter object to save the output video file
    output_dir = "../data/videos/output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, video_id + str(start_time) + ".mp4")  
    out = cv2.VideoWriter(output_path, fourcc, fps, (1280, 720))
    # trim the video using cv2 based on the start and end time of the video clip
    
    ret = True
    frame_no = 0
    while ret:
        ret, frame = video.read()  
        
        if ret:
            if frame_no >= start_frame and frame_no <= end_frame:
                out.write(frame)
            
            elif frame_no > end_frame:
                break
    
    video.release()
    print(f">>> A new video clip is created: {output_path}")
    out.release()
    