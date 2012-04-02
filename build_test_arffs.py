import os
import sys

weeks = ['w5', 'w6', 'w7']

if __name__ == '__main__':
    # if len(sys.argv) < 2:
    #     print 'usage: python build_test_arffs.py [week_number]'
    #     print 'ex: python build_test_arffs.py w6'
    #     sys.exit()

    for week in weeks:
        files = os.listdir("preprocessed/%s/" % week)
        for f in files:
            basename = f.split('.')[0]
            arffname = basename + '.arff'
            cmd = 'python build_arff.py %s %s %s' % (f, week, arffname)
            print cmd
            os.system(cmd)

