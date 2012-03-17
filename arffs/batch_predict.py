import os

files = os.listdir('w5')
for f in files:
    base_name = f.split('.')[0]
    arff_file = 'w5/' + f
    output_file = '../outputs/w5/' + base_name + '.txt'
    cmd = 'java -cp ~/Applications/weka36/weka.jar weka.classifiers.functions.SMO -p 21 -l pos_neg.model -T %s > %s' % (arff_file, output_file)
    print cmd
    os.system(cmd)
