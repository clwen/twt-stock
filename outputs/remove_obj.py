import os

def build_obj_dic(obj_file):
    obj_dic = {}
    with open(obj_file, 'r') as f:
        lines = f.readlines()
        lines = lines[5:-1]
        for line in lines:
            # print line,
            tokens = line.split()
            tweets_id = tokens[0]
            objectivity = tokens[2].split(':')[1]
            # print '\t%s\t%s' % (tweets_id, objectivity)
            obj_dic[tweets_id] = objectivity
    return obj_dic

def remove_obj(obj_file, pos_file):
    pos_fp = open(pos_file, 'r')

    # traverse obj_file and build dictionary about objectivity
    obj_dic = build_obj_dic(obj_file)
    # print obj_dic

    # traverse pos_file, if it's subjective, put into newlines
    newlines = []
    with open(pos_file, 'r') as f:
        lines = f.readlines()
        newlines.extend(lines[:5]) # in accordance to original format, added header five lines
        lines = lines[5:-1]
        for line in lines:
            # print line,
            tokens = line.split()
            tweets_id = tokens[0]
            if obj_dic[tweets_id] == 'subjecti':
                # print line,
                newlines.append(line)
        newlines.append('   \n')

    # write newlines to pos_file
    with open(pos_file, 'w') as f:
        for line in newlines:
            f.write(line)
    
if __name__ == '__main__':
    files = os.listdir('w2')
    for f in files:
        if f == 'obj' or f == 'back' or f.endswith('swp'):
            continue
        pos_file = 'w2/' + f
        base_name = f.split('.')[0]
        obj_file = 'w2/obj/' + base_name + '_obj.txt'
        print pos_file + '\t' + obj_file
        remove_obj(obj_file, pos_file)
