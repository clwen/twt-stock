import sys
import re
from NLPlib import NLPlib

def is_twt_time_format(s):
    return True if s.endswith(' +0000\n') or s.endswith(' +0000 2012\n') else False # TODO: use regex later

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python preprocess.py [raw-tweet-file]'
        sys.exit()

    input_path = 'tweets/objective/' + sys.argv[1]
    output_path = 'preprocessed/objective/' + sys.argv[1] + '.twt'
    of = open(output_path, 'w+')
    tagger = NLPlib()
    lines = open(input_path).readlines()
    for line in lines:
        if line == '|\n': # skip tweets delimiters
            of.write(line)
            continue
        if is_twt_time_format(line):
            continue

        line = re.sub(r'<.+?>', '', line) # remove html tags
        line = re.sub(r'&amp;', '&', line)
        line = re.sub(r'https?://\S+', '', line)

        # sentence segmentation
        sentence_boundary = re.compile(r'[.?!]+ ')
        sentences = sentence_boundary.split(line)
        for i in range(len(sentences)):
            input_sentence = sentences[i]
            # split sentence into tokens
            raw_tokens = input_sentence.strip().split()
            # deal with special cases
            tokens = []
            for token in raw_tokens:
                if not token[-1].isalnum(): # for commas, other punctuation
                    tokens.append(token[:-1])
                    tokens.append(token[-1])
                elif token[0] == '(':
                    tokens.append('(')
                    tokens.append(token[1:])
                elif token.find('....') != -1: # for ellipses
                    tokens.extend(token.split('....'))
                    tokens.append('....')
                elif token.find('...') != -1: # for ellipses
                    tokens.extend(token.split('...'))
                    tokens.append('...')
                else:
                    tokens.append(token)
            # tag tokens with NLPlib
            tags = tagger.tag(tokens)
            assert len(tokens) == len(tags)
            tokens_w_tags = []
            for j in range(len(tokens)):
                tokens_w_tags.append(tokens[j] + '/' + tags[j])
            output_sentence = ' '.join(tokens_w_tags)
            print output_sentence
            # print tags
            output_sentence += '\n'
            of.write(output_sentence)

