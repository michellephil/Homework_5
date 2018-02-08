from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
import nltk # import nltk # uncomment line after you install nltk

## SI 206 - HW
## COMMENT WITH:
## Your section day/time: Usually, 003 — Wed 9AM but for this assignment Tues at 2pm section
## Any names of people you worked with on this assignment: Monica Siegel, Tori Engler

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3: Caching
CACHE_FNAME = 'twitter_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

d = open(CACHE_FNAME, 'w')

#Finish parts 1 and 2 and then come back to this
#Code for Part 1:Get Tweets
def make_request_using_cache(username, num_tweets):
    twitter_url = 'https://api.twitter.com/1.1/search/tweets.json?q={}&count={}'.format(username, num_tweets)
    if twitter_url in CACHE_DICTION:
        print('Getting cached data...')
        d = CACHE_DICTION[twitter_url]
    else:
        print('Making a request for new data...')
        r = requests.get(twitter_url, auth = auth)
        d = json.loads(r.text)
        fw = open('tweet.json', 'w')
        fw.write(json.dumps(d, indent=4))
        fw.close()
        fw = open(CACHE_FNAME, 'w')
        CACHE_DICTION[twitter_url] = d
        fw.write(json.dumps(CACHE_DICTION))
        fw.close()
    tweets = ''
    for i in d['statuses']:
        tweets+=i['text']
    tokens = nltk.word_tokenize(tweets)
    freqDist = nltk.FreqDist(token for token in tokens if token.isalpha() and 'http' not in token and 'https' not in token and 'RT' not in token)
    #Code for Part 2:Analyze Tweets
    for word, frequency in freqDist.most_common(5):
        print(word + ' ' + str(frequency))
    return CACHE_DICTION[twitter_url]

make_request_using_cache(username, num_tweets)


if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
