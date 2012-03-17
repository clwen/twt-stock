import os

files = os.listdir('preprocessed/w5/')
for f in files:
    basename = f.split('.')[0]
    arffname = basename + '.arff'
    cmd = 'python build_arff.py %s %s' % (f, arffname)
    print cmd
    os.system(cmd)

