from django.urls import path, re_path
from draw import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from AlphaRaffle import cron

# 색인
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from .models import Shoe

info_dict = {
    'queryset': Shoe.objects.all(),
}
# --색인

# rss
from .feeds import LatestShoesFeed
# --rss

from django.views.generic import TemplateView

from draw import consumers

app_name = 'draw'

urlpatterns = [

    # path('',views.home, name = '홈'),
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
    path('member_nicknamecheck', views.member_nicknamecheck, name='member_nicknamecheck'),
    path('auth_forgot_id', views.auth_forgot_id, name='auth_forgot_id'),
    path('member_insert', views.member_insert, name='member_insert'),
    path('member_login', views.member_login, name='member_login'),
    path('member_delete', views.member_delete, name='member_delete'),
    path('full/', views.full, name='full'),
    path('full/filtering', views.filtering, name='필터링'),
    path('full/filtering_order', views.filtering_order, name='필터링오더'),
    path('full/like', views.like, name='좋아요'),
    path('full/likeCancel', views.likeCancel, name='좋아요취소'),
    # path('main3/bookmark', views.bookmark, name='북마크'),
    path('main/like', views.like, name='좋아요'),
    path('main/likeCancel', views.likeCancel, name='좋아요취소'),

    path('full/search/', views.search, name='검색'),
    
    # path('crawl', views.crawl, name='crawl'),
    
    path('auth/mypage/member_update', views.member_update, name='member_update'),
    path('auth/details/', views.details, name='상세정보'),
    path('auth/details/update_views', views.update_views, name='조회수 증가'),
    path('auth/details/comment', views.comment, name='코멘트'),
    path('auth/details/reportLayer', views.reportLayer, name='신고'),
    path('auth/details/report', views.report, name='신고전송'),
    path('auth/details/map/', views.map, name='map'),
    path('auth/details/map/api/get_geocode/', views.get_geocode, name='get_geocode'),

    path('auth/practice/sendmail/', views.sendmail, name='sendmail'),
    path('auth/login/send_mail', views.send_mail, name='send_mail'),

    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),

    path('main/likeShoe', views.like_shoe, name='신발좋아요'),
    path('full/likeShoe', views.like_shoe, name='신발좋아요'),
    path('auth/details/likeShoe', views.like_shoe, name='신발좋아요'),

    path('full/delete_recent_searches', views.delete_recent_searches, name="최근검색어삭제"),
    path('full/all_recent_delete', views.all_recent_delete, name="최근검색어전체삭제"),
    

    path('crawl', cron.crawl2, name='crawl'),

    # 색인
    # 기본 Sitemap 경로
    path('sitemap.xml', sitemap,
         {'sitemaps': {'sitemaps': GenericSitemap(info_dict, priority=0.6)}},
         name='django.contrib.sitemaps.views.sitemap'),

    # rss
    path('rss/', LatestShoesFeed(), name='rss'),

    # robots.txt
    path('robots.txt', TemplateView.as_view(template_name="draw/robots.txt", 
     content_type='text/plain')),

    # 네이버 서치어드바이저
    path('naver07438b501f2bcdb23c19460dc9cca09d.html', views.naverSearch , name='naverSearch'),
    path('naver73749ca69b9eff6e2574852408ea3ecf.html', views.naverSearchwww , name='naverSearchwww'),

    # 구글 애드센스(ads.txt)
    path('ads.txt', TemplateView.as_view(template_name="draw/ads.txt", 
     content_type='text/plain')),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

