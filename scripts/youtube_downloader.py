from pytube import YouTube, Search, extract, query
import random
import argparse
import os
import json

def get_srt_captions(yt_object):
    captions = yt_object.captions
    captions_query = query.CaptionQuery(captions=captions)
    
    # TO-DO: pull captions as well
    video_captions = None
    print(captions_query.values())
    
    for key in list(captions_query.keys()):
        
        if "en" in key and "a." not in key:
            video_captions = captions[key].generate_srt_captions()
            break
    
 

def Download(url: str = None, yt_object: YouTube = None, 
             save_path: str = '../data/videos', json_out_path=None):
    
    # documentation for the Download method
    """
    Download a video from a given URL.
    Parameters
    ----------
    url: str
        URL of the video to be downloaded.
    save_path: str 
        Path to save the downloaded video.
        
    Returns
    -------
    None
    """
    if yt_object:
        yt = yt_object
        video_id = random.randint(1, 100000)

    elif url:
        yt = YouTube(url)
        video_id = extract.video_id(url)
        
    else:
        print('No URL or YouTube object provided.')
        return None
        
    if not output_file_path:
        output_file_path = f"../data/videos/scraped_videos.json"
    
    if os.path.exists(output_file_path):
        with open(output_file_path) as f:
            videos_dict = json.load(f)
    else:
        videos_dict = {}
    
    save_path = os.path.abspath(save_path)
    
    filename = f'{video_id}.mp4'
    file_path  = os.path.join(save_path, filename)
    
    youtube_object = yt.streams.get_highest_resolution()
    video_title = youtube_object.title
    
    videos_dict['id'] = video_id
    videos_dict["title"] = video_title
    
    video_captions = get_srt_captions(youtube_object)
    
    if not video_captions:
        print(f'No English captions found for {video_id}')
        
    success = False
    try:
        youtube_object.download(output_path=save_path, filename=filename)
        success = True
        print(f'>>> Downloaded {filename} as {file_path}')
    except:
        print(f"! An error has occurred while downloading the video {video_id}")
    
    if video_id not in videos_dict.keys():
    
        videos_dict[video_id] = {'title': video_title, 
                                'file_path': file_path,
                                'captions': video_captions
                                }
        
        json_object = json.dumps(videos_dict, indent=4)

        with open(output_file_path, 'a+') as f:
            f.write(json_object)
            
    else:
        print(f"Video {video_id} already exists in the output file")
            
    return success


def search_and_download_top_k(query: str, k: int = 10, save_path = '../data/videos'):
    # write documentation for the search_and_download_top_k method
    """
    Searches for the top k videos matching the query and downloads them.

    Parameters
    ----------
    query : str
        The query to search for.
    k : int
        The number of videos to download.
    save_path : str
        The path to save the downloaded videos.

    Returns
    -------
    None
    """
    
    search = Search(query)
    
    for i, yt_object in enumerate(search.results):
        Download(yt_object=yt_object, save_path=save_path)
        
        if i == k-1: break


# url = input("Enter the url of the video: ")
# _, captions = Download(url)
# print(captions)



# write argument parser to get url from command line or from file


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--url", help="Enter the url of the video", default=None)
parser.add_argument("-f", "--file", help="Enter the path to the file", default=None)
parser.add_argument("-s", "--save_path", help="Enter the path to save the video", default=None)
parser.add_argument("-q", "--query", help="Enter the query to search for", default=None)
parser.add_argument("-c", "--count", help="Enter the number of videos to download", default=10)
args = parser.parse_args()

if args.url:
    url = args.url
    _, captions = Download(url)
    print(captions)

elif args.file:
    file = args.file
    with open(file, 'r') as f:
        for line in f:
            url = line
            _, captions = Download(url)
            print(captions)
            
elif args.query:
    search_and_download_top_k(args.query, int(args.count))

else:
    print("Please enter a url, a file name, or a search query")
    
    
    
