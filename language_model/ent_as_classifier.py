
import operator
import matplotlib.pyplot as plt

from collections import defaultdict

MOM_FILE = 'entropy_log_mhp_on_mhp'
POM_FILE = 'entropy_log_peer_on_mhp'
MOP_FILE = 'entropy_log_mhp_on_peer'
POP_FILE = 'entropy_log_peer_on_peer'

MHP_SENTS = 'data/fold0/mhp/test.txt'

def main():
    classify()
    # find_pred_flip_words()

def find_pred_flip_words():
    mom = get_ents(MOM_FILE, avg=False)
    pom = get_ents(POM_FILE, avg=False)
    pop = get_ents(POP_FILE, avg=False)
    mop = get_ents(MOP_FILE, avg=False)

    mlines = []
    with open(MHP_SENTS) as handle:
        for line in handle.readlines():
            mlines.append(line.rstrip().split(' '))

    change_words = defaultdict(lambda: 0)
    for i in range(len(mom)):
        msofar = []
        psofar = []
        cp = 'na' # current prediction
        changes = 0
        label_seq = []
        ment_seq = []
        pent_seq = []
        for j in range(len(mom[i])-1):
            msofar.append(mom[i][j])
            psofar.append(pom[i][j])

            # calculate averages so far
            mavg = sum(msofar) * 1.0 / len(msofar)
            pavg = sum(psofar) * 1.0 / len(psofar)
            ment_seq.append(mavg)
            pent_seq.append(pavg)

            ischange = False
            if mavg < pavg:
                label_seq.append('mhp')
                if cp != 'mhp':
                    cp = 'mhp'
                    ischange = True
            else:
                label_seq.append('peer')
                if cp != 'peer':
                    cp = 'peer'
                    ischange = True

            if ischange:
                changes += 1
                if j > 0:
                    # change bi-grams
                    change_words[mlines[i][j] + '-' + mlines[i][j-1]] += 1

        if changes > 1:
            print(mlines[i])
            print(label_seq)
            print(ment_seq)
            print(pent_seq)
            print('\n')

            # make a plot
            x = [z for z in range(len(ment_seq))]

            PLT_SKIP = 15 # avg fluctuates in beginning
            for z in range(PLT_SKIP):
                if len(ment_seq) > z:
                    ment_seq[z] = ment_seq[-1]
                    pent_seq[z] = pent_seq[-1]

            plt.figure(figsize=(18,9))
            plt.plot(x, ment_seq)
            plt.plot(x, pent_seq)
            plt.xticks(x, mlines[i], rotation=90)
            plt.margins(x=0, y=0.25)
            plt.legend(['MHP', 'Peer'])
            plt.grid(True)
            # plt.show()
            plt.tight_layout()
            plt.savefig('entropy_graphs/' + str(i) + '.png')
            plt.cla()

    # print('\n\n')
    # for k,v in sorted(change_words.items(), key=operator.itemgetter(1)):
    #     print(k + '\t' + str(v))

def classify():
    mom = get_ents(MOM_FILE)
    pom = get_ents(POM_FILE)
    pop = get_ents(POP_FILE)
    mop = get_ents(MOP_FILE)

    assert len(mom) == len(pom) 
    assert len(pom) == len(mop) 
    assert len(mop) == len(pop)

    # all_m = mom + mop
    # all_p = pop + pom
    # mean_M = sum(all_m) / len(all_m)
    # mean_P = sum(all_p) / len(all_p)

    correct = 0
    for i in range(len(mom)):
        if mom[i] - mean_P < pom[i] - mean_M:
            correct += 1
    for i in range(len(mom)):
        if pop[i] - mean_M < mop[i] - mean_P:
            correct += 1

    acc = correct * 100.0 / (len(mom) * 2)
    print('Accuracy: ' + '{:.2f}'.format(acc) + '%')

def get_ents(fname, avg=True):
    avg_ents = []
    with open(fname) as handle:
        for line in handle.readlines():
            tline = line.strip()[1:-1].split(', ')
            tline = [float(i) for i in tline]
            if avg:
                avg_ents.append(sum(tline) * 1.0 / len(tline))
            else:
                avg_ents.append(tline)
    return avg_ents

if __name__ == '__main__':
    main()
