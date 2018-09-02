import jieba
import json
from collections import Counter
from blogapp.models import Hole, HoleComment
import pytz


def get_freq(data):
    with open('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/stopwords.txt', 'r') as f:
        stop_words = f.read().splitlines()
    lst = jieba.cut(data, cut_all=False)
    print('cut done')
    cnt = 0
    c = Counter()
    for x in lst:
        cnt += 1
        if cnt % 10000 == 0:
            print('finished...{} words.%'.format(cnt))
        if len(x) > 1:
            c[x] += 1
    for x in c:
        if x in stop_words:
            c[x] = 0
    '''
    with open('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/word_freq.json', 'w') as f:
        json.dump(c.most_common(1000), f, ensure_ascii=False)
    '''
    data = dict()
    for k, v in c.most_common(1000):
        data[k] = v
    return data


def get_text(date, data_type='hole'):
    text = ''
    if data_type == 'hole':
        holes = Hole.objects.filter(time__range=[date + ' 00:00:00+08:00', date + ' 23:59:59+08:00'])
        for hole in holes:
            text += hole.text + ' '
        return text
    elif data_type == 'comment':
        hole_comments = HoleComment.objects.filter(time__range=[date + ' 00:00:00+08:00', date + ' 23:59:59+08:00'])
        for comment in hole_comments:
            text += comment.text + ' '
        return text
