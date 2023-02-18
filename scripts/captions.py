

import requests
import json

# Get the video ID from the URL 
def get_video_id(url): 
    video_id = url.split('=')[1] 
    return video_id 
  
# Get the captions of the video from YouTube Data API 
def get_captions(video_id): 

    # YouTube Data API key  
    api_key = 'AIzaSyBMSgZokcqEjPjSJ0VytpPm2PGs-QDxnU0'

    # YouTube Data API URL  
    url = 'https://www.googleapis.com/youtube/v3/captions?part=snippet&videoId=' + video_id + '&key=' + api_key

    # Request to get the captions  
    response = requests.get(url)

    # Convert response to JSON format  
    json_data = json.loads(response.text)
    print(json_data)
    # Get the captions from JSON data  
    items = json_data['items']

    # Print all captions of the video  
    for item in items: 
        if item["snippet"]["language"] == "en":
            caption_id = item["id"]
            break
        
    url = f"http://video.google.com/timedtext?lang=en&v={video_id}&fmt=srv3&name&signature&cap_id={caption_id}"
    captions = requests.get(url).text
    
    return captions
      
# Driver Code 
if __name__ == '__main__': 

	# Enter the URL of a YouTube Video here  														     # https://www.youtube.com/watch?v=YOUTUBE VIDEO ID HERE 

     url = input() 

     # Get Video ID from URL  
     video_id = get_video_id(url) 

     # Get Captions of Video from YouTube Data API  
     captions = get_captions(video_id)
     print(captions)