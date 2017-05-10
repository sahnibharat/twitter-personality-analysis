import tweepy #https://github.com/tweepy/tweepy
import csv
import re
#import thread 
import threading
import datetime
import time
from gingerit.gingerit import GingerIt
from tweepy import OAuthHandler
from textblob import TextBlob
import sys

#Twitter API credentials
consumer_key = "u8KVRzIfvR269fMy8O57aodMc"
consumer_secret = "dZP6mK2gmyU2Sx449o6REH7JahcdfkxK433gtSoDpG24JIqAvm"
access_key = "585034442-PXCtF9zdqtG5jBN14vrjKfRyQuxyQdSpBhJ0hNKc"
access_secret = "42j2v75lzQppHIMD4XCIGaQpJghJ9P5JKg1UFjRpdty9F"
parser = GingerIt()

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)
tweets = []
agreecount=0
opticount=0
negtweet=0
pessicount=0
postweet=0
viewholdercount=0
neuttweet=0
spectcount=0
specttweet=0
grammar=0
non_bmp_map=dict.fromkeys(range(0x10000, sys.maxunicode+1), 0xfffd)
parser = GingerIt()
class myThread(threading.Thread):
                def __init__(self,counter,tweet,hashtag):
                                threading.Thread.__init__(self)
                                self.counter=counter
                                self.tweet=tweet
                                self.hashtag=hashtag
                          
                def run(self):
                                parsed_tweet={}
                                parsed_tweet['text']=self.tweet.translate(non_bmp_map)
                                parsed_tweet['sentiment'] = self.get_tweet_sentiment(str(self.tweet))
                                #count=api.retweet_count(str(self.tweet))
                                tweets.append(parsed_tweet)
                                ptweets= self.get_tweets(self.hashtag,30)
                                if ptweets=="0" or ptweets==0:
                                                ptweets=parsed_tweet['sentiment']
                                if ptweets==parsed_tweet['sentiment']:
                                                global agreecount
                                                agreecount+=1
                                if str(ptweets)=='negative':
                                                global negtweet
                                                negtweet+=1
                                if str(ptweets)=='negative' and parsed_tweet['sentiment']=='positive':
                                                global opticount
                                                opticount+=1
                                if str(ptweets)=='neutral':
                                                global neuttweet
                                                neuttweet+=1
                                if str(ptweets)=='neutral' and parsed_tweet['sentiment']=='neutral':
                                                global viewholdercount
                                                viewholdercount+=1
                                if str(ptweets)!='neutral':
                                                global specttweet
                                                specttweet+=1
                                if str(ptweets)!='neutral' and parsed_tweet['sentiment']=='neutral':
                                                global spectcount
                                                spectcount+=1
                                if str(ptweets)!='positive':
                                                global postweet
                                                postweet+=1
                                if str(ptweets)!='positive' and parsed_tweet['sentiment']=='negative':
                                                global pessicount
                                                pessicount+=1
                                #print("counter:",self.counter," tweet sentiment:",parsed_tweet['sentiment'],"hashtag sentiment",ptweets)
                                
                def get_tweet_sentiment(self,tweet):
                                analysis = TextBlob(self.clean_tweet(tweet))
                                if analysis.sentiment.polarity > 0:
                                                #print("positive")
                                                return 'positive'
                                elif analysis.sentiment.polarity == 0:
                                                return 'neutral'
                                else:
                                                return 'negative'
                                                
                def get_tweets(self,query,count):
                                tweets1 = []
                                try:
                                                ptweets=0
                                                ntweets=0
                                                neut=0
                                                fetched_tweets = api.search(q = query, count = count)
                                                for tweet in fetched_tweets:
                                                                parsed_tweet = {}
                                                                #non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                                                                parsed_tweet['text'] = tweet.text.translate(non_bmp_map)
                                                                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                                                                if tweet.retweet_count > 0:
                                                                                if parsed_tweet not in tweets:
                                                                                                if parsed_tweet['sentiment']=='positive':
                                                                                                                ptweets+=1
                                                                                                elif parsed_tweet['sentiment']=='negative':
                                                                                                                ntweets+=1
                                                                                                else:
                                                                                                                neut+=1
                                                                                                tweets1.append(parsed_tweet)
                                                                else:
                                                                                if parsed_tweet['sentiment']=='positive':
                                                                                                ptweets+=1
                                                                                elif parsed_tweet['sentiment']=='negative':
                                                                                                ntweets+=1
                                                                                else:
                                                                                                neut+=1
                                                                                tweets1.append(parsed_tweet)
                                                                                #print(ptweets," ",ntweets," ",neut)
                                                if len(tweets1)==0:
                                                                return "0"
                                                if ptweets >= ntweets and ptweets >=neut  :
                                                                return "positive"
                                                elif ntweets >= ptweets and ntweets >=neut:
                                                                return "negative"
                                                else:
                                                                return "neutral"
                                                
                                
                                except tweepy.TweepError as e:
                                                print("Error : " + str(e))
                                                return 0
                                

                def clean_tweet(self, tweet):
                                          return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
                                
                
class Grammar(threading.Thread):
                def __init__(self,counter,tweet):
                                threading.Thread.__init__(self)
                                self.counter=counter
                                self.tweet=tweet
                def clean_tweet(self,tweet):
                                return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

                def run(self):
                                try:
                                                global grammar
                                                self.tweet=self.clean_tweet(self.tweet)
                                                p=parser.parse(self.tweet)
                                                #print (p)
                                                if len(p['corrections'])<=2:
                                                                grammar+=1
                                except Exception as e:
                                                pass
                                                #print(e)
                
class Var(object):
        def __init__(self):                     
                self.agree=0
                self.opti = 0
                self.pessi = 0
                self.spec = 0
                self.social = 0
                self.view = 0
                self.gram=0
                self.public=''
                self.subj=''
                self.img=''
                self.follower=0
                self.following=0
                self.tweets=0
                self.name=""
                self.yes="yes"
                self.t=[]
        def clean_tweet(self,tweet):
                return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
 
        def get_tweet_sentiment(self,tweet):
                analysis = TextBlob(clean_tweet(tweet))
                #print(analysis," ",analysis.sentiment.polarity)
                if analysis.sentiment.polarity > 0:
                        return 'positive'
                elif analysis.sentiment.polarity == 0:
                        return 'neutral'
                else:
                        return 'negative'
        def get_all_tweets(self):
                screen_name=self.subj
                #Twitter only allows access to a users most recent 3240 tweets with this method
                #initialize a list to hold all the tweepy Tweets
                alltweets = []  
                new_tweets =[]
                
                #make initial request for most recent tweets (200 is the maximum allowed count)
                try:
                                new_tweets = api.user_timeline(screen_name = screen_name,count=200)
                                alltweets.extend(new_tweets)
                                oldest = alltweets[-1].id - 1
                except Exception as e:
                                self.yes="no"
                                print(e)
                                return
                #save most recent tweets
                
                
                #save the id of the oldest tweet less one
        
                
                #keep grabbing tweets until there are no tweets left to grab
                while len(new_tweets) > 0:
                                #print ("getting tweets before %s" % (oldest))
                                
                                #all subsiquent requests use the max_id param to prevent duplicates
                                new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
                                
                                #save most recent tweets
                                alltweets.extend(new_tweets)
                                
                                #update the id of the oldest tweet less one
                                oldest = alltweets[-1].id - 1
                                
                                print ("...%s tweets downloaded so far" % (len(alltweets)))
                                if(len(alltweets)>=100):
                                                break
                
                #transform the tweepy tweets into a 2D array that will populate the csv
                now = datetime.date.today()
                week=now-datetime.timedelta(days=15)
                #week=week.strftime('%d-%m-%Y')
                #print(now," ",str(week))
                socialbird=0
                outtweets = [[ tweet.text.encode("utf-8")] for tweet in alltweets]
                timetweet=[[ tweet.created_at] for tweet in alltweets]
                c=0
                for tweet in timetweet:
                                if c>=50:
                                    break
                                tweet=str(tweet)
                                tweet=self.clean_tweet(tweet)
                                tweet=tweet.split(" ")
                                #tweet=tweet[4]+"-"+tweet[3]+"-"+tweet[2]
                                #print(tweet)
                                c+=1
                                if int(tweet[2])>=int(week.strftime('%Y')):
                                    if int(tweet[3])>=int(week.strftime('%m')):
                                        if int(tweet[4])>=int(week.strftime('%d')):
                                                socialbird+=1
                                
                                
                hashed=[]
                hashtweet=[]
                nohash=[]
                #print("SocialBird:{}/100".format(100*socialbird/len(timetweet)))
                for line in outtweets:
                                line=str(line)
                                search=re.search(r'^(.*)#(.*)\s*(.*)$',line)
                                if(search):
                                                search=str(line)
                                                temp=(re.findall(r'[#]\S*',search))
                                                t=self.clean_tweet(temp[0])
                                                hashtweet.append(t)
                                                #print(t)
                                                hashed.append(line)
                                else:
                                        line=self.clean_tweet(line)
                                        nohash.append(line)                                                
                                                                                
                try:
                                global agreecount,opticount,negtweet,pessicount,postweet,viewholdercount,neuttweet,spectcount,specttweet,grammar,tweets
                                tweets=[]
                                agreecount=0
                                opticount=0
                                negtweet=0
                                pessicount=0
                                postweet=0
                                viewholdercount=0
                                neuttweet=0
                                spectcount=0
                                specttweet=0
                                grammar=0
                                #print (len(hashed))
                                threads=[]
                                counter=0
                                for tweet in hashed:
                                                if counter>=50:
                                                                break
                                                #threading.Thread(target=get_all_tweets, args=("Thread-2","_sahnibharat",))
                                                p=myThread(counter,str(tweet),hashtweet[counter])
                                                p.start()
                                                threads.append(p)
                                                counter+=1
                                
                                for t in threads:
                                           t.join()
                                           print ("#",end=' ')
                                print ()

                                counter=0
                                grammy=[]
                                for tweet in nohash:
                                                if counter>=50:
                                                        break
                                                p=Grammar(counter,str(tweet))
                                                p.start()
                                                grammy.append(p)
                                                counter+=1
                                for t in grammy:
                                                t.join()
                                                print("-",end=' ')
                                print()

                                                           
                except tweepy.TweepError as e:
                                print("Error : "+str(e))
                #ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
                #print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(hashed)))
                #write the csv
                if len(threads)==0:
                    print ("Agreeableness:",agreecount," %")
                    self.agree=agreecount
                else:
                    print("Agreeableness:{} %".format(100*agreecount/len(threads)))
                    self.agree = int(100*agreecount/len(threads)               )
                
                #print(opticount," ",negtweet," ",agreecount," ",viewholdercount)
                if len(threads)==0:
                    self.opti=0
                    print("Optimist:0 %")
                elif negtweet==0 or opticount==0:
                                ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
                                print("Optimist-{} %".format(100*len(ptweets)/len(threads)))
                                #obj.opti = 100*len(ptweets)/len(threads)
                                self.opti=int(100*len(ptweets)/len(tweets))
                else:
                                print("Optimist:{} %".format(100*opticount/negtweet))
                                self.opti = int(100*opticount/negtweet)
                if len(threads)==0:
                    self.pessi=0
                    print("Pessimist:0 %")
                elif postweet==0:
                                ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
                                print("Pessimist-{} %".format(100*len(ptweets)/len(threads)))
                                self.pessi = int(100*len(ptweets)/len(threads))
                else:
                                print("Pessimist:{} %".format(100*pessicount/postweet))
                                self.pessi = int(100*pessicount/postweet)
                if len(threads)==0:
                    self.view=0
                    print("Viewholder:0%")
                elif neuttweet!=0:
                                print("Viewholder-{} %".format(100*viewholdercount/neuttweet))
                                self.view = int(100*viewholdercount/neuttweet )
                else:
                                ptweets = [tweet for tweet in tweets if tweet['sentiment'] != 'neutral']
                                print("Viewholder:{} %".format(100*len(ptweets)/len(threads)))
                                self.view = int(100*len(ptweets)/len(threads))
                if len(threads)==0:
                    self.spec=0
                    print("Spectator:0%")
                elif specttweet!=0:
                                print("Spectator:{} %".format(100*spectcount/specttweet))
                                self.spec = int(100*spectcount/specttweet)
                else:
                                neut=[tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
                                print("Spectator:{} %".format(100*len(neut)/len(threads)))
                                self.spec = int(100*len(neut)/len(threads))

                self.follower=api.get_user(screen_name).followers_count
                self.following=api.get_user(screen_name).friends_count
                print("followers-",self.follower)
                print("following-",self.following)
                self.img=api.get_user(screen_name).profile_image_url
                self.img=self.img.replace("_normal",'')
                #print(x)
                print(self.img)
                #print("listed in-",api.get_user(screen_name).listed_count)
                if(api.get_user(screen_name).verified):
                                print("Public Figure")
                                self.public="Public Figure"
                else:
                                print("Not a Public Figure")
                                self.public="Not a Public Figure"
                if len(timetweet)==0:
                    print("SocialBird-",socialbird,"%")
                    self.social=socialbird
                else:
                    print("SocialBird:{} %".format(100*socialbird/len(timetweet)))
                    self.social = int(100*socialbird/len(timetweet))
                
                if len(nohash)==0:
                        print("GrammarNazi:0%")
                        self.gram=0
                else:
                        print("GrammarNazi:{}%".format(100*grammar/counter))
                        self.gram = int(100*grammar/counter)
                self.tweets=api.get_user(screen_name).statuses_count
                print("no of tweets-",self.tweets)
                self.name=api.get_user(screen_name).name
                print (self.name)
                self.t=tweets
                #print (str(now.date))
                return self








  






