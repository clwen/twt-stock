import os

files = os.listdir('w2')
for f in files:
    base_name = f.split('.')[0]
    arff_file = 'w2/' + f
    output_file = '../outputs/w2/obj/' + base_name + '_obj.txt'
    cmd = 'java -cp ~/Applications/weka36/weka.jar weka.classifiers.functions.SMO -p 21 -l obj_subj.model -T %s > %s' % (arff_file, output_file)
    print cmd
    os.system(cmd)
