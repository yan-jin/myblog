from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans
import datetime
import jieba
from blogapp.models import Hole, HoleComment
import myblog.urls


class Kmeans(object):
    def transform(self, dataset, n_features=1000):
        vectorizer = TfidfVectorizer(max_df=0.5, max_features=n_features, min_df=2, use_idf=True)
        X = vectorizer.fit_transform(dataset)
        return X, vectorizer

    def train(self, X, vectorizer, true_k=10, minibatch=False, showLable=False):
        # 使用采样数据还是原始数据训练k-means，
        if minibatch:
            km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
                                 init_size=1000, batch_size=1000, verbose=False)
        else:
            km = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=1,
                        verbose=False)
        km.fit(X)
        if showLable:
            print("Top terms per cluster:")
            order_centroids = km.cluster_centers_.argsort()[:, ::-1]
            terms = vectorizer.get_feature_names()
            print(vectorizer.get_stop_words())
            for i in range(true_k):
                print("Cluster %d:" % i, end='')
                for ind in order_centroids[i, :10]:
                    print(' %s' % terms[ind], end='')
                print()
        result = list(km.predict(X))
        print('Cluster distribution:')
        print(dict([(i, result.count(i)) for i in result]))
        return -km.score(X)

    def test(self, dataset):
        """测试选择最优参数"""
        print("%d documents" % len(dataset))
        X, vectorizer = self.transform(dataset, n_features=500)
        true_ks = []
        scores = []
        for i in xrange(3, 80, 1):
            score = self.train(X, vectorizer, true_k=i) / len(dataset)
            print(i, score)
            true_ks.append(i)
            scores.append(score)
        plt.figure(figsize=(8, 4))
        plt.plot(true_ks, scores, label="error", color="red", linewidth=1)
        plt.xlabel("n_features")
        plt.ylabel("error")
        plt.legend()
        plt.show()

    def out(self, dataset, n=5):
        """在最优参数下输出聚类结果"""
        X, vectorizer = self.transform(dataset, n_features=500)
        score = self.train(X, vectorizer, true_k=n, showLable=True) / len(dataset)
        return score

    def get_cluster(self, date_range=[], cmt_flag='', num=100, n_clusters=5):
        with open('stopwords.txt', 'r') as f:
            stop_words = f.read().splitlines()
        segment_jieba = lambda text: " ".join([i for i in jieba.cut(text) if i not in stop_words])
        corpus = [segment_jieba(hole.text) for hole in Hole.objects.filter(time__range=date_range)]
        print('cut done')
        self.test(corpus)
