import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import sys
 
class TwitterClient(object):
    '''Twitter class for senti analysis.'''
    def __init__(self):
        consumer_key = 'u8KVRzIfvR269fMy8O57aodMc'
        consumer_secret = 'dZP6mK2gmyU2Sx449o6REH7JahcdfkxK433gtSoDpG24JIqAvm'
        access_token = '585034442-PXCtF9zdqtG5jBN14vrjKfRyQuxyQdSpBhJ0hNKc'
        access_token_secret = '42j2v75lzQppHIMD4XCIGaQpJghJ9P5JKg1UFjRpdty9F'
 
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication failed")
 
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))    
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
 
    def get_tweets(self, query, count = 50):
        tweets = []
 
        try:
            fetched_tweets = self.api.search(q = query, count = count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                parsed_tweet['text'] = tweet.text.translate(non_bmp_map)
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
 
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
class TwitterObject(object):
    def __init__(self):
        self.api=TwitterClient()
        self.subj='';
        self.ptweets=[]
        self.tweets=[]
        self.ntweets=[]
        self.neutral=[]

    def fetchTweets(self):
        self.tweets = self.api.get_tweets(self.subj, count = 200)
        self.ptweets = [tweet for tweet in self.tweets if tweet['sentiment'] == 'positive']
        self.ntweets = [tweet for tweet in self.tweets if tweet['sentiment'] == 'negative']
        self.neutral=[tweet for tweet in self.tweets if tweet['sentiment']=='neutral']