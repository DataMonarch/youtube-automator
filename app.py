# a gui application that takes a youtube video url and start and end times as input and submits 

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import sys
from io import StringIO
from video_processor import trimmer
from video_downloader import youtube_downloader
import json

class GUI:
    def __init__(self, master):
        self.master = master
        self.progress_text = tk.Text(master, height=20, width=50)
        self.progress_text.pack()

    def log_progress(self, message):
        self.progress_text.insert(tk.END, message)
        self.progress_text.see(tk.END)
        self.master.update_idletasks()

def get_video_clip(gui):
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
        gui.log_progress(f">>> Video with id {video_id} not found in the available videos list. Downloading now...")
        youtube_downloader.download(video_url)
    
    # with open("../data/videos/scraped_videos.json", "r") as f:
    #     available_videos = json.load(f)
    #     available_video_ids = available_videos.keys()
    
    # if video_id in available_video_ids:
    gui.log_progress(f">>> Done dowloading. Trimming now...")
    try:
        trimmer.get_video_clip(video_id, start_time, end_time)
    except:
        gui.log_progress(f">>> Error trimming video with id {video_id}")
    else:
        gui.log_progress(f">>> Done trimming video with id {video_id} from {start_time} to {end_time}")

def main():
    root = tk.Tk()
    root.title("VIdeo Trimmer")
    
    gui = GUI(root)
    sys.stdout = gui
    
    url_label = tk.Label(root, text="Enter YouTube Video URL:")
    url_label.pack()

    url_input = tk.Entry(root)
    url_input.pack()

    start_label = tk.Label(root, text="Enter Start Time (hh.mm.ss):")
    start_label.pack()

    start_input = tk.Entry(root)
    start_input.pack()

    end_label = tk.Label(root, text="Enter End Time (hh.mm.ss):")
    end_label.pack()

    end_input = tk.Entry(root)
    end_input.pack()

    text_widget = ScrolledText(root)
    text_widget.pack()
      
    submit_button = tk.Button(root, text="Submit", command=get_video_clip(gui))
    submit_button.pack()


    # Redirect stdout to the GUI text widget
    root.mainloop()

if __name__ == "__main__":
    main()



