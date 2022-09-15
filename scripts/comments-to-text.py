#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os 

data_path = os.path.join('..', 'data')

# Loading data
path = os.path.join(data_path, 'reddit_tagpro-mylittlepony_01042017-04042017_long.csv')
posts_df = pd.read_csv(path)

# list of comments
comments = list(posts_df['comment_body'])

# save as txt
with open(os.path.join(data_path, "reddit_comments.txt"), 'w') as f:
    for line in comments:
        f.write(line)