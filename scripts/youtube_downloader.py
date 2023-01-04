from pytube import YouTube, extract
import argparse
import os

def Download(url: str, save_path: str = '../data/videos'):
    yt = YouTube(url)
    video_id = extract.video_id(url)
    
    youtube_object = yt.streams.get_highest_resolution()
    captions = yt.captions.get_by_language_code('en')
    
    # TO-DO: pull captions as well
    # captions = captions.generate_srt_captions()
    
    success = False
    try:
        youtube_object.download(output_path=save_path, filename=video_id)
        success = True
        
    except:
        print("An error has occurred")
        
    return success, captions

# url = input("Enter the url of the video: ")
# _, captions = Download(url)
# print(captions)

# write argument parser to get url from command line or from file


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--url", help="Enter the url of the video")
parser.add_argument("-f", "--file", help="Enter the path to the file", default=None)
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

else:
    print("Please enter a url or a file name")