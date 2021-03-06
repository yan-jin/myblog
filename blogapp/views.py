from django.shortcuts import render, get_object_or_404
from .models import Post, Hole, HoleComment
from django.shortcuts import render_to_response
from django.http import JsonResponse, HttpResponse
import markdown
import pytz
from collections import Counter
import blogapp.nlp as nlp
import gensim
import json


def index(request):
    projects = Post.objects.filter().order_by('-published_date')
    return render(request, 'base_index.html', {'projects': projects})


def blog(request, pk):
    blog = get_object_or_404(Post, pk=pk)
    if blog.text[0] != '$':
        blog.text = markdown.markdown(blog.text)
    else:
        blog.text = blog.text[1:]
    return render(request, 'base_blog.html', {'blog': blog})


def page_not_found(request):
    return render_to_response('404.html')


def hole(request):
    return render(request, 'pkuhole.html')


def heat_plot(request):
    return render(request, 'heat_plot.json')


def week_heat(request):
    return render(request, 'week_heat.json')


def hole_bg(request):
    return HttpResponse(open("/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/templates/PKU-background.jpg", "rb"), content_type="image/jpg")


def q_word(request):
    word = request.GET.get('q')
    cmt_flag = request.GET.get('cmt', '')
    time_range = request.GET.get('time_range', '')
    tip_flag = request.GET.get('tips', '')
    if tip_flag == '1':
        try:
            model = gensim.models.Word2Vec.load(
                '/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/holes_corpus.model')
            result = model.most_similar(word)
        except:
            with open('/Users/yanjin/PycharmProjects/web-projects/myblog/blogapp/bbs_words_relative.json', 'r') as f:
                data = json.load(f)
            try:
                tips = [w[0] for w in data[word]]
            except:
                return JsonResponse({'tips': None, 'q': word})
            return JsonResponse({'tips': tips})
        tips = []
        for r in result:
            tips.append(r[0])
        return JsonResponse({'tips': tips})
    if time_range != '':
        time_range = eval(time_range)
        time_range[0] += ' 00:00:00+08:00'
        time_range[1] += ' 23:59:59+08:00'

    tz = pytz.timezone('Asia/Shanghai')
    if time_range != '':
        holes = Hole.objects.filter(time__range=time_range).order_by('time')
    else:
        holes = Hole.objects.all().order_by('time')
    c = Counter()
    date_cnt = Counter()
    for hole in holes:
        date = hole.time.astimezone(tz).strftime('%Y-%m-%d')
        c[date] += hole.text.count(word)
        date_cnt[date] += 1

    if cmt_flag == '1':
        if time_range != '':
            hole_cmts = HoleComment.objects.filter(time__range=time_range).order_by('time')
        else:
            hole_cmts = HoleComment.objects.all().order_by('time')
        for cmt in hole_cmts:
            date = cmt.time.astimezone(tz).strftime('%Y-%m-%d')
            c[date] += cmt.text.count(word)
            date_cnt[date] += 1
    json_date = sorted([k for k in c.keys()])
    json_num = [c[d] for d in json_date]
    for k in c:
        c[k] /= date_cnt[k]

    json_index = [c[d] for d in json_date]
    json_keywords = nlp.get_relative(word, time_range=time_range, cmt_flag=cmt_flag, num=300)

    # data = json.dumps({'date': json_date, 'index': json_index, 'num': json_num})
    # return HttpResponse(data)
    return JsonResponse({'date': json_date, 'index': json_index, 'num': json_num, 'keywords': json_keywords})
