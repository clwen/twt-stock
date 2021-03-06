import os
import sys
import operator

d = {}

def is_twt_time_format(s):
    return True if s.endswith(' +0000\n') or s.endswith(' +0000 2012\n') else False # TODO: use regex later

def count_ngram_from_file(filename):
    lines = open(filename).readlines()
    for line in lines:
        if is_twt_time_format(line): continue
        if line == '|\n': continue
        line = line.strip()
        tokens = line.split()
        # TODO: token should be viewed the same no matter capital or not
        # TODO: punctuation should be removed
        # TODO: count @, #, RT, URL
        for token in tokens:
            token = token.lower()
            if token not in d:
                d[token]  = 0
            else:
                d[token] += 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python count_ngram.py [objective or postive or negative] [top n]'
        sys.exit()

    if sys.argv[1] == 'positive':
        count_ngram_from_file('tweets/subjective/positive')
    elif sys.argv[1] == 'negative':
        count_ngram_from_file('tweets/subjective/negative')
    elif sys.argv[1] == 'subjective':
        count_ngram_from_file('tweets/subjective/positive')
        count_ngram_from_file('tweets/subjective/negative')
    elif sys.argv[1] == 'objective':
        for filename in os.listdir('tweets/objective/'):
            count_ngram_from_file('tweets/objective/' + filename)
    else:
        print 'error: wrong argument for filename'
        sys.exit()

    # sort d
    sd = sorted(d.iteritems(), key=operator.itemgetter(1), reverse=True)

    # write top n tokens to file
    output_file = 'ngrams/' + sys.argv[1]
    of = open(output_file, 'w')
    for ngram in sd:
        of.write(ngram[0] + '\n')
    of.close()
