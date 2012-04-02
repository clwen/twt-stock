import sys
import os
import random

weeks = ['w1']

def find_and_replace(week, file_name, twt_name):
    file_name = week + '/' + file_name
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

if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print 'usage: python align_header.py [week_number]'
    #     print 'ex: python align_header.py w2'
    #     sys.exit()
    
    for week in weeks:
        files = os.listdir(week)
        for f in files:
            basename = f.split('.')[0]
            twt_name = basename + '.twt'
            print twt_name
            find_and_replace(week, f, twt_name)
    
