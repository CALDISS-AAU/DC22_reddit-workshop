#!/usr/bin/env python
# coding: utf-8

import sys
import os
from datetime import datetime
import json
from json import JSONDecodeError
import requests
import time
import random
import pandas as pd
sys.path.append(os.path.join('..', 'modules'))
from pushift_wrap import get_submissions, get_comments

sub_end = "https://api.pushshift.io/reddit/search/submission/"
subcomment_end = "https://api.pushshift.io/reddit/submission/comment_ids/"
comment_end = "https://api.pushshift.io/reddit/search/comment/"

# subreddits: r/Tagpro og r/mylittlepony 
# date range: 2017-04-01-2017-04-04 

start_time_epoch = int(datetime(2017,4,1,0,0).timestamp())
end_time_epoch = int(datetime(2017,4,5,0,0).timestamp())

subreddits = ['tagpro', 'mylittlepony']

submissions_all = []
for subreddit in subreddits:
    submissions = get_submissions(subreddit, before = end_time_epoch, after = start_time_epoch, size = 500, num_comments = 0)
    
    submissions_all = submissions_all + submissions
    

for submission in submissions_all:
    subid = submission.get('id')
    try:
        commentids = requests.get(f"{subcomment_end}{subid}").json().get('data')
    
        comments = get_comments(commentids)
        submission['comments'] = comments
        
        time.sleep(random.uniform(0.05, 0.1))
    except JSONDecodeError:
        time.sleep(5)
        
        commentids = requests.get(f"{subcomment_end}{subid}").json().get('data')
    
        comments = get_comments(commentids)
        submission['comments'] = comments
        
        time.sleep(random.uniform(0.05, 0.1))
        
    
out_dir = os.path.join('..', 'data')
filename = 'reddit_tagpro-mylittlepony_01042017-04042017.json'

with open(os.path.join(out_dir, filename), 'w', encoding = 'utf-8') as f:
    json.dump(submissions_all, f)

posts_df = pd.DataFrame.from_records(submissions_all)

posts_df_long = posts_df.explode('comments').reset_index(drop=True).add_prefix('post_')
posts_df_long = posts_df_long.dropna(subset = ['post_comments'])

posts_df_long = pd.merge(posts_df_long, pd.json_normalize(posts_df_long['post_comments']).add_prefix('comment_'), left_index=True, right_index=True)

outname = "reddit_tagpro-mylittlepony_01042017-04042017_long.csv"

posts_df_long.to_csv(os.path.join(out_dir, outname), index = False)