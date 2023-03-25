import json
import toml
import pandas as pd
import numpy as np
import os
import moviepy.editor as mp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import clips_array
from .editor import change_aspect_ratio, add_image, add_self_as_bg


def time_stamp_to_sec(time_stamp: str) -> float:
    time_stamp = time_stamp.split(".")
    if len(time_stamp) == 1:
        time_stamp = ["0", "0"] + time_stamp
    elif len(time_stamp) == 2:
        time_stamp = ["0"] + time_stamp
    
    h, m, s = [int(i) for i in time_stamp]
    return h * 3600.0 + m * 60.0 + s
    

with open('../configs/yt_config.toml') as f:
    config = toml.load(f)
    SHORT_VIDEO_LENTGTH = config["video_processing"]["video_len"]



def get_trimmed_video_srt(videos_dict: dict, video_id: str, start_time: str, end_time: str) -> pd.DataFrame:
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
        try:
            end_time = srt_df[srt_df["start"] >= end_time]["start"].values[0]
        except IndexError:
            end_time = srt_df["start"].values[-1]
        
    print(f"Start and end times: {start_time} - {end_time}")
    
    trimmed_video_srt = srt_df[(srt_df["start"] >= start_time) & (srt_df["start"] <= end_time)]
    
    # add a new row with the full text of the caption
    full_text = trimmed_video_srt["text"].str.cat(sep=" ")
    trimmed_video_srt = trimmed_video_srt.append({"start": start_time, "duration": end_time - start_time, "text": full_text}, ignore_index=True)
    
    
    return trimmed_video_srt


def add_captions(video_clip: VideoFileClip, trimmed_video_srt: pd.DataFrame):
    caption_clips = []
    trimmed_video_srt.reset_index(inplace=True)
    clip_end = video_clip.end
    audio = video_clip.audio
    
    initial_start_time = trimmed_video_srt.iloc[0]['start']
    for i in range(0, len(trimmed_video_srt)-1):
        # end_prev_caption = trimmed_video_srt.iloc[i-1]['start'] - initial_start_time + trimmed_video_srt.iloc[i-1]['duration']
        start_curr_caption = trimmed_video_srt.iloc[i]['start'] - initial_start_time
        # end_curr_caption = start_curr_caption + trimmed_video_srt.iloc[i]['duration']
        # start_next_caption = trimmed_video_srt.iloc[i+1]['start'] - initial_start_time
        if i < len(trimmed_video_srt) - 2:
            end_curr_caption = trimmed_video_srt.iloc[i+1]['start'] - initial_start_time
        else:
            end_curr_caption = start_curr_caption + trimmed_video_srt.iloc[i]['duration']
        
        text = trimmed_video_srt.iloc[i]['text']
        
        # if end_curr_caption > start_next_caption:
        #     text += trimmed_video_srt.iloc[i+1]['text']            
        
        video_width, video_height = video_clip.size
        width = int(0.8*video_width)
        # height = 0
        
        caption_clip = mp.TextClip(text, fontsize=32, color='black', bg_color='gold', method="caption", size=(width, None), font="Arial-Bold", 
                                   align="South", transparent=True).set_start(start_curr_caption).set_end(end_curr_caption)
        caption_clip = caption_clip.set_position(("center", 0.75*video_height))
        
        # caption_clips.append(caption_clip)
        # print(f"INFO: caption {i} set. Start time: {start_curr_caption}")
        video_clip = mp.CompositeVideoClip([video_clip, caption_clip], use_bgclip=True, size=video_clip.size).set_duration(video_clip.duration)
    # captions = clips_array([caption_clips], bg_color="transparent")
    # composite_clip = mp.CompositeVideoClip([video_clip, captions.set_pos(("center", "bottom"))], use_bgclip=True, size=video_clip.size).set_duration(video_clip.duration)
    
    # add audio to the video
    video_clip = video_clip.set_audio(audio)
    
    return video_clip

def get_video_clip(video_id: str, start_time: str=None, end_time: str=None):
    
    file_name = video_id + '-' + str(start_time)
    output_dir = os.path.join("../data/videos/output", file_name)
    
    
    with open("../data/videos/scraped_videos.json") as f:
        videos_dict = json.load(f)
    
    trimmed_video_srt = get_trimmed_video_srt(videos_dict, video_id, start_time, end_time)
    print(">> generated SRT for the clip")
    # print(trimmed_video_srt)
    
    
    start_time, end_time = trimmed_video_srt.iloc[0]["start"], trimmed_video_srt.iloc[-2]["start"]
    
    # create a VideoFileClip object
    video_path = videos_dict[video_id]["file_path"]
    video = VideoFileClip(video_path)   

    # set the start and end time
    subclip = video.subclip(start_time, end_time)
    subclip = change_aspect_ratio(subclip)
    subclip = add_image(subclip, scaling_factor=0.275)
    # subclip = crop_to_aspect_ratio(subclip)
    # subclip = add_gaussian_blur(subclip, 10)

    # subclip = add_logo_cv2(subclip, scaling_factor=0.275)
    
    # subclip = add_captions(subclip, trimmed_video_srt)
    
    # check for the existence of the output directory
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # set the output path
    output_path = os.path.join(output_dir, file_name + ".mp4")  
    
    # extract the trimmed video and preserve the audio
    subclip.write_videofile(output_path, audio=True, audio_codec="aac", codec="libx264", preset="ultrafast", threads=4, verbose=False)
    
    # save the srt file in the output directory
    csv_filename = os.path.join(output_dir, file_name + ".csv")
    trimmed_video_srt.to_csv(csv_filename, index=False)
    
    print(f">>> A new video clip is created: {output_path}")
    
    
# get_video_clip("QIz15aJR3Mw", start_time = "4.14", end_time="5.05")

