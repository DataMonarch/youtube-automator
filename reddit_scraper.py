# Scrape discussions of a subreddit

import praw

reddit = praw.Reddit(client_id='CLIENT_ID',
                     client_secret='CLIENT_SECRET',
                     user_agent='USERAGENT')

subreddit = reddit.subreddit('SUBREDDIT')

for submission in subreddit.hot(limit=10):
    print(submission.title)