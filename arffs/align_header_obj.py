import os
import random

weeks = ['w2', 'w3', 'w4', 'w5', 'w6', 'w7']

def find_and_replace(file_name, week, twt_name):
    file_name = week + '/' + file_name
    newlines = []
    with open(file_name, 'r') as f:
        for line in f.readlines():
            line = line.replace('positive', 'subjective')
            line = line.replace('negative', 'objective')
            newlines.append(line)
    with open(file_name, 'w') as f:
        for line in newlines:
            f.write(line)

if __name__ == '__main__':
    for week in weeks:
        print week
        files = os.listdir(week)
        for f in files:
            basename = f.split('.')[0]
            twt_name = basename + '.twt'
            print '\t' + twt_name
            find_and_replace(f, week, twt_name)
    
