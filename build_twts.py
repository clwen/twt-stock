import os

if __name__ == '__main__':
    # traverse tweets dir, for each file
    for filename in os.listdir('tweets'):
        if filename[0] == '.': # skip the swp file
            continue

        # run twtt.py with specifying the filename
        twtt_cmd = 'python preprocess.py ' + filename
        os.system(twtt_cmd)
