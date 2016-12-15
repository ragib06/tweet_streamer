__author__ = 'ragib'

import re
from ts_utils import TSUtils


class KPUtils():

    @staticmethod
    def filterKPTweet(tweet):
        if not TSUtils.isEnglish(tweet):
            return True

        if tweet.find('RT') == 0:
            return True

        if tweet.find('@') == 0:
            return True

        if tweet.find('#') == -1:
            return True

        # ignore tweets with no or more than one hashtag
        hashtags = TSUtils.getAllHashtags(tweet)
        if len(hashtags) == 0 or len(hashtags) > 1:
            return True

        hashtag = hashtags[0]
        noUpper = not any([l for l in hashtag if l.isupper()])
        noLower = not any([l for l in hashtag if l.islower()])

        # ignore tweets with only lower or upper case letters
        if noUpper or noLower:
            return True

        # ignore tweets with three consecutive capital letters
        threeCaps = re.search(r"([^A-Z]*)([A-Z]{3})([^A-Z]*)", hashtag)
        if threeCaps is not None:
            return True

        return False

    @staticmethod
    def genY(tweet, keyphrase):
        tokens = tweet.split()
        y1 = map(lambda t: 1 if t in keyphrase.split() else 0, tokens)

        y2 = [-1] * len(tokens)

        indt = 0
        indk = tweet.find(keyphrase)
        for i in range(len(tokens)):
            if indt == indk:
                y2[i] = 0 if (len(keyphrase.split()) == 1) else 1
            elif indt < indk or indt > indk + len(keyphrase):
                y2[i] = 4
            elif indt + len(tokens[i]) == indk + len(keyphrase):
                y2[i] = 3
            else:
                y2[i] = 2

            indt += len(tokens[i]) + 1

        return [y1, y2]

    @staticmethod
    def testGenY():
        t = "go and vote for out idol nash for social media star"
        kp = "nash for social media star"
        [y1, y2] = KPUtils.genY(t, kp)

        y1t = [0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1]
        y2t = [4, 4, 4, 4, 4, 4, 1, 2, 2, 2, 3]

        assert(sorted(y1) == sorted(y1t) and sorted(y2) == sorted(y2t))
