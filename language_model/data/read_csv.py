

import pandas as pd

def main():
    # read_from_task_df()
    read_from_scores_df()

def read_from_scores_df():
    df = pd.read_pickle('../../Data/task_df_score_info.pickle')
    maindf = pd.read_pickle('../../Data/task_dataframe.pickle')
    # high_scores = df['highest-score'].tolist()

    scores = df[df['tie-highest'] == 0]
    idxes = scores['idx'].tolist()
    trt = [maindf.iloc[idx]['top-reply-text'] for idx in idxes]

    #print(mhp_df)
    print('\n\nTotal Size: ' + str(len(trt)))

    handle = open('lowscore/all.txt', 'w')

    for com in trt:
        lines = com.split('\n')
        for l in lines:
            t = l.strip()
            if '' == t:
                continue
            handle.write(t + '\n')

    handle.close()

def score_stats():
    df = pd.read_pickle('../../Data/task_dataframe.pickle')
    mhp_df = df[df['author-type'] == 'mhp']
    peer_df = df[df['author-type'] == 'non-mhp']

    mhp_scores = mhp_df['top-reply-score'].tolist()
    peer_scores = peer_df['top-reply-score'].tolist()

    def show_stats(tdf):
        avg = sum(tdf) * 1.0 / len(tdf)
        sort_scores = sorted(tdf)
        iqr1 = sort_scores[int(len(sort_scores) / 4.0)]
        iqr3 = sort_scores[int(len(sort_scores) * 3 / 4.0)]
        median = sort_scores[int(len(sort_scores) / 2.0)]

        print('\tAverage: ' + str(avg))
        print('\tMedian: ' + str(median))
        print('\tIQR-1: ' + str(iqr1))
        print('\tIQR-3: ' + str(iqr3))
        print('\tMin-Max: ' + str(min(tdf)) + ' -- ' + str(max(tdf)))

    print('MHPs:')
    show_stats(mhp_scores)
    print('\nPeers:')
    show_stats(peer_scores)

def read_from_task_df():
    # df = pd.read_csv('task_dataframe.csv', low_memory=False)
    df = pd.read_pickle('../../Data/task_dataframe.pickle')

    # 'author-type' field refers to the top replier type for the post (not the poster)
    mhp_df = df[df['author-type'] == 'mhp'] #non-
    trt = mhp_df['top-reply-text'].tolist()

    #print(mhp_df)
    print('\n\nTotal Size: ' + str(len(trt)))

    handle = open('mhp/all.txt', 'w')

    for com in trt:
        lines = com.split('\n')
        for l in lines:
            t = l.strip()
            if '' == t:
                continue
            handle.write(t + '\n')

    handle.close()

if __name__ == '__main__':
    main()
