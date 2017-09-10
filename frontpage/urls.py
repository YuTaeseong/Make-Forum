from django.conf.urls import include, url
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', frontpage, name='frontpage'),
    url(r'^profile/$', overview, name='overview'),
    url(r'^post/(?P<pk>\d+)/$', post_detail, name='post_detail'),
    url(r'^post/(?P<pk>\d+)/edit/$', post_edit, name='post_edit'),
    url(r'^post/new/$', post_new, name='post_new'),
    url(r'^post/delete/$', post_delete, name='post_delete'),
    url(r'ajax/like/$', like, name='like'),
    url(r'ajax/follow/$', follow, name='follow'),
    url(r'^profile/likeandfollow/$', likeandfollow, name='likeandfollow'),
    url(r'^profile/edit/$', profile_edit, name='profile_edit')
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)