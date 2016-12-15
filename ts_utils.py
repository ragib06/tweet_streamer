import re, sys, os, shutil, time

import preprocessor as tp


class TSUtils():

    @staticmethod
    def prepare_output_file(dirname, filename):
        full_path = dirname + '/' + filename
        print 'output:', full_path
        if os.path.isfile(full_path):
            shutil.copyfile(full_path, dirname + '/' + str(int(time.time())) + "." + filename)

        out = open(full_path, 'w')
        return out

    @staticmethod
    def isEnglish(s):
        try:
            s.decode('ascii')
        except UnicodeEncodeError:
            return False
        else:
            return True

    @staticmethod
    def getAllHashtags(tweet):
        return re.findall(r"#(\w+)", tweet)

    @staticmethod
    def filterTrend(trend):
        if TSUtils.isEnglish(trend) == False:
            return False

        hashtags = TSUtils.getAllHashtags(trend)

        if len(hashtags) == 0:
            return True

        hashtag = hashtags[0]

        noUpper = not any([l for l in hashtag if l.isupper()])
        noLower = not any([l for l in hashtag if l.islower()])

        if noUpper or noLower:
            return False

        threeCaps = re.search(r"([^A-Z]*)([A-Z]{3})([^A-Z]*)", hashtag)
        if threeCaps is not None:
            return False

        return True


    @staticmethod
    def cleanTweet(tweet):
        tp.set_options(tp.OPT.URL, tp.OPT.MENTION, tp.OPT.EMOJI, tp.OPT.SMILEY, tp.OPT.NUMBER)
        tweet = tp.clean(tweet)
        tweet = re.sub(r"[\.\,\-\_\!\(\)\{\}\[\]\:\;\"\\\/\=]","", tweet).strip()
        tweet = re.sub(' +',' ', tweet)
        tweet = re.sub('\?+','?', tweet)
        tweet = re.sub('&gt','', tweet)
        tweet = re.sub('&amp','', tweet)
        return tweet

    @staticmethod
    def getKeyPhrase(tweet):
        hashtag = TSUtils.getAllHashtags(tweet)[0]
        hashtag = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', hashtag)
        hashtag = re.sub('([a-z0-9])([A-Z])', r'\1 \2', hashtag).lower()
        return hashtag

    @staticmethod
    def replaceHashtag(tweet, str):
        hashtag = TSUtils.getAllHashtags(tweet)[0]
        return tweet.replace("#" + hashtag, str)



