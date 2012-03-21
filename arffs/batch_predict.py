import sys
import os

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage: python batch_predict.py [week_number]'
        print 'ex: python batch_predict.py w2'
        sys.exit()
    cur_week = sys.argv[1]
    files = os.listdir(cur_week)
    for f in files:
        base_name = f.split('.')[0]
        arff_file = cur_week + '/' + f
        output_file = '../outputs/' + cur_week + '/' + base_name + '.txt'
        cmd = 'java -cp ~/Applications/weka36/weka.jar weka.classifiers.functions.SMO -p 203 -l pos_neg.model -T %s > %s' % (arff_file, output_file)
        print cmd
        os.system(cmd)
