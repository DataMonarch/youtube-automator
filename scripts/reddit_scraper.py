import tomli
import json
import praw

with open("configs/reddit_config.toml", mode="rb") as fp:
    config = tomli.load(fp)
    CLIENT_ID = config['reddit_oauth']['reddit_client_id']
    CLIENT_SECRET = config['reddit_oauth']['reddit_secret']
    TFR_FLAIRS = config['tales_for_retail']['flairs']


reddit = praw.Reddit(client_id=CLIENT_ID, 
                     client_secret=CLIENT_SECRET,
                     user_agent='discussion_scraper')

subreddit = reddit.subreddit('TalesFromRetail')

submissions_dict = {}

for i, submission in enumerate(subreddit.hot(limit=10)):
    print(f'Hottest thread no.{i}: {submission.title}')
    # get the id of a subreddit submission
    flair = submission.link_flair_text
    print(f"Link flair text: {flair}")
    
    if flair.lower() in TFR_FLAIRS:

        comments = {comment.id: [comment.score, comment.body] for comment in submission.comments.list()}
        if not comments:
            top_comment = None
        else:
            top_comment = sorted(comments.items(), key=lambda x: x[1][0], reverse=True)[0] 
        
        submissions_dict[submission.id] = {'title': submission.title, 
                                        'flair': flair,
                                        'top_comment': top_comment}
        print(top_comment)
        print('*' * 20)
 

json_object = json.dumps(submissions_dict, indent=4)

with open('../data/submissions_tfr.json', 'a+') as f:
    f.write(json_object)
    
# scrape the most liked comment under a thread in a subreddit