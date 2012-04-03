import os

weeks = ['w2', 'w3', 'w4', 'w5', 'w6', 'w7']

if __name__ == '__main__':
    for week in weeks:
        files = os.listdir(week)
        for f in files:
            base_name = f.split('.')[0]
            arff_file = week + '/' + f
            output_file = '../outputs/%s/obj/%s_obj.txt' % (week, base_name)
            cmd = 'java -Xms512m -Xmx1024m -cp ~/Applications/weka36/weka.jar weka.classifiers.trees.RandomForest -p 1064 -l obj_subj.model -T %s > %s' % (arff_file, output_file)
            print cmd
            os.system(cmd)
