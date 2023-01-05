from os import getenv
from .models import DB, Tweet, User
import tweepy
import spacy


#get api keysfrom our .env file
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)

def add_or_update_user(username):
    '''ADD AND UPDATE THE USER TO APP'''

    try:

        twitter_user = TWITTER.get_user(screen_name=username)

        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id)

        DB.session.add(db_user)

        tweets = twitter_user.timeline(count=200,
                                    exclude_replies=True,
                                    include_rts=False,
                                    tweet_mode='extended',
                                    since_id=db_user.newest_tweet_id)

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.text)
            db_tweet = Tweet(id=tweet.id,
                            text=tweet.full_text[:300],
                            vect=tweet_vector)
            db_user.tweets.append(db_tweet)

            DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error processing {username}: {e}")
        raise e


    else: 
        DB.session.commit()

nlp = spacy.load('my_model/')

def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector
