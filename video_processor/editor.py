
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
        # video = video.resize(0.5)

        width, height = video.size
        
        bar_height = int((int(width * (1 / new_aspect_ratio)) - height) / 2)
        video_new_ar = video.margin(left=0, right=0, top=bar_height, bottom=bar_height)
        
        bg_size = video_new_ar.size
        bg_video = add_self_as_bg(video_cpy, bg_size)
        print(f"Size of the bg video: {bg_video.size[0]} x {bg_video.size[1]}")

        return video_new_ar
    
def crop_to_aspect_ratio(video: VideoFileClip, aspect_ratio: float = 9/16,
                         resize_factor: float = 0.5) -> VideoFileClip:
    video_aspect_ratio = video.w / video.h
    if video_aspect_ratio > aspect_ratio:
        new_width = aspect_ratio * video.h
        x_offset = (video.w - new_width) / 2
        video = video.crop(x1=x_offset, x2=video.w - x_offset)
    else:
        new_height = video.w / aspect_ratio
        y_offset = (video.h - new_height) / 2
        video = video.crop(y1=y_offset, y2=video.h - y_offset)
        
    return video 

def add_gaussian_blur(video: VideoFileClip, blur_size: int = 5) -> VideoFileClip:
    """Adds a Gaussian blur to the video.

    Args:
        video (VideoFileClip): The video to be blurred.
        blur_size (int, optional): The size of the blur. Defaults to 5.

    Returns:
        VideoFileClip: The blurred video.
    """
    
    # Get video frames
    frames = []
    for frame in video.iter_frames():
        frames.append(frame)

    # Apply Gaussian blur to each frame
    blurred_frames = []
    for frame in frames:
        # blurred_frame = cv2.GaussianBlur(frame, (55, 55))
        blurred_frame = cv2.medianBlur(frame, 55)
        blurred_frames.append(blurred_frame)

    # Create video clip from blurred frames
    blurred_video = mp.ImageSequenceClip(blurred_frames, fps=video.fps)

    # Add audio to blurred clip
    blurred_video = blurred_video.set_audio(video.audio)
    return video
    
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
