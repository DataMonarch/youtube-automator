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

def scrape_subreddit(subreddit_name: str, threads_no_limit=10, skip_n_submission=0,
                     output_file_path=None, scraping_level="thread", comments_no_limit=5, verbose=False) -> None:
    
    """
    Scrapes a subreddit for threads and comments.
    Inputs:
    - subreddit_name: name of the subreddit to scrape,
    - threads_no_limit: number of threads to scrape, default 10, optional,
    - skip_n_submission: number of threads to skip from the start, default 0, optional,
    - output_file_path: path to the output file, default None, optional. If None, the output filename will be submissions_{subreddit_name},
    - scraping_level: indicates level of scraping, default "thread", optional, can be "thread" or "comment",
    - comments_no_limit: number of comments to scrape, default 5, optional,
    - verbose: indicates whether to print the scraping progress, default False, optional,
    """

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
                
    

    json_object = json.dumps(submissions_dict, indent=4)

    with open(output_file_path, 'a+') as f:
        f.write(json_object)
    
# scrape the threads in a subreddit

