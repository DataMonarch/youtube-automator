import tomli
import json
import praw
import os

with open("configs/reddit_config.toml", mode="rb") as fp:
    config = tomli.load(fp)
    CLIENT_ID = config['reddit_oauth']['reddit_client_id']
    CLIENT_SECRET = config['reddit_oauth']['reddit_secret']
    TFR_FLAIRS = config['tales_for_retail']['flairs']


reddit = praw.Reddit(client_id=CLIENT_ID, 
                     client_secret=CLIENT_SECRET,
                     user_agent='discussion_scraper')

def scrape_subreddit(subreddit_name, threads_no_limit=10, skip_n_submission=0,
                     output_file_path=None, scraping_level="thread", comments_no_limit=5):

    if not output_file_path:
        output_file_path = f"submissions_{subreddit_name}"
        
    subreddit = reddit.subreddit(subreddit_name)

    if os.path.exists(output_file_path):
        with open("../data/submissions_tfr.json") as f:
            submissions_dict = json.load(f)
    else:
        submissions_dict = {}
        

    for i, submission in enumerate(subreddit.top(limit = skip_n_submission + threads_no_limit)):
        
        if i < skip_n_submission:
            continue
        
        # print(f'Hottest thread no.{i}: {submission.title}')
        # get the id of a subreddit submission
        flair = submission.link_flair_text
        # print(f"Link flair text: {flair}")
        submission_id = submission.id
        
        if submission_id not in submissions_dict.keys():
        
            if flair.lower() in TFR_FLAIRS:
                
                if scraping_level == "comment":
                    comments = {comment.id: [comment.score, comment.body] for comment_no, comment in enumerate(submission.comments.list()) if comment_no<comments_no_limit}
                else:
                    comments = None
                # if not comments:
                #     top_k_comments = None
                # else:
                #     top_k_comments = sorted(comments.items(), key=lambda x: x[1][0], reverse=True)[0] 
                
                submissions_dict[submission.id] = {'title': submission.title, 
                                                    'flair': flair,
                                                    'body': submission.selftext,
                                                    'comments': comments, 
                                                    }
                # print(top_comment)
                # print('*' * 20)
    

    json_object = json.dumps(submissions_dict, indent=4)

    with open(output_file_path, 'a+') as f:
        f.write(json_object)
    
# scrape the threads in a subreddit

