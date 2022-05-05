import tweepy

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth)

def retrieve_tweets(terms, last_tweet=""):
    kwargs = {
       "screen_name": "Wario64",
       "trim_user": True
    }
    if last_tweet:
        kwargs['since_id'] = last_tweet
    else:
        kwargs['count'] = 200

    wario_tweets = tweepy.Cursor(api.user_timeline, **kwargs)
    filtered_results = {term:{"tweets":[]} for term in terms}
    last_tweet_id = filtered_results[-1].id
    for tweet in wario_tweets:
        for term in terms:
            if term in tweet.text:
                filtered_results[term]["tweets"].append(tweet.id)
    
    return filtered_results, last_tweet_id