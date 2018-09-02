import re
import os
import requests
import datetime
import json
import pytz
import blogapp.text_analysis as ta

from blogapp.models import Hole, HoleComment

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myblog.settings")
django.setup()


class Comment(object):
    def __init__(self, cid='', pid='', text='', time=''):
        self.cid = cid
        self.pid = pid
        self.text = text
        self.time = time


class Post(object):
    def __init__(self, text='', comments=[], pid='', time='', likes='', comments_num=''):
        self.text = text
        self.comments = comments
        self.time = time
        self.likes = likes
        self.comments_num = comments_num
        self.pid = pid


def plus_dir(s):
    year = s[0:4]
    month = s[-2:]
    if month == '12':
        month = '01'
        year = year[0:3] + str(int(year[3]) + 1)
    else:
        m = int(month) + 1
        if m < 10:
            month = '0' + str(m)
        else:
            month = str(m)
    return year + month


def plus_date(s):
    year = int(s[0:4])
    month = int(s[4:6])
    day = int(s[-2:])
    m = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0 and year % 100 == 0):
        m[1] = 29
    day += 1
    if day > m[month - 1]:
        day = 1
        month += 1
        if month > 12:
            month = 1
            year += 1
    y = str(year)
    m = ''
    d = ''
    if month < 10:
        m = '0' + str(month)
    else:
        m = str(month)
    if day < 10:
        d = '0' + str(day)
    else:
        d = str(day)
    return y + m + d


def minus_date(s):
    year = int(s[0:4])
    month = int(s[4:6])
    day = int(s[-2:])
    m = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0 and year % 100 == 0):
        m[1] = 29
    day -= 1
    if day == 0:
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        day = m[month - 1]
    y = str(year)
    m = ''
    d = ''
    if month < 10:
        m = '0' + str(month)
    else:
        m = str(month)
    if day < 10:
        d = '0' + str(day)
    else:
        d = str(day)
    return y + m + d


def date_trans(s):
    return s[0:4] + '-' + s[4:6] + '-' + s[6:8]


def parse(filename):
    posts = []
    with open(filename) as f:
        content = f.read()
        raw_posts = content.split('#p ')[1:]

        for raw_post in raw_posts:
            raw_comments = raw_post.split('#c ')[1:]
            raw_post = raw_post.split('#c ')[0]
            raw_post = raw_post.split('\n', 1)[0] + ' #: ' + raw_post.split('\n', 1)[1].replace('\n', '')
            post_info = raw_post.split(' #: ')[0].split(' ')
            post_text = raw_post.split(' #: ')[1]
            post_pid = post_info[0]
            post_time = post_info[1] + ' ' + post_info[2]
            post_likes = post_info[3]
            post_comments_num = post_info[4]
            # print('post:', raw_post)
            post_comments = []
            for raw_comment in raw_comments:
                raw_comment = raw_comment.split('\n', 1)[0] + ' #: ' + raw_comment.split('\n', 1)[1].replace(
                    '\n', '')
                comment_info = raw_comment.split(' #: ', 1)[0].split(' ')
                comment_text = raw_comment.split(' #: ', 1)[1]
                comment_cid = comment_info[0]
                comment_time = comment_info[1] + ' ' + comment_info[2]
                post_comments.append(Comment(pid=post_pid, cid=comment_cid, text=comment_text, time=comment_time))
                # print('comments:', raw_comment)
            posts.append(Post(pid=post_pid, time=post_time, text=post_text, comments=post_comments, likes=post_likes,
                              comments_num=post_comments_num))
    return posts


def insert_data(data):
    hole_cnt = 0
    cmt_cnt = 0
    for post in data:
        hole_cnt += 1
        if hole_cnt % 1000 == 0:
            print('inserted {} holes'.format(hole_cnt))
        hole = Hole(pid=post.pid, text=post.text, time=post.time + '+08:00', likes=post.likes,
                    comments_num=post.comments_num)
        hole.save()
        for comment in post.comments:
            cmt_cnt += 1
            if cmt_cnt % 1000 == 0:
                print('inserted {} comments'.format(cmt_cnt))
            hole_comment = HoleComment(pid=comment.pid, cid=comment.cid, text=comment.text,
                                       time=comment.time + '+08:00')
            hole_comment.save()
            hole.comments.add(hole_comment)


def backup_old_data():
    posts = []
    dire = '201401'
    while dire != '201809':
        print(dire)
        path = '/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/archive/{}'.format(dire)
        files = os.listdir(path)
        for file in files:
            filename = path + '/' + file
            posts.extend(parse(filename))
        dire = plus_dir(dire)
    insert_data(posts)


def get_text(date):
    main_url = 'https://github.com/martinwu42/dlpkuhole2/raw/master/archive/'
    html = None
    for i in range(1, 5):
        url = main_url + date[0:6] + '/pkuhole' + date + '.txt'
        try:
            html = requests.get(url)
        except:
            continue

        if html is None or html.status_code == 200:
            break
    if html is not None and html.status_code == 200:
        return html.text
    else:
        return None


def get_new_data():
    posts = []
    date = ''
    text = ''
    flag = False
    with open('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/update.log', 'r') as f:
        date = f.read().replace('\n', '')
    while 1:
        date = plus_date(date)
        text = get_text(date)
        if text is None:
            break
        flag = True
        with open('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/update.log', 'w') as f:
            f.write(date)
        if not os.path.exists('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/archive/{}'.format(date[0:6])):
            os.mkdir('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/archive/{}'.format(date[0:6]))
        filename = '/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/archive/{}/{}'.format(date[0:6],
                                                                                                    'pkuhole' + date + '.txt')
        with open(filename, 'w') as ff:
            print('downloaded: {}'.format(date))
            ff.write(text)
        posts.extend(parse(filename))
    if flag:
        insert_data(posts)
        get_heat_plot_data()
        get_week_heat_data()
        print('{0}: Finished, inserted: {1} posts, latest date: {2}.'.format(
            datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"), len(posts), minus_date(date)))
    else:
        print('{}: No new data.'.format(datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S")))


def get_heat_plot_data():
    print('updating heat plot data...')
    dire = '201401'
    date_cnt = {}
    for y in range(2014, 2019):
        date_cnt.update({str(y): []})
    with open('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/update.log', 'r') as f:
        max_dire = f.read()[0:6]
    while 1:
        path = '/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/archive/{}'.format(dire)
        files = os.listdir(path)
        files.sort()
        for file in files:
            cnt = 0
            with open(path + '/' + file) as f:
                content = f.read()
                if content == '':
                    continue
                posts = re.findall(r'#p \d{1,6} \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \d+? \d+?', content)
                cnt = len(posts)
                date = posts[-1].split()[2]
            year = dire[0:4]
            date_cnt[year].append([date, cnt])
        if dire == max_dire:
            break
        dire = plus_dir(dire)

    with open('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/templates/heat_plot.json', 'w') as f:
        json.dump(date_cnt, f)


def get_week_heat_data():
    print('updating week heat data...')
    max_date = ''
    min_date = ''
    data = dict()
    times = []
    with open('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/update.log') as f:
        max_date = f.read()
    min_date = minus_date(max_date)
    data[date_trans(max_date)] = []
    data[date_trans(min_date)] = []
    for i in range(0, 5):
        min_date = minus_date(min_date)
        data[date_trans(min_date)] = []
    max_time = ' 23:59:59+08:00'
    min_time = ' 00:00:00+08:00'
    tz = pytz.timezone('Asia/Shanghai')
    for date in data.keys():
        holes = Hole.objects.filter(time__range=[date + min_time, date + max_time])
        times.extend([hole.time.astimezone(tz) for hole in holes])
    for d in data:
        for i in range(0, 24):
            data[d].append(0)
    for time in times:
        data[time.strftime('%Y-%m-%d')][time.hour] += 1
    json_data = dict()
    json_data['xAxis'] = [i for i in range(0, 24)]
    json_data['yAxis'] = sorted([d for d in data.keys()])
    json_data['data'] = []
    3
    for x in range(0, 7):
        for y in range(0, 24):
            json_data['data'].append([x, y, data[json_data['yAxis'][x]][y]])
    with open('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/templates/week_heat.json', 'w') as f:
        json.dump(json_data, f)
