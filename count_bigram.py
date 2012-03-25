import os
import sys
import operator

d = {}

def is_twt_time_format(s):
    return True if s.endswith(' +0000\n') or s.endswith(' +0000 2012\n') else False # TODO: use regex later

def count_bigram_from_file(filename):
    lines = open(filename).readlines()
    for line in lines:
        if is_twt_time_format(line): continue
        if line == '|\n': continue
        line = line.strip()
        tokens = line.split()
        # TODO: punctuation should be removed
        # TODO: count @, #, RT, URL
        for i in range(0, len(tokens)-1):
            first_token = tokens[i].lower()
            second_token = tokens[i+1].lower()
            bigram = "%s %s" % (first_token, second_token)
            if bigram not in d:
                d[bigram]  = 0
            else:
                d[bigram] += 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python count_bigram.py [objective or postive or negative] [top n]'
        print 'ex: python count_bigram.py objective 3000'
        sys.exit()

    if sys.argv[1] == 'positive':
        count_bigram_from_file('tweets/subjective/positive')
    elif sys.argv[1] == 'negative':
        count_bigram_from_file('tweets/subjective/negative')
    elif sys.argv[1] == 'subjective':
        count_bigram_from_file('tweets/subjective/positive')
        count_bigram_from_file('tweets/subjective/negative')
    elif sys.argv[1] == 'objective':
        for filename in os.listdir('tweets/objective/'):
            count_bigram_from_file('tweets/objective/' + filename)
    else:
        print 'error: wrong argument for filename'
        sys.exit()

    # sort d
    sd = sorted(d.iteritems(), key=operator.itemgetter(1), reverse=True)

    # write top n tokens to file
    output_file = 'bigrams/' + sys.argv[1]
    of = open(output_file, 'w')
    topn = int(sys.argv[2])
    sd = sd[:topn]
    for bigram in sd:
        of.write(bigram[0] + '\n')
    of.close()
