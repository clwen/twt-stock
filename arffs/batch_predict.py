import sys
import os

weeks = ['w6', 'w7']

if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print 'usage: python batch_predict.py [week_number]'
    #     print 'ex: python batch_predict.py w2'
    #     sys.exit()

    # week = sys.argv[1]
    for week in weeks:
        files = os.listdir(week)
        for f in files:
            base_name = f.split('.')[0]
            arff_file = week + '/' + f
            output_file = '../outputs/' + week + '/' + base_name + '.txt'
            cmd = 'java -Xms512m -Xmx1024m -cp ~/Applications/weka36/weka.jar weka.classifiers.trees.RandomForest -p 1064 -l pos_neg.model -T %s > %s' % (arff_file, output_file)
            print cmd
            os.system(cmd)
