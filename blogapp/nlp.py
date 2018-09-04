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


def get_relative(keywd, time_range='', cmt_flag='', num=100):
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
    jieba.add_word(keywd)
    jieba.analyse.set_stop_words('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/stopwords.txt')
    tags = dict(jieba.analyse.extract_tags(text, topK=num, withWeight=True))
    return tags
