import os
from collections import OrderedDict as odict

sites = ['TechCrunch', 'CNETNews', 'RWW', 'mashable', 'Gizmodo', 'gigaom', 'allthingsd', 'TheNextWeb', 'verge', 'Wired', 'nytimesbits', 'WSJTech', 'SAI', 'guardiantech', 'HuffPostTech']

def count_tweets(filename):
    tweets_count = 0
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == '|':
                tweets_count += 1
    return tweets_count

if __name__ == '__main__':
    pos = count_tweets('subjective/positive')
    neg = count_tweets('subjective/negative')
    print 'positive: %s, negative: %s' % (pos, neg)
        
