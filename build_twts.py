import os

if __name__ == '__main__':
    target_dir = 'tweets/w6/'
    # traverse tweets dir, for each file
    for filename in os.listdir(target_dir):
        if filename[0] == '.': # skip the swp file
            continue

        if os.path.isdir(target_dir + filename): # skip dirs
            continue

        # run twtt.py with specifying the filename
        twtt_cmd = 'python preprocess.py ' + filename
        print twtt_cmd
        os.system(twtt_cmd)
