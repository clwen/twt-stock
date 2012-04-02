import os
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: python build_test_arffs.py [week_number]'
        print 'ex: python build_test_arffs.py w6'
        sys.exit()

    week_number = sys.argv[1]
    files = os.listdir("preprocessed/%s/" % week_number)
    for f in files:
        basename = f.split('.')[0]
        arffname = basename + '.arff'
        cmd = 'time python build_arff.py %s %s' % (f, arffname)
        print cmd
        os.system(cmd)

