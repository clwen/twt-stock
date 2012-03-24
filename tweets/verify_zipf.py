import os
import operator
from collections import OrderedDict as odict
from rpy2 import robjects
r = robjects.r

companies = odict(
        [('apple', ['apple', 'iphone', 'iphone4s', 'iphone4', 'siri', 'ipod', 'mac', 'macintosh', 'itunes', 'ios']),
        ('google', ['google', 'android', 'droid', 'googleplus', 'gplus', 'gmail', 'youtube', 'chrome', 'googlemap', 'gmap']),
        ('microsoft', ['windows', 'windows8', 'xbox', 'xbox360', 'kinect', 'msn', 'bing', 'ie']),
        ('amazon', ['amazon', 'kindle', 'kindlefire']),
        ('rim', ['rim', 'blackberry']),
        ('dell', ['dell']),
        ('intel', ['intel', 'xeon']),
        ('yahoo', ['yahoo', 'yahoomail', 'ymail', 'yim']),
        ('nvidia', ['nvidia', 'tegra', 'tegra3', 'geforce']),
        ('netflix', ['netflix'])
        ])
weeks = ['w1', 'w2', 'w3', 'w4', 'w5']

token_freq = {}
freqs = {}

def count_tokens(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            tokens = line.split()
            for token in tokens:
                token = token.lower()
                if token not in token_freq:
                    token_freq[token] = 1
                else:
                    token_freq[token] += 1

if __name__ == '__main__':
    # construct freqency table for each token
    print 'constrcting freq table'
    for company, keywords in companies.items():
        for keyword in keywords:
            total_tweets = 0
            for week in weeks:
                filename = "%s/%s_%s" % (week, company, keyword)
                print filename
                count_tokens(filename)

    # sort by freq
    print 'sort by freq'
    sorted_freq = sorted(token_freq.iteritems(), key=operator.itemgetter(1), reverse=True)

    # extract freqency part (value) in sorted_freq
    print 'extract freq in sorted freq'
    freq_list = []
    for token, freq in sorted_freq:
        freq_list.append(freq)

    # plot according to values of freq times table
    print 'plotting...'
    freq_list = freq_list[:2000]
    x = range(1, len(freq_list)+1)
    r.png('zipf.png')
    r.plot(x, freq_list, xlab='rank', ylab='frequency')
