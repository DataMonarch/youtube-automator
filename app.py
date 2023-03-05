# a gui application that takes a youtube video url and start and end times as input and submits 

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import sys
from io import StringIO
from video_processor import trimmer
from video_downloader import youtube_downloader
import json



def get_video_clip():
    video_url = url_input.get() 
    start_time = start_input.get()
    end_time = end_input.get()
    
    with open("../data/videos/scraped_videos.json", "r") as f:
        available_videos = json.load(f)
        available_video_ids = available_videos.keys()
    
    # extract the youtube video id from the url
    video_id = video_url.split("=")[1]
    video_id = video_id.split("&")[0]
    
    # make sure the video is downloaded before trimming
    
    
    if  video_id not in available_video_ids:
        print(f">>> Video with id {video_id} not found in the available videos list. Downloading now...")
        youtube_downloader.download(video_url)
    
    # with open("../data/videos/scraped_videos.json", "r") as f:
    #     available_videos = json.load(f)
    #     available_video_ids = available_videos.keys()
    
    # if video_id in available_video_ids:
    print(f">>> Done dowloading. Trimming now...")
    trimmer.get_video_clip(video_id, start_time, end_time)
    

def redirect_output(function):
    def wrapper(*args, **kwargs):
        # redirect output to the Text widget
        text_widget = kwargs.pop('text_widget', None)
        if text_widget:
            text_widget.configure(state="normal")
            text_widget.delete('1.0', 'end')
            original_stdout = sys.stdout
            sys.stdout = redirected_output = StringIO()
            result = function(*args, **kwargs)
            sys.stdout = original_stdout
            redirected_output = redirected_output.getvalue()
            text_widget.insert('end', redirected_output)
            text_widget.configure(state="disabled") 
        else:
            result = function(*args, **kwargs)
        return result
    return wrapper


@redirect_output
def submit_action():
    get_video_clip()

root = tk.Tk()

url_label = tk.Label(root, text="Enter YouTube Video URL:")
url_label.pack()

url_input = tk.Entry(root)
url_input.pack()

start_label = tk.Label(root, text="Enter Start Time (in seconds):")
start_label.pack()

start_input = tk.Entry(root)
start_input.pack()

end_label = tk.Label(root, text="Enter End Time (in seconds):")
end_label.pack()

end_input = tk.Entry(root)
end_input.pack()

text_widget = ScrolledText(root)
text_widget.pack()

submit_button = tk.Button(root, text="Submit", command=submit_action(text_widget=text_widget))
submit_button.pack()

root.mainloop()
