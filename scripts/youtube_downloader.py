from pytube import YouTube, Search, extract, query
import random
import argparse
import os

def Download(url: str = None, yt_object: YouTube = None, save_path: str = '../data/videos'):
    
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
        
    save_path = os.path.abspath(save_path)
    
    filename = f'{video_id}.mp4'
    file_path  = os.path.join(save_path, filename)
    
    youtube_object = yt.streams.get_highest_resolution()
    captions = yt.captions
    captions_query = query.CaptionQuery(captions=captions)
    
    # TO-DO: pull captions as well
    video_captions = None
    print(captions_query.values())
    
    # for key in list(captions_query.keys()):
        
    #     if "en" in key and "a." not in key:
    #         video_captions = captions[key].generate_srt_captions()
    #         break
    
    # if not video_captions:
    #     print(f'No English captions found for {video_id}')

    
    success = False
    try:
        youtube_object.download(output_path=save_path, filename=filename)
        success = True
        print(f'>>> Downloaded {filename} as {file_path}')
    except:
        print(f"! An error has occurred while downloading the video {video_id}")
        
    return success, captions


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
    
    
    