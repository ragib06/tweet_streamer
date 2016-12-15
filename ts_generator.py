import sys, json, time, getopt

import tweepy
from tweepy import OAuthHandler, Stream

from ts_stream_listener import TSListener
from kp_listener import KPListener
from ts_utils import TSUtils


AUTH_FILE = 'auth.json'
OUT_DIR = 'data'
OUT_FILE = 'tweets.txt'


NUM_MAX_TRENDS = 50
NUM_MAX_TWEETS = 50

# set your custom listener
TweetStreamListener = TSListener
# TweetStreamListener = KPListener


def enum(**enums):
    return type('Enum', (), enums)

Places = enum(CHICAGO=2379574, NEWYORK=2459115, SANFRANCISCO=2487956)


def authenticate(auth_data):
    #source: https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/
    auth = OAuthHandler(auth_data['consumer_key'], auth_data['consumer_secret'])
    auth.set_access_token(auth_data['access_token'], auth_data['access_secret'])
    api = tweepy.API(auth)
    return [auth, api]


def get_local_trends(api, woeid):
    local_trends = api.trends_place(woeid)
    local_trends = list(set([trend['name'] for trend in local_trends[0]['trends']]))
    return local_trends


def get_global_trends(api, max_trends=10):
    #WOEIDs (global: 1), (Chicago: 2379574), (New York: 2459115), (San Francisco: 2487956)
    #source: https://gist.github.com/lukemelia/353493

    local_trends = get_local_trends(api, Places.CHICAGO)
    global_trends = local_trends

    local_trends = get_local_trends(api, Places.NEWYORK)
    global_trends += local_trends

    local_trends = get_local_trends(api, Places.SANFRANCISCO)
    global_trends += local_trends

    global_trends = set(global_trends)
    global_trends = filter(lambda x: TSUtils.filterTrend(x), global_trends)
    global_trends = list(global_trends)

    return global_trends[0:max_trends]





def parse_cl_arguments():
    global NUM_MAX_TWEETS
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:", ["help", "output="])
    except getopt.GetoptError:
        # print help information and exit:
        print "option not recognized"

    for o, a in opts:
        if o == "-n":
            NUM_MAX_TWEETS = int(a)


def main():

    global AUTH_FILE, OUT_DIR, OUT_FILE, NUM_MAX_TRENDS, NUM_MAX_TWEETS

    parse_cl_arguments()

    with open(AUTH_FILE) as data_file:
        auth_data = json.load(data_file)

    [auth, api] = authenticate(auth_data)

    global_trends = get_global_trends(api, NUM_MAX_TRENDS)
    twitter_stream = Stream(auth, TweetStreamListener(api, NUM_MAX_TWEETS))
    twitter_stream.filter(track=global_trends)


if __name__ == '__main__':

    start_time = time.time()

    main()

    diff = (time.time() - start_time)

    hours, minutes, seconds  = diff / 3600, (diff % 3600) / 60, diff % 60

    print "--- Elapsed time %02d:%02d:%02d seconds ---" %  (hours, minutes, seconds)