Generates tweet data using the [Twitter Streaming API](https://dev.twitter.com/streaming/overview) and then stores cleaned tweet along with keyphrase into an output file (data/tweet.txt). The example kp_listener uses 'Algorithm I' from the following paper: [Keyphrase Extraction Using Deep Recurrent Neural Networks on Twitter](http://jkx.fudan.edu.cn/~qzhang/paper/keyphrase.emnlp2016.pdf)


Requirements:
    - Requires Python 2.7 or higher


Dependencies:
-------------
    - tweepy (https://github.com/tweepy/tweepy)
        - pip install tweepy
    - tweet-preprocessor (https://github.com/s/preprocessor)
        - pip install tweet-preprocessor


Usage:
------
    - Run:
        - python ts_generator.py [-n <num_max_tweets>]
    - Custom Listener:
        - Inherit TSListener and override the methods filter_tweet and dump_tweet
        - Example of a custom listener: KPListener