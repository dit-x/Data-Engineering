#!/usr/bin/python3

# %%
import sys, os, re
import csv, json
import pandas as pd
from textblob import TextBlob
from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

pd.set_option('display.max_columns', None)

class TweetStreamListener(StreamListener):
    """
        Th class get tweet in real time, store the tweet,
        monitors the frequency rate at which the tweets are tweeted and save it as csv.
        It also gets try to do simple sentimental analysis on each tweet based on the parameter that has set.

        NOTE: This class is specifically made for tweets that contains Trump and Biden but can be change for more usage
    """

    def __init__(self):
        """
            Necessary class varables are declared here and the file needed to start was created
        """


        # create the file path to store the data
        self.data_path = os.getcwd() + '/data_T_B.csv'
        with open(self.data_path, 'w') as f:
            self.fieldnames_d = ["x_value", 'trump', 'biden']
            writer = csv.DictWriter(f, fieldnames=self.fieldnames_d)
            writer.writeheader()

        # save tweets filepath
        self.tweet_path = os.getcwd() + '/tweets_T_B.csv'
        with open(self.tweet_path, 'w') as f:
            self.fieldnames_t = ["time", 'tweets']
            writer = csv.DictWriter(f, fieldnames=self.fieldnames_t)
            writer.writeheader()
        
        self.max_sec = 300

        self.x = []
        self.y = []
        self.store = []

        self.count_sec = 0
        self.count_t = 0
        self.count_b = 0
        self.last_ts = "0"


    def clean_text(self, text):
        """
            This is use to clear the tweets
        """

        text = re.sub(r'@[a-zA-Z0-9]+', "", text)  # remove all match @......
        text = re.sub(r'#', "", text) # Remove the '#' symbol
        text = re.sub(r'RT[\s]+', '', text) # Removing RT
        text = re.sub(r'https?:\/\/\S+', '', text)  #Removing hyper link

        return text


    def get_sentiment(self, score):
        """
            This is used to get the sentiment of the tweet
        """
        if score < 0:
            return "Negative"
        elif score == 0:
            return "Neutral"
        else:
            return "Positive"


    def on_data(self, data):
        """
            The data parameter is the tweet return from the streaming api
        """

        tweet = json.loads(data)                                                                       # convert json to dictionary
        if "created_at" in tweet:
            ts = tweet["created_at"][11:-11]                                                           # get time and text

            # try to get the tweet if it extended 
            try:
                get_data = [ tweet["created_at"], tweet.extended_tweet["full_text"] ] 
            except AttributeError:
                get_data = [ tweet["created_at"], tweet['text'] ]                                      # get the time only
            self.store.append(get_data)                                                                # save the data
            
            with open(self.tweet_path, 'a') as f:                                                   # append every new record
                writer = csv.DictWriter(f, fieldnames=self.fieldnames_t)
                
                info = {
                    'time': get_data[0],
                    'tweets': get_data[1]
                }
                writer.writerow(info)

            # if time (the seconds) is the same keep counting the incoming tweets
            if ts == self.last_ts:                                                                     # check if the last and current ts is diff
                if 'trump' in tweet['text'].lower():
                    self.count_t += 1
                if 'biden' in tweet['text'].lower():
                    self.count_b += 1

            else:                                                                                      # if the last and the current ts is diff, start another cycle
                self.x.append(len(self.x))  

                with open(self.data_path, 'a') as f:                                                   # append every new record
                    writer = csv.DictWriter(f, fieldnames=self.fieldnames_d)
                    
                    info = {
                        'x_value':len(self.x),
                        'trump': self.count_t,
                        'biden': self.count_b
                    }
                    writer.writerow(info)
                    print(f'{len(self.x)} | {self.count_t} | {self.count_b}')

                # reset all counts to 1 and make last_ts the current ts
                # self.count_sec = 1
                self.count_b = 1
                self.count_t = 1
                self.last_ts = ts

                if not len(self.x)%5:
                    # make a df and clean the tweets using the "clean_text" function defined above
                    df = pd.DataFrame(self.store, columns=['time', 'tweets']) 
                    df['tweets'] = df["tweets"].apply(self.clean_text)

                    # get polarity function from textblob
                    get_polarity = lambda x: TextBlob(x).sentiment.polarity
                    df["polarity"] = df["tweets"].apply(get_polarity).apply(self.get_sentiment)

                    # split df
                    df["trump"] = df["tweets"].apply(lambda x: 1 if "trump" in x.lower() else 0)
                    df["biden"] = df["tweets"].apply(lambda x: 1 if "biden" in x.lower() else 0)

                    trump = df[df['trump']==1]
                    biden = df[df['biden']==1]
                    
                    trump_pol = trump.polarity.value_counts()
                    biden_pol = biden.polarity.value_counts()
                    
                    # print(df.head())
                    self.sentiment_path = os.getcwd() + '/sentiment.csv'
                    with open(self.sentiment_path, 'w') as f:
                        self.fieldnames_s = ['Positive', 'Neutral', 'Negative']
                        writer = csv.DictWriter(f, fieldnames=self.fieldnames_s)
                        writer.writeheader()

                        #this is not fail if polarities are not found on the first run
                        try:
                            trump_info = {
                                'Positive':trump_pol.loc['Positive'],
                                'Neutral': trump_pol.loc['Neutral'],
                                'Negative': trump_pol.loc['Negative']
                            }
                            writer.writerow(trump_info)

                            biden_info = {
                                'Positive':biden_pol.loc['Positive'],
                                'Neutral': biden_pol.loc['Neutral'],
                                'Negative': biden_pol.loc['Negative']
                            }
                            writer.writerow(biden_info)
                        except Exception as e:
                            # print(e)
                            pass
                    

                if len(self.x) > self.max_sec:                                                             # break if false
                    # df = pd.DataFrame(self.store, columns=['time', 'tweets'])                              # store the data fetched into dataframe
                    # df.to_csv('tweets_T-B.csv')
                    return False



        return True
    
    def on_error(self, status):
        print(status)


auth = []
# make a file to store your twitter cred and get the path
path_a = os.getcwd() + '/auth'                                                              
f = open(path_a, "r")
for line in f:
    auth.append(line.strip())
f.close()

try:
# set your authentication and call the class
    listener = TweetStreamListener()
    auth_key = OAuthHandler(auth[0], auth[1])
    auth_key.set_access_token(auth[2], auth[3])
    live_twitter_stream = Stream(auth_key, listener)
    live_twitter_stream.filter(track=['Trump', 'Biden'])

except KeyboardInterrupt as e:
    sys.exit()


# %%
