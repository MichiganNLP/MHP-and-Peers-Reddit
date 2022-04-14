
import argparse

# python data_splitter.py --root reddit --data  jshuf_cut --train 50000 --valid 5000 --test 5000

parser = argparse.ArgumentParser()
parser.add_argument('--root', type=str, default=None, help='Location of file to split (just dir)')
parser.add_argument('--data', type=str, default=None, help='File to split (just file, not dir)')
parser.add_argument('--train', type=int, default=50000, help='Number of training posts to use')
parser.add_argument('--valid', type=int, default=5000, help='Number of validation posts to use')
parser.add_argument('--test', type=int, default=5000, help='Number of test posts to use')
args = parser.parse_args()

trains = []
valids = []
tests = []

with open(args.root + '/' + args.data) as handle:
    for line in handle.readlines():
        if len(trains) < args.train:
            trains.append(line)
        elif len(valids) < args.valid:
            valids.append(line)
        elif len(tests) < args.test:
            tests.append(line)
        else:
            break

with open(args.root + '/train.txt', 'w') as handle:
    for t in trains:
        handle.write(t)

with open(args.root + '/valid.txt', 'w') as handle:
    for t in valids:
        handle.write(t)

with open(args.root + '/test.txt', 'w') as handle:
    for t in tests:
        handle.write(t)
