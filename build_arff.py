import sys
import itertools

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
slang_words = ['smh', 'fwb', 'lmfao', 'lmao', 'lms', 'tbh', 'rofl', 'wtf', 'bff', 'wyd', 'lylc', 'brb', 'atm', 'imao', 'sml', 'btw', 'bw', 'imho', 'fyi', 'ppl', 'sob', 'ttyl', 'imo', 'ltr', 'thx', 'kk', 'omg', 'ttys', 'afn', 'bbs', 'cya', 'ez', 'f2f', 'gtr', 'ic', 'jk', 'k', 'ly', 'ya', 'nm', 'np', 'plz', 'ru', 'so', 'tc', 'tmi', 'ym', 'ur', 'u', 'sol'] # TODO: move it to a file

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
    fp_words = import_words_from_file('First-person')
    sp_words = import_words_from_file('Second-person')
    tp_words = import_words_from_file('Third-person')
    conj_words = import_words_from_file('Conjunct')

def all_capital(word):
    return True if len(word) >= 2 and all(c.isupper() for c in word) else False

def class_name_defined(s):
    return False if s.find(':') == -1 else True

def output_preamble(output_file, classes):
    # open output file in open mode
    f = open(output_file, 'w')
    # write relation
    f.write('@relation twit_classification\n\n')
    # write attributes
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
    # write classes
    class_s = '@attribute twit {' + ', '.join(classes.keys()) + '}\n\n'
    f.write(class_s)
    # write data prompt
    f.write('@data\n')
    # close output file
    f.close()

def extract_features(class_name, twt_file, output_file):
    # open output file in append mode
    of = open(output_file, 'a')

    fp_count = 0
    sp_count = 0
    tp_count = 0
    conj_count = 0
    past_count = 0
    future_count = 0
    comma_count = 0
    colon_count = 0
    dash_count = 0
    paren_count = 0
    ellipse_count = 0
    common_nouns_count = 0
    proper_nouns_count = 0
    adverbs_count = 0
    wh_count = 0
    slang_count = 0
    all_capital_count = 0
    sentence_in_tokens = []
    avg_sentence_in_tokens = 0
    sentence_num = 0

    input_path = 'twts/' + twt_file
    # read lines from .twt file
    lines = open(input_path).readlines()
    # process lines one by one
    twt_buf = ''
    for line in lines:
        # if it's not '|', append it to buffer
        if line != '|\n':
            twt_buf += line.strip()
            sentence_in_tokens.append(len(line.strip().split()))
            sentence_num += 1
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
                fp_count += 1
            if word in sp_words:
                sp_count += 1
            if word in tp_words:
                tp_count += 1
            if word in conj_words:
                conj_count += 1
            if tag in past_words:
                past_count += 1
            if tag in future_words:
                future_count += 1
            if word == ',':
                comma_count += 1
            if word == ':' or word == ';':
                colon_count += 1
            if word == '-':
                dash_count += 1
            if word == '(' or word == ')':
                paren_count += 1
            if word == '....' or word == '...':
                ellipse_count += 1
            if tag in common_nouns:
                common_nouns_count += 1
            if tag in proper_nouns:
                proper_nouns_count += 1
            if tag in adverbs:
                adverbs_count += 1
            if tag in wh_words:
                wh_count += 1
            if word in slang_words:
                slang_count += 1
            if all_capital(word):
                all_capital_count += 1
            # count average length of sentences in tokens
            avg_sentence_in_tokens = float(sum(sentence_in_tokens)) / len(sentence_in_tokens)
            avg_token_in_chars = float(sum(len(t) for t in tokens)) / len(tokens) # should exclude punctuation
        # write to output file
        of.write(str(fp_count) + ',' + str(sp_count) + ',' + str(tp_count) + ',' + str(conj_count) + ',' + str(past_count) + ',' + str(future_count) + ',' + str(comma_count) + ',' + str(colon_count) + ',' + str(dash_count) + ',' + str(paren_count) + ',' + str(ellipse_count) + ',' + str(common_nouns_count) + ',' + str(proper_nouns_count) + ',' + str(adverbs_count) + ',' + str(wh_count) + ',' + str(slang_count) + ',' + str(all_capital_count) + ',' + str(avg_sentence_in_tokens) + ',' + str(avg_token_in_chars) + ',' + str(sentence_num) + ',' + class_name + '\n')
        # clean the buffer for next tweet
        twt_buf = ''
        fp_count = 0
        sp_count = 0
        tp_count = 0
        conj_count = 0
        past_count = 0
        future_count = 0
        comma_count = 0
        colon_count = 0
        dash_count = 0
        paren_count = 0
        ellipse_count = 0
        common_nouns_count = 0
        proper_nouns_count = 0
        adverbs_count = 0
        wh_count = 0
        slang_count = 0
        all_capital_count = 0
        sentence_in_tokens = []
        avg_sentence_in_tokens = 0
        sentence_num = 0

    # close output file
    of.close()

if __name__ == '__main__':
    # parse arguments
    # if only one argument provided, ask user to run it again
    if len(sys.argv) <= 1:
        print "Usage: python buildarff.py [class files] [output file]"
        sys.exit()
    # prepare output file according to last argument
    output_file = 'arffs/' + sys.argv[-1]
    # from 2nd argument to 2nd from the last it's the class definition
    classes = {}
    for i in range(1, len(sys.argv)-1):
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

    output_preamble(output_file, classes)

    extract_feature_words()

    for (class_name, files) in classes.iteritems():
        for twt_file in files:
            print '%s, %s' % (class_name, twt_file)
            extract_features(class_name, twt_file, output_file)

