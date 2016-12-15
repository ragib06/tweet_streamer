from ts_stream_listener import TSListener
from ts_utils import TSUtils
from kp_utils import KPUtils


class KPListener(TSListener):

    Y1_FILE = 'y1.txt'
    Y2_FILE = 'y2.txt'

    def __init__(self, api=None, max_count=10):
        super(KPListener, self).__init__(api, max_count)
        self.y1_file = TSUtils.prepare_output_file(self.OUT_DIR, self.Y1_FILE)
        self.y2_file = TSUtils.prepare_output_file(self.OUT_DIR, self.Y2_FILE)
        KPUtils.testGenY()

    def filter_tweet(self, tweet):
        return KPUtils.filterKPTweet(tweet)

    def dump_tweet(self, tweet):
        keyphrase = TSUtils.getKeyPhrase(tweet)

        print self.num_tweets, "->", tweet, "=>", keyphrase

        tweet = TSUtils.replaceHashtag(tweet, keyphrase)

        [y1, y2] = KPUtils.genY(tweet, keyphrase)

        print 'y1:', y1
        print 'y2:', y2

        self.out_file.write(tweet + "," + keyphrase + "\n")
        self.y1_file.write(",".join([str(b) for b in y1]) + "\n")
        self.y2_file.write(",".join([str(b) for b in y2]) + "\n")

