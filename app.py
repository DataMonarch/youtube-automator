# a gui application that takes a youtube video url and start and end times as input and submits 

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import sys
from tkinter import ttk
from video_processor import trimmer
from video_downloader import youtube_downloader
import json

class GUI:
    def __init__(self, master):
        self.master = master
        self.progress_text = tk.Text(master, height=5, width=50)
        self.progress_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def log_progress(self, message):
        self.progress_text.insert(tk.END, message)
        self.progress_text.see(tk.END)
        self.master.update_idletasks()
        sys.stdout.flush()

def get_video_clip(gui, url_input, start_input, end_input):
    video_url = url_input.get() 
    start_time = start_input.get()
    end_time = end_input.get()
    
    with open("../data/videos/scraped_videos.json", "r") as f:
        available_videos = json.load(f)
        available_video_ids = available_videos.keys()
    
    # extract the youtube video id from the url
    video_id = video_url.split("=")[1]
    
    # make sure the video is downloaded before trimming
    
    
    if  video_id not in available_video_ids:
        gui.log_progress(f">>> Video with id {video_id} not found in the available videos list. Downloading now...\n")
        youtube_downloader.download(video_url)
        gui.log_progress(f">>> Done dowloading. Trimming now...\n")
    else:
        gui.log_progress(f">>> Video with id {video_id} found in the available videos list. Trimming now...\n")
        
    
    # with open("../data/videos/scraped_videos.json", "r") as f:
    #     available_videos = json.load(f)
    #     available_video_ids = available_videos.keys()
    
    # if video_id in available_video_ids:
    try:
        trimmer.get_video_clip(video_id, start_time, end_time)
    except:
        gui.log_progress(f">>> Error trimming video with id {video_id}\n")
    else:
        gui.log_progress(f">>> Done trimming video with id {video_id} from {start_time} to {end_time}\n")

def main():
    root = tk.Tk()
    root.title("VIdeo Trimmer")
    root.configure(bg='gray15')
    # root.geometry("500x250")
    
    # Creating style for the input fields
    label_style_options = {
        'foreground': 'gray70',
        'background': 'gray15',
    }
    
    input_style_options = {
        'foreground': 'black',
        'background': 'white',
    }
    
       
    style = ttk.Style()
    style.configure('TEntry', foreground='gray70', fieldbackground='gray25')
    
    url_label = ttk.Label(root, text="Enter YouTube Video URL:", **label_style_options)
    url_label.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=10, pady=10)

    url_input = ttk.Entry(root, width=50, **input_style_options)
    url_input.grid(row=1, column=0, columnspan=2, sticky="NSEW", padx=10, pady=10)

    start_label = ttk.Label(root, text="Enter Start Time (hh.mm.ss):", **label_style_options)
    start_label.grid(row=2, column=0, sticky="NSEW", padx=10, pady=10)

    start_input = ttk.Entry(root, **input_style_options)
    start_input.grid(row=3, column=0, sticky="NSEW", padx=10, pady=10)

    end_label = ttk.Label(root, text="Enter End Time (hh.mm.ss):", **label_style_options)
    end_label.grid(row=2, column=1, sticky="NSEW", padx=10, pady=10)

    end_input = ttk.Entry(root, **input_style_options)
    end_input.grid(row=3, column=1, sticky="NSEW", padx=10, pady=10)

      
    submit_button = ttk.Button(root, text="Submit", command=lambda: get_video_clip(gui, url_input, start_input, end_input), width=30)
    submit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    gui = GUI(root)
    # for child in root.winfo_children():
    #     child.grid_configure(sticky="NSEW")
    # text_widget = ScrolledText(root)
    # text_widget.pack()
    # Redirect stdout to the GUI text widget
    root.mainloop()

if __name__ == "__main__":
    main()



