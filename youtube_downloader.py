from pytube import YouTube

def Download(link):
    yt = YouTube(link)
    youtubeObject = yt.streams.get_highest_resolution()
    captions = yt.captions.get_by_language_code('en')
    
    # TO-DO: pull captions as well
    # captions = captions.generate_srt_captions()
    
    success = False
    try:
        youtubeObject.download()
        success = True
        
    except:
        print("An error has occurred")
        
    return success, captions

link = input("Enter the link of the video: ")
_, captions = Download(link)
print(captions)
