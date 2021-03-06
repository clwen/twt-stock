import sys
import itertools
from collections import OrderedDict

fp_words = []
sp_words = []
tp_words = []
conj_words = []
common_nouns = ['NN', 'NNS']
proper_nouns = ['NNP', 'NNPS']
adverbs = ['RB', 'RBR', 'RBS']
wh_words = ['WDT', 'WP', 'WP$', 'WRB']
past_words = ['VBD', 'VBN']
future_words = ['MD']
slang_words = []
unigrams = OrderedDict()
# bigrams = OrderedDict()

def import_words_from_file(filename):
    # import feature word lists
    wl_path = 'Wordlists/'
    file_path = wl_path + filename
    words = []
    lines = open(file_path).readlines()
    for line in lines:
        line = line.strip()
        words.append(line)
        words.append(line.upper())
        words.append(line[0].upper() + line[1:])
    return words

def extract_feature_words():
    global fp_words
    global sp_words
    global tp_words
    global conj_words
    global slang_words
    fp_words = import_words_from_file('First-person')
    sp_words = import_words_from_file('Second-person')
    tp_words = import_words_from_file('Third-person')
    conj_words = import_words_from_file('Conjunct')
    slang_words = import_words_from_file('Slang')

def load_unigrams():
    global unigrams
    keywords = []
    with open('ngrams/unigram') as f:
        lines = f.readlines()
        for line in lines:
            keyword = (line.strip(), 0)
            keywords.append(keyword)
    unigrams = OrderedDict(keywords)

def load_bigrams():
    global bigrams
    keywords = []
    with open('bigrams/bigrams') as f:
        lines = f.readlines()
        for line in lines:
            keyword = (line.strip(), 0)
            keywords.append(keyword)
    bigrams = OrderedDict(keywords)

def all_capital(word):
    return True if len(word) >= 2 and all(c.isupper() for c in word) else False

def class_name_defined(s):
    return False if s.find(':') == -1 else True

def output_preamble(output_file, classes):
    global unigrams
    with open(output_file, 'w') as f:
        # write relation
        f.write('@relation twt_sentiment_analysis\n\n')
        # write attributes TODO: can be automatic
        f.write('@attribute 1st_person numeric\n')
        f.write('@attribute 2st_person numeric\n')
        f.write('@attribute 3rd_person numeric\n')
        f.write('@attribute coordinate_conj numeric\n')
        f.write('@attribute past_tense numeric\n')
        f.write('@attribute future_tense numeric\n')
        f.write('@attribute commas numeric\n')
        f.write('@attribute colons numeric\n')
        f.write('@attribute dashes numeric\n')
        f.write('@attribute parentheses numeric\n')
        f.write('@attribute ellipses numeric\n')
        f.write('@attribute common_nouns numeric\n')
        f.write('@attribute proper_nouns numeric\n')
        f.write('@attribute adverbs numeric\n')
        f.write('@attribute wh_words numeric\n')
        f.write('@attribute slangs numeric\n')
        f.write('@attribute all_capital numeric\n')
        f.write('@attribute avg_sentence_in_tokens numeric\n')
        f.write('@attribute avg_token_in_chars numeric\n')
        f.write('@attribute sentence_num numeric\n')
        # write preambles for unigrams
        n = 1
        for unigram, freq in unigrams.items():
            f.write("@attribute %s numeric\n" % ('unigram' + str(n)))
            n += 1
        # write preambles for bigrams
        # n = 1
        # for bigram, freq in bigrams.items():
        #     f.write("@attribute %s numeric\n" % ('bigram' + str(n)))
        #     n += 1
        # write classes
        class_s = '@attribute twit {' + ', '.join(classes.keys()) + '}\n\n'
        f.write(class_s)
        # write data prompt
        f.write('@data\n')

def count_bigram_features(line):
    global bigrams
    tokens = line.split()
    for i in range(0, len(tokens)-1):
        first_token = tokens[i].split('/')[0].lower()
        second_token = tokens[i+1].split('/')[0].lower()
        cur_bigram = "%s %s" % (first_token, second_token)
        for bigram, freq in bigrams.items():
            if cur_bigram == bigram:
                # print 'got bigram %s' % (cur_bigram)
                bigrams[cur_bigram] += 1

def extract_features(class_name, twt_file, week, output_file):
    # open output file in append mode
    of = open(output_file, 'a')

    # feature count
    fcnt = OrderedDict([('first_person', 0), ('second_person', 0), ('third_person', 0), ('conjunction', 0), ('past_tense', 0), ('future_tense', 0), ('comma', 0), ('colon', 0), ('dash', 0), ('parentheses', 0), ('ellipse', 0), ('common_noun', 0), ('proper_noun', 0), ('adverb', 0), ('wh', 0), ('slang', 0), ('all_capital', 0), ('avg_sentence_in_tokens', 0), ('avg_token_in_chars', 0), ('sentence_num', 0)])
    sentence_in_tokens = []
    global unigrams
    # global bigrams

    # input_path = 'preprocessed/' + week + '/' + twt_file
    input_path = 'preprocessed/' + twt_file
    # read lines from .twt file
    lines = open(input_path).readlines()
    # process lines one by one
    twt_buf = ''
    for line in lines:
        # if it's not '|', append it to buffer
        if line != '|\n':
            twt_buf += line.strip()
            sentence_in_tokens.append(len(line.strip().split()))
            fcnt['sentence_num'] += 1
            continue
        # else, if it's '|', process all the tokens in buffer
        # decompose to tokens
        tokens = twt_buf.split()
        # decompose to words and tags
        for token in tokens:
            # print token,
            try:
                (word, tag) = token.split('/')
            except ValueError:
                continue
            # check if it's in the feature list
            if word in fp_words:
                fcnt['first_person'] += 1
            if word in sp_words:
                fcnt['second_person'] += 1
            if word in tp_words:
                fcnt['third_person'] += 1
            if word in conj_words:
                fcnt['conjunction'] += 1
            if tag in past_words:
                fcnt['past_tense'] += 1
            if tag in future_words:
                fcnt['future_tense'] += 1
            if word == ',':
                fcnt['comma'] += 1
            if word == ':' or word == ';':
                fcnt['colon'] += 1
            if word == '-':
                fcnt['dash'] += 1
            if word == '(' or word == ')':
                fcnt['parentheses'] += 1
            if word == '....' or word == '...':
                fcnt['ellipse'] += 1
            if tag in common_nouns:
                fcnt['common_noun'] += 1
            if tag in proper_nouns:
                fcnt['proper_noun'] += 1
            if tag in adverbs:
                fcnt['adverb'] += 1
            if tag in wh_words:
                fcnt['wh'] += 1
            if word in slang_words:
                fcnt['slang'] += 1
            if all_capital(word):
                fcnt['all_capital'] += 1
            # count average length of sentences in tokens
            fcnt['avg_sentence_in_tokens'] = float(sum(sentence_in_tokens)) / len(sentence_in_tokens)
            fcnt['avg_token_in_chars'] = float(sum(len(t) for t in tokens)) / len(tokens) # should exclude punctuation
            # count for unigram features 
            for u, v in unigrams.items():
                if word == u:
                    unigrams[u] += 1
        # count for bigram features
        # count_bigram_features(twt_buf)

        # write to output file # TODO: use fcnt
        output_line = ','.join(str(f) for f in fcnt.values())
        output_line += ',' + ','.join(str(f) for u, f in unigrams.items())
        # output_line += ',' + ','.join(str(f) for u, f in bigrams.items())
        output_line += ',' + class_name + '\n'
        of.write(output_line)

        # clean buffer and counters for next tweet
        twt_buf = ''
        fcnt = OrderedDict([('first_person', 0), ('second_person', 0), ('third_person', 0), ('conjunction', 0), ('past_tense', 0), ('future_tense', 0), ('comma', 0), ('colon', 0), ('dash', 0), ('parentheses', 0), ('ellipse', 0), ('common_noun', 0), ('proper_noun', 0), ('adverb', 0), ('wh', 0), ('slang', 0), ('all_capital', 0), ('avg_sentence_in_tokens', 0), ('avg_token_in_chars', 0), ('sentence_num', 0)])
        sentence_in_tokens = []
        # clean unigrams to zeros
        for u, v in unigrams.items():
            unigrams[u] = 0
        # clean bigrams to zeros
        # for u, v in bigrams.items():
        #     bigrams[u] = 0

    # close output file
    of.close()

if __name__ == '__main__':
    # parse arguments
    # if only one argument provided, ask user to run it again
    if len(sys.argv) <= 2:
        print "usage: python buildarff.py [class files] [week] [output file]"
        print "ex: python buildarff.py apple_iphone.twt w6 apple_iphone.arff"
        sys.exit()
    # get current week number
    week = sys.argv[-2]
    # prepare output file according to last argument
    # output_file = 'arffs/' + week + '/' + sys.argv[-1]
    output_file = 'arffs/' + sys.argv[-1]
    # from 2nd argument to 2nd from the last it's the class definition
    classes = {}
    for i in range(1, len(sys.argv)-2):
        cur_arg = sys.argv[i]
        if class_name_defined(cur_arg):
            arg_splitted = cur_arg.split(':')
            class_name = arg_splitted[0]
            files = arg_splitted[1].split('+')
        else:
            class_name = cur_arg
            files = cur_arg.split('+')
        classes[class_name] = files
    print classes

    extract_feature_words()
    load_unigrams()
    # load_bigrams()
    output_preamble(output_file, classes)

    for (class_name, files) in classes.iteritems():
        for twt_file in files:
            print '%s, %s' % (class_name, twt_file)
            extract_features(class_name, twt_file, week, output_file)

