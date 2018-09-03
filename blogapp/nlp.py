import jieba
import json
from collections import Counter
from blogapp.models import Hole, HoleComment
import pytz
import math
import jieba.analyse
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re


def get_freq(data):
    with open('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/stopwords.txt', 'r') as f:
        stop_words = f.read().splitlines()
    lst = jieba.cut(data, cut_all=False)
    print('cut done')
    cnt = 0
    c = Counter()
    for x in lst:
        cnt += 1
        if cnt % 500000 == 0:
            print('finished...{} words.'.format(cnt))
        if len(x) > 1:
            c[x] += 1
    for x in c:
        if x in stop_words:
            c[x] = 0
    '''
    with open('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/word_freq.json', 'w') as f:
        json.dump(c.most_common(1000), f, ensure_ascii=False)
    '''

    return dict(c)


def get_text(year, data_type='hole'):
    text = ''
    if data_type == 'hole':
        holes = Hole.objects.filter(time__year=year)
        for hole in holes:
            text += hole.text + ' '
        return text
    elif data_type == 'comment':
        hole_comments = HoleComment.objects.filter(time__year=year)
        for comment in hole_comments:
            text += comment.text + ' '
        return text


'''
def get_relative(keywd):
    text = get_text('2018')
    freq_data = get_freq(text)
    words = freq_data.keys()
    valid_holes = []
    holes = Hole.objects.filter(time__year='2018')
    hole_num = len(holes)
    keywd_cnt = 0
    for hole in holes:
        if keywd in hole.text:
            keywd_cnt += 1
            valid_holes.append(hole)
    relative_words_cnt = Counter()
    for word in words:
        for hole in valid_holes:
            if word in hole.text:
                relative_words_cnt[word] += 1
    relative_words_lst = dict(relative_words_cnt.most_common(1000))
    relative_words_index = dict()
    for word in relative_words_lst.keys():
        total_freq = freq_data[word]
        if total_freq == 0:
            continue
        cnt = 0
        for hole in holes:
            if word in hole.text:
                cnt += 1
        print('{}: cnt: {}, freq:{}'.format(word, cnt, relative_words_lst[word]))
        index = math.log(hole_num / (cnt + 1))
        relative_words_index[word] = index * relative_words_lst[word]
    relative_words = dict(sorted(relative_words_index.items(), key=lambda x: x[1], reverse=True)[0:100])
    return relative_words
'''


def get_relative(keywd, time_range='', cmt_flag='', draw=False):
    text = ''
    rg = re.compile(r'\[.*?\]')
    rg2 = re.compile(r'Re .*?:')
    if time_range == '':
        holes = Hole.objects.filter(time__year='2018')
        if cmt_flag == '1':
            cmts = HoleComment.objects.filter(time__year='2018')
    else:
        holes = Hole.objects.filter(time__range=time_range)
        if cmt_flag == '1':
            cmts = HoleComment.objects.filter(time__range=time_range)
    for hole in holes:
        if keywd in hole.text:
            text += hole.text
    if cmt_flag == '1':
        for cmt in cmts:
            if keywd in cmt.text:
                text += re.sub(rg2, '', re.sub(rg, '', cmt.text, 1), 1)
    jieba.analyse.set_stop_words('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/stopwords.txt')
    tags = dict(jieba.analyse.extract_tags(text, topK=500, withWeight=True))
    if draw:
        word_cloud(tags)
    return tags


def word_cloud(data):
    wc = WordCloud(font_path='/Users/yanjin/Documents/《此间》/培训/《此间》字体包/方正兰亭黑简体.TTF')
    wc.generate_from_frequencies(data)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
