import tomli
import json

with open("conf.toml", mode="rb") as fp:
    config = tomli.load(fp)
    CLIENT_ID = config['reddit_oauth']['reddit_client_id']
    CLIENT_SECRET = config['reddit_oauth']['reddit_secret']

import praw

reddit = praw.Reddit(client_id=CLIENT_ID, 
                     client_secret=CLIENT_SECRET,
                     user_agent='discussion_scraper')

subreddit = reddit.subreddit('TalesFromRetail')

submissions_dict = {}

for i, submission in enumerate(subreddit.hot(limit=10)):
    print(f'Hottest thread no.{i}: {submission.title}')
    print(f"Link flair text: {submission.link_flair_text}")
    # get the id of a subreddit submission

    
    comments = {comment.id: [comment.score, comment.body] for comment in submission.comments.list()}
    if not comments:
        top_comment = None
    else:
        top_comment = sorted(comments.items(), key=lambda x: x[1][0], reverse=True)[0] 
    
    submissions_dict[submission.id] = {'title': submission.title, 
                                    'flair': submission.link_flair_text,
                                    'top_comment': top_comment}
    print(top_comment)
    print('*' * 20)
 
 
with open('submissions.json', 'a+') as f:
    json.dump(submissions_dict, f)
# scrape the most liked comment under a thread in a subreddit