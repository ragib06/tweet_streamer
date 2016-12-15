import re
from tweepy.streaming import StreamListener
from ts_utils import TSUtils
from ts_cache import TSCache


class TSListener(StreamListener):

    OUT_DIR = 'data'
    OUT_FILE = 'tweets.txt'

    def __init__(self, api=None, max_count=10):
        super(StreamListener, self).__init__()

        self.num_tweets = 0
        self.api = api
        self.max_count = max_count
        self.cache = TSCache(500)
        self.out_file = TSUtils.prepare_output_file(self.OUT_DIR, self.OUT_FILE)

    def on_status(self, status):

        tweet = re.sub("\n", r" ", status.text)

        # basic filtering, ignore non-english characters
        if not TSUtils.isEnglish(tweet):
            return True

        tweet = TSUtils.cleanTweet(tweet)

        # ignore duplicates
        if self.cache.contains(tweet):
            return True

        self.cache.put(tweet)

        # filter out the tweet
        if self.filter_tweet(tweet):
            return True

        self.num_tweets += 1
        self.dump_tweet(tweet)

        if self.num_tweets == self.max_count:
            return False
        else:
            return True

    def filter_tweet(self, tweet):
        return False

    def dump_tweet(self, tweet):
        print self.num_tweets, "->", tweet
        self.out_file.write(tweet + "\n")

    def on_error(self, status):
        print(status)
        return True
