from googleapiclient.discovery import build
import tomli

with open("../configs/yt_config.toml", "rb") as f:
    config = tomli.load(f)
    API_KEY = config["youtube_data_api"]["key"]


CHANNEL_ID = 'UCllYn_ao6QzNKMyixWmHmkw'

youtube = build('youtube', 'v3', developerKey=API_KEY)

channel_response = youtube.channels().list(
    id=CHANNEL_ID,
    part='snippet, statistics'
).execute()

channel_title = channel_response['items'][0]['snippet']['title']
subscriber_count = channel_response['items'][0]['statistics']['subscriberCount']

print(f'Channel title: {channel_title}')
print(f'Subscriber count: {subscriber_count}')
