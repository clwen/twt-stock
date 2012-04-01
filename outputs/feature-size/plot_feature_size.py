from rpy2 import robjects
r = robjects.r

raw_sizes = range(100, 2001, 100)
classifiers = ['bayes', 'svm', 'tree', 'forest']

def load_accuracies(classifier):
    global raw_sizes
    accuracies = []
    for size in raw_sizes:
        filename = '%s_%s.txt' % (classifier, size)
        with open(filename) as f:
            lines = f.readlines()
            accuracy_line = lines[-16]
            accuracy = accuracy_line.split()[4]
            accuracies.append(accuracy)
    return accuracies

def load_size_used():
    size_used = []
    with open('size_used_100_2000') as f:
        lines = f.readlines()
        for line in lines:
            size_used.append(int(line.strip()))
    return size_used

if __name__ == '__main__':
    # construct sizes vector
    size_used = load_size_used()
    print size_used

    for classifier in classifiers:
        # construct accuracies vector
        accuracies = load_accuracies(classifier)
        assert(len(accuracies) == len(size_used)), 'length of size used and accuracy vector is not the same'
        print classifier
        print '\t accuracies: ' + str(accuracies)
        print '\t max accuracy: ' + max(accuracies)

        # plotting
        # png_name = '%s.png' % (classifier)
        # r.png(png_name)
        # r.plot(size_used, accuracies, type='l', main=classifier, xlab='Feature Size', ylab='Accuracy (%)')
