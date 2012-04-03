import os

companies = ['apple', 'google', 'microsoft', 'amazon', 'rim', 'dell', 'intel', 'yahoo', 'nvidia', 'netflix']
weeks = ['w1', 'w2', 'w3', 'w4', 'w5', 'w6', 'w7']

def count_pos_neg(week, fname):
    pos_num = 0
    neg_num = 0
    # return the number of positive and negative tweets
    input_path = week + '/' + fname
    print input_path
    lines = open(input_path, 'r').readlines()
    # ignore the first 5 lines: just header from output of WEKA
    # last line is also an empty line
    lines = lines[5:-1]
    for line in lines:
        tokens = line.split()
        pos_neg = tokens[2].split(':')[1]
        if pos_neg == 'positive':
            pos_num += 1
        elif pos_neg == 'negative':
            neg_num += 1
        else:
            raise UnknowPosNegTypeError

    return (pos_num, neg_num)

if __name__ == '__main__':
    for company in companies:
        output_path = company
        of = open(output_path, 'w')
        print "calculating ratio for %s..." % (company)
        ratio = []
        for week in weeks:
            total_pos = 0
            total_neg = 0
            # traverse the directory
            files = os.listdir(week)
            for f in files:
                # if it's start with the company name, calculate the pos and neg number
                if f.startswith(company):
                    (positive, negative) = count_pos_neg(week, f)
                    print ' week %s file %s pos %s neg %s' % (week, f, positive, negative) 
                    total_pos += positive
                    total_neg += negative

            # write the ratio list to file
            pos_ratio = float(total_pos) / (float(total_pos) + float(total_neg))
            output_line = '%s %s %s\n' % (pos_ratio, total_pos, total_neg)
            of.write(output_line)
