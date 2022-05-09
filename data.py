import praw
import pandas as pd
import random
import numpy as np
#read the documentation: https://praw.readthedocs.io/en/latest/

#read the documentation: https://praw.readthedocs.io/en/latest/

def user_login(client_id, client_secret,username,password,user_agent):
    # reddit api login
    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         username=username,
                         password=password,
                         user_agent=user_agent)
    return reddit

reddit = user_login(
    "ylbQWn6sbbPt7f_65h4sQQ", # client id
    "lGcLvy3mnJ--DdafDKIu2tfo_sQxMg",
    "rods2022",
    "rods22rods22",
    "rods22" # user agent
)

def getNewPosts(subreddit = "wallstreetbets", numberOfPosts = 50, idStop = ""):
    tmp = reddit.subreddit(subreddit).new(limit = numberOfPosts)
    return tmp

def upvotePost(postID):
    submission = reddit.submission(postID)
    submission.upvote()

def getLikes(postID):
    submission = reddit.submission(postID)
    return (submission.score, submission.upvote_ratio)


def main():
    df = pd.read_csv("dat.csv")
    print('read df')
    Break_id = max(df["id"] if len(df["id"]) else [0,0])
    nop = 10
    #Get new post and add to df
    subs = getNewPosts("wallstreetbets", nop)
    print('get subreddit posts')
    for sub in subs:#, idStop = Break_id):
        if sub.id == Break_id:
            break
        default_list = [0 for i in range(len(df.columns))]
        default_list[0] = sub.id# +default_list
        if random.random() < 0.5:
            upvotePost(sub.id)
            default_list[1] = 1
        else:
            default_list[1] = 0
        df2 = pd.DataFrame(np.insert(df.values, len(df.index), values=default_list, axis=0))
        df2.columns = df.columns
        df =df2
    #Update likes
    seq = df["id"]
    new_data = []
    for id in seq:
        new_data.append(getLikes(id))
    df[len(df.columns)-1] = new_data
    df.to_csv("dat.csv", index = False)
main()

