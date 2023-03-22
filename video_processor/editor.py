
import pandas as pd
import numpy as np
import moviepy.editor as mp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import clips_array
from moviepy.video.VideoClip import VideoClip
import cv2


def add_self_as_bg(video: VideoFileClip, bg_size: tuple,  blur: bool = True) -> VideoFileClip:
    bg_w, bg_h = bg_size
    video_w, video_h = video.size
    
    # To-Do: use ratios to compute the crop size
    # video = video.crop(width = bg_w, height = bg_h, x_center = int(video_w/2), y_center = int(video_h / 2))
    x_start, y_start = (video_w - bg_w) // 2, (video_h - bg_h) // 2
    
    if x_start < 0:
        x_start = 0
        
    if y_start < 0:
        y_start = 0
        
    x_end, y_end = x_start + bg_w, y_start + bg_h
    # if x_end - x > 
    
    video_cropped = video.crop(x1 = x_start, y1 = y_start, 
                       x2 = x_start + bg_w, y2 = y_start + bg_h)
    
    print(f"Video will be cropped to size {bg_w} x {bg_h} starting at ({x_start}, {y_start}) and ending at ({x_end}, {y_end})", )
    
    return video_cropped

def change_aspect_ratio(video: VideoFileClip, new_aspect_ratio: float = 9/16) -> VideoFileClip:
    """Change the aspect ratio of a video.

    Args:
        video (VideoFileClip): The video to be changed.
        new_aspect_ratio (float) : The new aspect ratio of the video. Default is 9/16.

    Returns
        VideoFileClip: The video with the new aspect ratio.
    """
    
    # Determine the aspect ratio of the input video
    curr_aspect_ratio = video.aspect_ratio
        
    # If the aspect ratio is greater than the indicated ratio (e.g. 9:16 portrait), add black bars to the top and bottom
    if curr_aspect_ratio > new_aspect_ratio: # reverse as in MP aspect ratio is width / height
        video_cpy = video.copy()
        
        width, height = video.size
        
        bar_height = int((int(width * (1 / new_aspect_ratio)) - height) / 2)
        video_new_ar = video.margin(left=0, right=0, top=bar_height, bottom=bar_height)
        
        bg_size = video_new_ar.size
        bg_video = add_self_as_bg(video_cpy, bg_size)
        print(f"Size of the bg video: {bg_video.size[0]} x {bg_video.size[1]}")

        return video_new_ar
    
def add_image(video: VideoFileClip, logo_path: str="../data/docs/logo.png",
             x_top_left: int = None, y_top_left: int = None, scaling_factor: float = 0.25):
    """Adds a logo on top of the video.

    Args:
        video (VideoFileClip): original video.
        logo_path (str, optional): path to the logo image. Defaults to "../data/docs/logo.png".
        x_top_left (int, optional): x coordinate of the top left corner of the logo on the video. Defaults to None.
        y_top_left (int, optional): y coordinate of the top left corner of the logo on the video. Defaults to None.
    """
    width, height = video.size
    
    logo = mp.ImageClip(logo_path)
    logo = logo.resize(width=int(width * scaling_factor))
    
    if x_top_left is None:
        x_top_left = (width - logo.size[0]) // 2
    
    if y_top_left is None:
        y_top_left = 170
        
    duration = video.duration
    logo = logo.set_pos((x_top_left, y_top_left)).set_duration(duration)
    final_video = mp.CompositeVideoClip([video, logo])
    
    return final_video
