import jieba
import json
from collections import Counter
from blogapp.models import Hole, HoleComment
import pytz
import math
import jieba.analyse
import matplotlib.pyplot as plt
import re
import datetime
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans


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


def get_text(keywd='', time_range='', time_date='', cmt_flag='', lst=False):
    if lst:
        text = []
    else:
        text = ''
    rg = re.compile(r'\[.*?\]')
    rg2 = re.compile(r'Re .*?:')
    holes = None
    cmts = None
    if time_range == '':
        if time_date == '':
            holes = Hole.objects.all()
            if cmt_flag == '1':
                cmts = HoleComment.objects.all()
        elif time_date != '':
            holes = Hole.objects.filter(time__date=time_date)
            if cmt_flag == '1':
                cmts = HoleComment.objects.filter(time__date=time_date)
    else:
        holes = Hole.objects.filter(time__range=time_range)
        if cmt_flag == '1':
            cmts = HoleComment.objects.filter(time__range=time_range)

    for hole in holes:
        if keywd == '' or keywd in hole.text:
            if lst:
                text.append(hole.text)
            else:
                text += hole.text + ' '
    if cmt_flag == '1':
        for cmt in cmts:
            if keywd == '' or keywd in cmt.text:
                if lst:
                    text.append(re.sub(rg2, '', re.sub(rg, '', cmt.text, 1), 1))
                else:
                    text += re.sub(rg2, '', re.sub(rg, '', cmt.text, 1), 1) + ' '
    return text


def get_relative(keywd, time_range='', cmt_flag='', num=100):
    text = get_text(keywd, time_range, cmt_flag)
    jieba.add_word(keywd)
    jieba.analyse.set_stop_words('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/stopwords.txt')
    tags = dict(jieba.analyse.extract_tags(text, topK=num, withWeight=True))
    return tags


def get_cluster(date_range=[], cmt_flag='', num=100, n_clusters=5):
    min_date = datetime.datetime.strptime(date_range[0], '%Y-%m-%d')
    max_date = datetime.datetime.strptime(date_range[1], '%Y-%m-%d')
    dates = []
    data = dict()
    while 1:
        dates.append(min_date.strftime('%Y-%m-%d'))
        if min_date == max_date:
            break
        min_date += datetime.timedelta(days=1)

    segment_jieba = lambda text: " ".join(jieba.cut(text))
    corpus = []

    for date in dates:
        print(date)
        corpus.append(segment_jieba(get_text(time_date=date)))

    print('cut done')

    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

    word = vectorizer.get_feature_names()
    print("word feature length: {}".format(len(word)))
    tfidf_weight = tfidf.toarray()

    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(tfidf_weight)

    print(kmeans.cluster_centers_)
    for index, label in enumerate(kmeans.labels_, 1):
        print("index: {}, label: {}".format(index, label))

    print("inertia: {}".format(kmeans.inertia_))

    tsne = TSNE(n_components=2)
    decomposition_data = tsne.fit_transform(tfidf_weight)

    x = []
    y = []

    for i in decomposition_data:
        x.append(i[0])
        y.append(i[1])

    plt.figure(figsize=(10, 10))
    plt.axes()
    plt.scatter(x, y, c=kmeans.labels_, marker="x")
    plt.xticks(())
    plt.yticks(())
    plt.show()

