Generates tweet data using the [Twitter Streaming API](https://dev.twitter.com/streaming/overview) and then stores cleaned tweet along with keyphrase into an output file (data/tweet.txt).

Requirements:
-------------
    - Requires Python 2.7 or higher


Register App with Twitter:
--------------------------
    - Go to http://apps.twitter.com and log in
    - Register a new application
    - You will receive a 'consumer key' and a 'consumer secret'
    - From the configuration page of your app, you can also get an 'access token' and an 'access token secret'
    - Put these four piece of information in the auth.json file


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
        - The example kp_listener uses 'Algorithm I' from the following paper: [Keyphrase Extraction Using Deep Recurrent
          Neural Networks on Twitter](http://jkx.fudan.edu.cn/~qzhang/paper/keyphrase.emnlp2016.pdf)
