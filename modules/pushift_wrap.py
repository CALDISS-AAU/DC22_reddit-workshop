import requests
import time
import random
import os 
import json
import math

sub_end = "https://api.pushshift.io/reddit/search/submission/"
subcomment_end = "https://api.pushshift.io/reddit/submission/comment_ids/"
comment_end = "https://api.pushshift.io/reddit/search/comment/"

def get_submissions(subreddit, before, after, q = "", size = 100, num_comments = 15, fields = ['author', 'created_utc', 'domain', 'full_link', 'gildings', 'id', 'is_original_content', 'is_reddit_media_domain', 
                                                                           'locked', 'media_only', 'num_comments', 'num_crossposts', 'over_18', 'permalink', 'pinned', 'post_hint', 'preview', 
                                                                           'retrieved_on', 'score', 'selftext', 'spoiler', 'stickied', 'subreddit', 'subreddit_id', 'subreddit_subscribers',
                                                                           'subreddit_type', 'thumbnail', 'title', 'total_awards_received', 'upvote_ratio', 'url', 'url_overridden_by_dest',
                                                                           'comments']):
    
    endpoint = "https://api.pushshift.io/reddit/search/submission/"
    fields_str = ','.join(fields)
    
    request_url = f"{endpoint}?subreddit={subreddit}&before={before}&after={after}&size={size}&num_comments=>{num_comments}&q={q}&fields={fields_str}"
    
    submissions = requests.get(request_url).json().get('data')
    return(submissions)
    
def get_comments(commentids, fields = ['author', 'banned_at_utc', 'body', 'collapsed', 'collapsed_reason', 'comment_type', 'created_utc', 'edited', 'id', 'is_submitter',
                 'link_id', 'parent_id', 'permalink', 'retrieved_on', 'score', 'stickied', 'subreddit', 'subreddit_id', 'total_awards_received']):
    
    endpoint = 'https://api.pushshift.io/reddit/search/comment/'
    
    max_ids = 500
    split = math.ceil(len(commentids)/max_ids)

    comment_fields_str = ','.join(fields)

    comments = []
    for i in range(split):
        ids_chunk = commentids[i*max_ids:(i+1)*max_ids]
        commentids_str = ','.join(ids_chunk)

        request_url = f"{endpoint}?ids={commentids_str}&fields={comment_fields_str}"

        comments_chunk = requests.get(request_url).json().get('data')
        comments = comments + comments_chunk
    
    return(comments)