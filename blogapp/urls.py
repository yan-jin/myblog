from django.conf.urls import url
from . import views
import myblog.settings as settings

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^blog/(?P<pk>[0-9]+)/$', views.blog, name='blog'),
    url(r'^hole/$', views.hole, name='hole'),
    url(r'^hole/api/heat-plot$', views.heat_plot, name='heat_plot'),
    url(r'^hole/api/week-heat$', views.week_heat, name='week_heat'),
    url(r'hole/api/q-word/$', views.q_word, name='q_word'),
    url(r'hole/api/bg/$', views.hole_bg, name='hole_bg')
]
handler404 = views.page_not_found
