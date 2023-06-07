from django.urls import path, re_path
from draw import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

app_name = 'draw'

urlpatterns = [

    # path('',views.home, name = '홈'),
    path('main3/',views.home3, name = '홈3'),
    path('main/',views.home, name = '홈'),
    # path('start/', views.start, name='시작'),
    path('', views.start, name='시작'),
    path('auth/login/', views.login, name='로그인'),
    path('auth/logout/', views.logout, name='로그아웃'),
    path('auth/join/', views.join, name='회원가입'),
    path('auth/mypage/', views.myPage, name='마이페이지'),
    path('auth/delete/', views.delete, name='회원탈퇴'),
    path('auth/practice/', views.practice, name='연습모드'),
    path('member_idcheck', views.member_idcheck, name='member_idcheck'),
    path('member_insert', views.member_insert, name='member_insert'),
    path('member_login', views.member_login, name='member_login'),
    path('member_delete', views.member_delete, name='member_delete'),
    path('full/', views.full, name='full'),
    path('full/filtering', views.filtering, name='필터링'),
    path('full/like', views.like, name='좋아요'),
    path('full/likeCancel', views.likeCancel, name='좋아요취소'),
    # path('main3/bookmark', views.bookmark, name='북마크'),
    path('main/like', views.like, name='좋아요'),
    path('main/likeCancel', views.likeCancel, name='좋아요취소'),

    path('crawl', views.crawl, name='crawl'),
    
    path('auth/mypage/member_update', views.member_update, name='member_update'),
    path('auth/details/', views.details, name='상세정보'),
    path('auth/details/update_views', views.update_views, name='조회수 증가'),
    path('auth/details/comment', views.comment, name='코멘트'),
    path('auth/details/reportLayer', views.reportLayer, name='신고'),
    path('auth/details/report', views.report, name='신고전송'),

    path('auth/practice/sendmail/', views.sendmail, name='sendmail'),
    path('auth/login/send_mail', views.send_mail, name='send_mail'),

    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),

    path('main/likeShoe', views.like_shoe, name='신발좋아요'),
    path('full/like2', views.like_shoe, name='신발좋아요2'),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

