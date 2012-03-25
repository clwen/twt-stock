import copy

emoticons = [':)', ':d', ':p', ':-)', ':(', ':-(']

def contain_emoticons(line):
    tokens = line.split()
    for token in tokens:
        if token in emoticons:
            return True
    return False

def load_from_file(filename):
    words = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        lines = lines[:100]
        for line in lines:
            if contain_emoticons(line):
                continue
            else:
                words.append(line.strip())
    return words

if __name__ == '__main__':
    pos = load_from_file('positive')
    neg = load_from_file('negative')
    bigrams = copy.deepcopy(pos)

    for word in neg:
        if word not in pos:
            bigrams.append(word)

    print bigrams
    print len(bigrams)

    # write bigrams to file
    with open('bigram', 'w') as f:
        for u in bigrams:
            f.write(u + '\n')
