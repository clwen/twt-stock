import os
import random

def find_and_replace(file_name, twt_name):
    file_name = 'w4/' + file_name
    newlines = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            line = line.replace('{' + twt_name + '}', '{positive, negative}')
            if random.random() < 0.5:
                line = line.replace(twt_name, 'positive')
            else:
                line = line.replace(twt_name, 'negative')
            newlines.append(line)
    with open(file_name, 'w') as f:
        for line in newlines:
            f.write(line)

files = os.listdir('w4/')
for f in files:
    basename = f.split('.')[0]
    twt_name = basename + '.twt'
    print twt_name
    find_and_replace(f, twt_name)
    
