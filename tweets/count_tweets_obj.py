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
    of = open('tweets_count_obj', 'w')
    for site in sites:
        filename = 'objective/' + site
        total_tweets = count_tweets(filename)
        output_line = '%s & %s \\\\ \hline\n' % (site, total_tweets)
        print output_line,
        of.write(output_line)
