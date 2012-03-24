import os
from collections import OrderedDict as odict

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
    of = open('tweets_count', 'w')
    for company, keywords in companies.items():
        for keyword in keywords:
            total_tweets = 0
            for week in weeks:
                filename = "%s/%s_%s" % (week, company, keyword)
                total_tweets += count_tweets(filename)
            output_line = '%s &  \#%s & %s \\\\ \hline\n' % (company, keyword, total_tweets)
            print output_line,
            of.write(output_line)
