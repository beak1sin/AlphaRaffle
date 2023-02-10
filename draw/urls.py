from django.urls import path, re_path
from draw import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

app_name = 'draw'

urlpatterns = [

    path('',views.home, name = '홈'),
    path('auth/login/', views.login, name='로그인'),
    path('auth/logout/', views.logout, name='로그아웃'),
    path('auth/mypage/', views.myPage, name='마이페이지'),
    path('auth/delete/', views.delete, name='회원탈퇴'),
    path('auth/practice/', views.practice, name='연습모드'),
    path('member_idcheck', views.member_idcheck, name='member_idcheck'),
    path('member_insert', views.member_insert, name='member_insert'),
    path('member_login', views.member_login, name='member_login'),
    path('member_delete', views.member_delete, name='member_delete'),
    path('full/', views.full, name='full'),

    path('crawl', views.crawl, name='crawl'),
    path('crawl2', views.crawl2, name='crawl2'),
    
    path('auth/mypage/member_update', views.member_update, name='member_update'),
    path('auth/details/', views.details, name='상세정보'),

    path('auth/practice/sendmail/', views.sendmail, name='sendmail'),
    path('auth/login/send_mail', views.send_mail, name='send_mail'),

    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

