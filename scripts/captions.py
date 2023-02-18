from youtube_transcript_api import YouTubeTranscriptApi
import requests
import json
import tomli

with open("configs/yt_configs.toml", mode="rb") as fp:
    config = tomli.load(fp)
    LANG_PRIORITY_LIST = config['yt_srt']['lang_priority_list']


# Get the video ID from the URL 
def get_video_id(url): 
    video_id = url.split('=')[1] 
    return video_id 
  
# Get the captions of the video from YouTube Data API 
def get_captions(video_id): 

    # YouTube Data API key  
    srt = YouTubeTranscriptApi.get_transcript(video_id, LANG_PRIORITY_LIST)
    
    return srt
      
# Driver Code 
if __name__ == '__main__': 

	# Enter the URL of a YouTube Video here  														     # https://www.youtube.com/watch?v=YOUTUBE VIDEO ID HERE 

     url = input() 

     # Get Video ID from URL  
     video_id = get_video_id(url) 

     # Get Captions of Video from YouTube Data API  
     captions = get_captions(video_id)
     print(captions)