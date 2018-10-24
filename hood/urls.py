from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

urlpatterns=[
    url('^$', views.index, name='index'),
    url(r'^user/(\d+)$', views.profile, name='profile'),
    url(r'search/', views.search_results, name='search'),
    url(r'^createhood/$', views.createhood, name='createhood'),
    url(r'^edithood/(\d+)$', views.edithood, name='edithood'),
    url(r'^deletehood/(\d+)$',views.deletehood, name = 'deletehood'),
    url(r'^join/(\d+)$',views.join, name = 'joinhood'),
    url(r'^createbusiness/$', views.createbusiness, name='createbusiness'),
    url(r'^exithood/(\d+)$', views.exithood, name='exithood'),
    url(r'^createpost/$', views.createPost, name='createpost'),
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
