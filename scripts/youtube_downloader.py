from pytube import YouTube, extract, query
import argparse
import os

def Download(url: str, save_path: str = '../data/videos'):
    
    save_path = os.path.abspath(save_path)
    yt = YouTube(url)
    video_id = extract.video_id(url)
    
    filename = f'{video_id}.mp4'
    file_path  = os.path.join(save_path, filename)
    
    youtube_object = yt.streams.get_highest_resolution()
    captions = yt.captions
    captions_query = query.CaptionQuery(captions=captions)
    
    # TO-DO: pull captions as well
    video_captions = None
    print(captions_query.values())
    for key in list(captions_query.keys()):
        
        if "en" in key and "a." not in key:
            video_captions = captions[key].generate_srt_captions()
            break
    
    if not video_captions:
        print(f'No English captions found for {video_id}')

    
    success = False
    try:
        youtube_object.download(output_path=save_path, filename=filename)
        success = True
        print(f'>>> Downloaded {filename} as {file_path}')
    except:
        print(f"! An error has occurred while downloading the video {video_id}")
        
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