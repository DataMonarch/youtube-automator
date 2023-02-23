import json
import toml
import pandas as pd
import numpy as np
import os
import moviepy.editor as mp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import clips_array


def change_aspect_ratio(video: VideoFileClip, new_aspect_ratio: float = 9/16):
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
        video = video.resize(0.5)
        width, height = video.size
        
        bar_height = int((int(width * (1 / new_aspect_ratio)) - height) / 2)
        video = video.margin(left=0, right=0, top=bar_height, bottom=bar_height)
        
        return video