import tomli
import json
import praw
import os
import re
import argparse


def string_parser(input_text):
    input_text = input_text.replace('\n', ' ')
    input_text = input_text.replace('\"', '\'')
    input_text = input_text.replace('*', '')
    input_text = input_text.replace('>', '.')
    input_text = input_text.replace('\\', '')
    input_text = re.sub("\^\([a-zA-Z0-9(:,;. \/)]*\)", '', input_text)
    # replace string based on regex
    
    return input_text 


def scrape_subreddit(subreddit_name: str, num_threads=10,
                     output_file_path=None, scraping_level="thread", comments_no_limit=5, verbose=False) -> None:
    
    """
    Scrapes a subreddit for threads and comments.
    Inputs:
    - subreddit_name: name of the subreddit to scrape,
    - num_threads: number of threads to scrape, default 10, optional,
    - output_file_path: path to the output file, default None, optional. If None, the output filename will be submissions_{subreddit_name},
    - scraping_level: indicates level of scraping, default "thread", optional, can be "thread" or "comment",
    - comments_no_limit: number of comments to scrape, default 5, optional,
    - verbose: indicates whether to print the scraping progress, default False, optional,
    """
    
    with open("configs/reddit_config.toml", mode="rb") as fp:
        config = tomli.load(fp)
        CLIENT_ID = config['reddit_oauth']['reddit_client_id']
        CLIENT_SECRET = config['reddit_oauth']['reddit_secret']
        FLAIRS = config[subreddit_name]['flairs']


    reddit = praw.Reddit(client_id=CLIENT_ID, 
                        client_secret=CLIENT_SECRET,
                        user_agent='discussion_scraper')


    if not output_file_path:
        output_file_path = f"../data/submissions_{subreddit_name}.json"
        
    subreddit = reddit.subreddit(subreddit_name)

    if os.path.exists(output_file_path):
        with open(output_file_path) as f:
            submissions_dict = json.load(f)
    else:
        submissions_dict = {}
        

    initial_thread_limit = 1000
    no_submissions_recorded = 0
    
    for i, submission in enumerate(subreddit.hot(limit = initial_thread_limit)):

        
        # get the id of a subreddit submission
        flair = submission.link_flair_text
        print(flair)
        # print(f"Link flair text: {flair}")
        submission_id = submission.id
        
        if submission_id not in submissions_dict.keys():
        
            if FLAIRS and flair.lower() in FLAIRS:
                print("flair detected")
                
                if scraping_level == "comment":
                    comments = {comment.id: [comment.score, comment.body] for comment_no, comment in enumerate(submission.comments.list()) if comment_no<comments_no_limit}
                else:
                    comments = None

                submission_body = string_parser(submission.selftext)
                
                submission_title = string_parser(submission.title)
                
                submissions_dict[submission.id] = {'title': submission_title,
                                                    'flair': flair,
                                                    'body': submission_body,
                                                    'comments': comments, 
                                                    }
                
                no_submissions_recorded += 1
                
                if verbose:
                    print(f'>>> Scraped the hot thread no.{no_submissions_recorded}: \nTitle:{submission.title}')
                    print('*' * 20)
                # print(top_comment)
        
        if no_submissions_recorded < num_threads:
            initial_thread_limit += 100
        elif no_submissions_recorded == num_threads:
            break
                
    

    json_object = json.dumps(submissions_dict, indent=4)

    with open(output_file_path, 'a+') as f:
        f.write(json_object)


parser = argparse.ArgumentParser(description='Scrape the threads in a subreddit')
parser.add_argument('--subreddit_name', type=str, help='the name of the subreddit to scrape')
parser.add_argument('--num_threads', type=int, help='the number of threads to scrape', default=10)
parser.add_argument('--output_file_path', type=str, help='the path of the output file', default=None)
parser.add_argument('--scraping_level', type=str, help='the level of scraping', default="thread")
parser.add_argument('--comments_no_limit', type=int, help='the number of comments to scrape', default=5)
parser.add_argument('--verbose', type=bool, help='verbose mode', default=False)
args = parser.parse_args()


subreddit_name = args.subreddit_name
threads_no_limit = args.num_threads
output_file_path = args.output_file_path
scraping_level = args.scraping_level
comments_no_limit = args.comments_no_limit
verbose = args.verbose

# call the function scrape_subreddit on parsed arguments
if __name__ == '__main__':
    scrape_subreddit(subreddit_name, threads_no_limit, output_file_path, scraping_level, comments_no_limit, verbose)
