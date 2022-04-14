
import torch, json, os

from collections import Counter


class Dictionary(object):
    def __init__(self):
        self.word2idx = {}
        self.idx2word = []
        self.counter = Counter()
        self.total = 0

    def add_word(self, word):
        if word not in self.word2idx:
            self.idx2word.append(word)
            self.word2idx[word] = len(self.idx2word) - 1
        token_id = self.word2idx[word]
        self.counter[token_id] += 1
        self.total += 1
        return self.word2idx[word]

    def __len__(self):
        return len(self.idx2word)


class Corpus(object):
    def __init__(self, path, vocab):
        self.dictionary = Dictionary()
        with open(vocab) as handle:
            vv = json.loads(handle.read())
        for i in vv:
            self.dictionary.add_word(i)
        self.dictionary.add_word('<UNK>')
        self.dictionary.add_word('<eos>')

        self.train = self.tokenize(os.path.join(path, 'train.txt'))
        self.valid = self.tokenize(os.path.join(path, 'valid.txt'))
        self.test = self.tokenize(os.path.join(path, 'test.txt'))

        DATA_ROOT = 'data/' # fold0/
        self.test_lines = {}
        self.ts = {}
        self.ts['lowscore'] = self.tokenize(DATA_ROOT + 'lowscore/test.txt')
        self.ts['highscore'] = self.tokenize(DATA_ROOT + 'highscore/test.txt')
        with open(DATA_ROOT + 'lowscore/test.txt') as handle:
            self.test_lines['lowscore'] = handle.readlines()
        with open(DATA_ROOT + 'highscore/test.txt') as handle:
            self.test_lines['highscore'] = handle.readlines()

    def tokenize(self, path):
        """Tokenizes a text file."""
        assert os.path.exists(path)
        # Add words to the dictionary
        with open(path, 'r') as f:
            tokens = 0
            for line in f:
                words = line.split() + ['<eos>']
                tokens += len(words)
                # for word in words: # vocab will be preloaded
                #     self.dictionary.add_word(word)

        # Tokenize file content
        with open(path, 'r') as f:
            ids = torch.LongTensor(tokens)
            token = 0
            for line in f:
                words = line.split() + ['<eos>']
                for word in words:
                    ids[token] = self.dictionary.word2idx[word]
                    token += 1

        return ids
