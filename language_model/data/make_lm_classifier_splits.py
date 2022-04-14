

import random, json
import pandas as pd
from tqdm import tqdm
from collections import Counter
from nltk.tokenize import word_tokenize
from sklearn import svm, linear_model, naive_bayes

df = pd.read_pickle('../../Data/task_dataframe.pickle')
mhp_df = df[df['author-type'] == 'mhp']
peer_df = df[df['author-type'] == 'non-mhp']

mhp_text = list(mhp_df['top-reply-text'].values)
peer_text = list(peer_df['top-reply-text'].values)
mhp_index = list(mhp_df['top-reply-text'].index)
peer_index = list(peer_df['top-reply-text'].index) 

print(len(mhp_text), len(peer_text))

folds = 10
proportion = 1/folds
n_samples = len(mhp_text)

fold_ranges = {}

for i in range(folds):
    test_0 = int((i * proportion) * n_samples)
    test_1 = int(test_0 + proportion * n_samples)

    test_range = list(range(test_0, test_1))
    train_range = list(range(0,test_0)) + list(range(test_1,n_samples))

    fold_ranges[i] = {'train':train_range, 'test':test_range}

def preprocess(sentence):
    return [i.lower() for i in word_tokenize(sentence)]

from collections import defaultdict
def get_vocab(points, min_count, nchar):
    vl = defaultdict(lambda: 0)
    for p in tqdm(points):
        tokens = preprocess(p)# if preproc else p.split()
        for t in tokens:
            vl[t] += 1

    vset = set()
    for k,v in vl.items():
        if v >= min_count:
            vset.add(k)

    return list(vset)

min_count = 5
LABELS = {'mhp': 0, 'peer': 1}

###############################

seed = 20
random.seed(seed)

peer_sample = random.sample(list(zip(peer_text, peer_index)), k=len(mhp_text))
peer_text_sample, peer_index_sample = zip(*peer_sample)

result_df = {'seed':[],'fold':[],'accuracy':[], 'vocabsize':[], 'len(train)':[], 'len(test)':[], '% train':[], '% test':[], 'test-mhp':[], 'test-peer':[], 'train-mhp':[], 'train-peer':[]}

fold_vector_df = {'seed':[], 'fold':[], 'actuals':[], 'random-baseline':[], 'predictions':[], 'difference':[], 'index':[]}

for fold in fold_ranges:

    print("\nFold {}".format(fold + 1))
    print('-'*80)
    train_range = fold_ranges[fold]['train']
    test_range = fold_ranges[fold]['test']

    train_mhp = [mhp_text[i] for i in train_range]
    train_peer = [peer_text_sample[i] for i in train_range]

    test_mhp = [mhp_text[i] for i in test_range]
    test_peer = [peer_text_sample[i] for i in test_range]

    # test_index = [mhp_index[i] for i in test_range] + [peer_index_sample[i] for i in test_range]
    # train_index = [mhp_index[i] for i in train_range] + [peer_index_sample[i] for i in train_range]


    ##### get splits

    with open('fold' + str(fold) + '/mhp/train.txt', 'w') as handle:
        print(len(train_mhp))
        handle.write(json.dumps(train_mhp))
    with open('fold' + str(fold) + '/mhp/test.txt', 'w') as handle:
        print(len(test_mhp))
        handle.write(json.dumps(test_mhp))

    with open('fold' + str(fold) + '/peer/train.txt', 'w') as handle:
        print(len(train_peer))
        handle.write(json.dumps(train_peer))
    with open('fold' + str(fold) + '/peer/test.txt', 'w') as handle:
        print(len(test_peer))
        handle.write(json.dumps(test_peer))

    #######
    break



    points, labels = zip(*train)
    train_label_counts = Counter(labels)

    print('shuffling points...')
    z = [i for i in range(len(points))]
    random.shuffle(z)
    p2 = [points[i] for i in z]
    l2 = [labels[i] for i in z]
    points = p2
    labels = l2

    print("getting vocab...")
    vocab = get_vocab(points, min_count, nchar)
    vocabsize = len(vocab)
    print('vocab size: ' + str(vocabsize))

    """
    Vectorizing
    """
    print('vectorizing training...')
    train_vecs = vectorize(points, vocab, nchar)
    label_bin = [LABELS[i] for i in labels]

    tp, tl = zip(*test)
    tl_counts = Counter(tl)

    print('vectorizing test...')
    dev_vecs = vectorize(tp, vocab, nchar)
    tl_bin = [LABELS[i] for i in tl]
    clf = naive_bayes.MultinomialNB()
    print('fitting classifier...')
    # clf = svm.LinearSVC(verbose=1, max_iter=10000)
    # clf = linear_model.LogisticRegression()
    clf = naive_bayes.MultinomialNB()
    clf.fit(train_vecs, label_bin)


    """
    Predictions
    """
    print('predicting dev labels...')
    out = clf.predict(dev_vecs)
    print(out)
    total = np.sum(out == tl_bin)
    accuracy = total * 100.0 / len(tl_bin)
    print('accuracy: ' + str(accuracy))
    random_baseline = [random.choice([0,1]) for i in tl_bin]

    fold_vector_df['seed'].extend([seed for i in tl_bin])
    fold_vector_df['fold'].extend([fold for i in tl_bin])
    fold_vector_df['predictions'].extend(out)
    fold_vector_df['random-baseline'].extend(random_baseline)
    fold_vector_df['actuals'].extend(tl_bin)
    fold_vector_df['difference'].extend(prediction_differences(out, random_baseline, tl_bin))
    fold_vector_df['index'].extend(test_index)



    result_df['seed'].append(seed)
    result_df['fold'].append(fold)
    result_df['accuracy'].append(accuracy)
    result_df['vocabsize'].append(vocabsize)
    result_df['len(train)'].append(len(train))
    result_df['len(test)'].append(len(test))
    result_df['% train'].append(len(train) / (len(train) + len(test)))
    result_df['% test'].append(len(test) / (len(train) + len(test)))
    result_df['test-mhp'].append(tl_counts['mhp'])
    result_df['test-peer'].append(tl_counts['peer'])
    result_df['train-mhp'].append(train_label_counts['mhp'])
    result_df['train-peer'].append(train_label_counts['peer'])

# result_df = pd.DataFrame(result_df, columns=result_df.keys())
# fold_vector_df = pd.DataFrame(fold_vector_df, columns=fold_vector_df.keys())

# result_df.to_pickle('classifier/lstm-results.pickle')
# fold_vector_df.to_pickle('classifier/lstm-fold-vectors.pickle')
# print("complete.")