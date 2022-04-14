
import json
from collections import defaultdict

DIRS = ['mhp', 'peer']
FILES = ['train.txt', 'test.txt'] # valid.txt
MIN_COUNT = 5
IS_JSON = True
ROOT_DIR = 'fold0' # '.'

def main():
    vocab = defaultdict(lambda: 0)

    files = 0
    for d in DIRS:
        for f in FILES:
            files += 1
            with open(ROOT_DIR + '/' + d + '/' + f + '.nounks') as handle:
                lines = handle.readlines() if not IS_JSON else json.loads(handle.read())
                for line in lines:
                    tline = ' '.join(line) if IS_JSON else line
                    tline = tline.rstrip().split(' ')
                    for t in tline:
                        vocab[t] += 1

    print('Number of files read: ' + str(files))
    print('Vocabulary size pre-filter: ' + str(len(vocab)))

    v = [k for k,v in vocab.items() if v >= MIN_COUNT]
    print('Vocabulary size post-filter: ' + str(len(v)))

    with open('vocab', 'w') as handle:
        handle.write(json.dumps(v))

if __name__ == '__main__':
    main()
