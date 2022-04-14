
import operator, re
import numpy as np

from tqdm import tqdm
from colored import fg, bg, attr
from collections import defaultdict

MOM_FILE = 'entropy_log_mhp_on_mhp'
POM_FILE = 'entropy_log_peer_on_mhp'
MOP_FILE = 'entropy_log_mhp_on_peer'
POP_FILE = 'entropy_log_peer_on_peer'
#MOM_FILE = 'entropy_log_lowscore_on_lowscore'
#POM_FILE = 'entropy_log_highscore_on_lowscore'
#MOP_FILE = 'entropy_log_lowscore_on_highscore'
#POP_FILE = 'entropy_log_highscore_on_highscore'
PATH_TO_TEST_DATA = 'data/fold0/peer/test.txt'

TARGET_CAT = 'CERTAIN'
NEG_INF = -999999.0
POS_INF = 999999.0
MIN_THRESHOLD = 50
SAFE_ZERO = 0.0001

LIWC_PATH = '/path/to/liwc.2015.all'
LIWC_STEMS = defaultdict(lambda: [])
LIWC_WORDS = defaultdict(lambda: [])

with open(LIWC_PATH) as handle:
    for line in handle.readlines():
        parts = line.strip().split(' ,')
        if parts[0].endswith('*'):
            LIWC_STEMS[parts[0][:-1]].append(parts[1])
        else:
            LIWC_WORDS[parts[0]].append(parts[1])

def main():
    color_state = 'black'
    ent_map = defaultdict(lambda: [])
    ment_map = defaultdict(lambda: [])
    rl_map = defaultdict(lambda: defaultdict(lambda: 0))
    target_map = defaultdict(lambda: 0)
    target_words = defaultdict(lambda: [])
    individual_ents = defaultdict(lambda: [])
    lmap = defaultdict(lambda: [])
    sents = []
    ents = []
    ments = []

    with open(MOP_FILE) as handle:
        lines = handle.readlines()
        for l in range(len(lines)):
            parts = [float(i) for i in lines[l][1:-2].split(', ')]
            ents.append(parts[:-1] if l != len(lines) - 1 else parts)

    with open(POP_FILE) as handle:
        lines = handle.readlines()
        for l in range(len(lines)):
            parts = [float(i) for i in lines[l][1:-2].split(', ')]
            ments.append(parts[:-1] if l != len(lines) - 1 else parts)

    with open(PATH_TO_TEST_DATA) as handle:
        for line in handle.readlines():
            tline = line.strip().split(' ')
            sents.append(tline)

    min_ent = POS_INF
    max_ent = NEG_INF
    # iterate over words to create map
    for s in tqdm(range(len(sents))):
        # print(len(sents[s]))
        # print(len(ents[s]))
        # assert len(sents[s]) == len(ents[s]), print(sents[s])

        high_target = NEG_INF
        diff_ents = []
        for w in range(len(sents[s])):
            ent_map[sents[s][w]].append(ents[s][w])
            ment_map[sents[s][w]].append(ments[s][w])

            new_ent = ents[s][w] - ments[s][w]
            diff_ents.append(new_ent)

            if new_ent > max_ent:
                max_ent = new_ent
            if new_ent < min_ent:
                min_ent = new_ent

            lparts = get_liwc_parts(sents[s][w])
            for lp in lparts:
                lmap[lp].append(ents[s][w]/ments[s][w])
                #lmap[lp].append(-ments[s][w])
                rl_map[lp][sents[s][w]] += 1

                if TARGET_CAT == lp:
                    target_words[' '.join(sents[s])].append(sents[s][w])
                    if new_ent > high_target:
                        high_target = new_ent

        if high_target > NEG_INF:
            fstr = ' '.join(sents[s])
            target_map[fstr] = high_target
            individual_ents[fstr] = diff_ents

    # print top entropy word avgs
    avg_map = {k: sum(v) * 1.0 / len(v) for k,v in ent_map.items()}
    mavg_map = {k: sum(v) * 1.0 / len(v) for k,v in ment_map.items()}
    diff_map = {k: avg_map[k] - mavg_map[k] for k in avg_map}
    ldiff_map = {k: sum(v) * 1.0 / len(v) for k,v in lmap.items()}
    for k,v in sorted(diff_map.items(), key=operator.itemgetter(1)):
        print(k + '\t' + str(v))

    print('\n\n')
    for k,v in sorted(ldiff_map.items(), key=operator.itemgetter(1)):
        print(k + '\t' + str(v))

    print(rl_map[TARGET_CAT])
    print('\n\n')
    res = attr('reset')

    print('MIN_ENT: ' + str(min_ent))
    print('MAX_ENT: ' + str(max_ent))

    '''
    for k,v in sorted(target_map.items(), key=operator.itemgetter(1)):
        tokens = tex_escape(k).split(' ')
        tmin = min(individual_ents[k])
        tmax = max(individual_ents[k])
        for i in range(len(tokens)):
            # bgval = hex(int((individual_ents[k][i] - min_ent) / (max_ent - min_ent) * 255.0))[2:]
            bgval = int((individual_ents[k][i] - tmin) / (tmax - tmin + SAFE_ZERO) * 100.0)
            # color = fg('#C0C0C0') + bg('#0000' + bgval)
            # print(color + tokens[i] + res, end=' ')
            # print(color + tokens[i] + res)
            # print(' -- ' + str(individual_ents[k][i]) + ' --> ' + str((individual_ents[k][i] - min_ent) / (max_ent - min_ent)) + ' --> ' + str(bgval))

            tstr = 'black' if bgval < MIN_THRESHOLD else 'white'
            if tokens[i] in rl_map[TARGET_CAT]:
                tstr = '\\autour{blue!' + str(bgval) + '}{' + tstr + '}{' + tokens[i] + '}'
            else:
                tstr = '{\\color{' + tstr + '}'
                tstr = tstr + '\hlc[blue!' + str(bgval) + ']{' + tokens[i] + '}}'

            print(tstr, end=' ')
        # print(str(v) + '\n\n')
        # print(' -- ' + ','.join(target_words[k]))
        print('\\\\\n')
        # print(k + '\t' + str(v))
        '''

def get_liwc_parts(token):
    liwc_keys = []
    if token in LIWC_WORDS:
        liwc_keys.extend(LIWC_WORDS[token])
    for i in range(len(token)):
        temp_token = token[0:i+1]
        if temp_token in LIWC_STEMS:
            liwc_keys.extend(LIWC_STEMS[temp_token])
    return list(set(liwc_keys))

# modified, from: https://stackoverflow.com/questions/16259923/how-can-i-escape-latex-special-characters-inside-django-templates
def tex_escape(text):
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '’': '\'',
        '£': r'\\pounds',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '“': r'``',
        '”': '\'\'',
        '‘': r'`',
        '»': r'\textgreater{}\textgreater{}',
        '«': r'\textless{}\textless{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    text = ''.join([c if ord(c) < 65536 else '<UNICODE>' for c in text])
    return regex.sub(lambda match: conv[match.group()], text)

if __name__ == '__main__':
    main()

