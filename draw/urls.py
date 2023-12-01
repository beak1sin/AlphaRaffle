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
    'queryset': Shoe.objects.all().order_by('-id'),
}
# --색인

# rss
from .feeds import LatestShoesFeed
# --rss

from django.views.generic import TemplateView

from draw import consumers

app_name = 'draw'


urlpatterns = [

    path('',views.home, name = '홈'),
    # path('main/',views.home, name = '홈'),
    path('start/', views.start, name='시작'),
    # path('', views.start, name='시작'),
    path('auth/login/', views.login, name='로그인'),
    path('auth/logout/', views.logout, name='로그아웃'),
    path('auth/join/', views.join, name='회원가입'),
    path('auth/mypage/', views.myPage, name='마이페이지'),
    path('auth/mypage/bookmark/', views.Mypage.bookmark, name='마이페이지북마크'),
    path('auth/mypage/draw/', views.Mypage.draw, name='마이페이지응모'),
    path('auth/mypage/comment/', views.Mypage.comment, name='마이페이지댓글'),
    path('auth/mypage/board/', views.Mypage.board, name='마이페이지게시물'),
    path('auth/mypage/review/', views.Mypage.review, name='마이페이지리뷰'),
    path('auth/mypage/settings/', views.Mypage.settings, name='마이페이지개인정보'),
    path('auth/mypage/delete/', views.Mypage.delete, name='회원탈퇴'),
    path('auth/mypage/delete/password_check', views.Mypage.password_check, name='password_check'),
    path('auth/mypage/delete/member_delete', views.Mypage.member_delete, name='member_delete'),
    path('auth/practice/', views.practice, name='연습모드'),
    path('member_idcheck', views.member_idcheck, name='member_idcheck'),
    path('member_nicknamecheck', views.member_nicknamecheck, name='member_nicknamecheck'),
    path('auth_forgot_id', views.auth_forgot_id, name='auth_forgot_id'),
    path('verification', views.verification, name='verification'),
    path('new_password', views.new_password, name='new_password'),
    path('member_insert', views.member_insert, name='member_insert'),
    path('member_login', views.member_login, name='member_login'),
    path('full/', views.full, name='full'),
    path('full/filtering', views.filtering, name='필터링'),
    path('full/filtering_order', views.filtering_order, name='필터링오더'),
    path('full/like', views.like, name='좋아요'),
    path('full/likeCancel', views.likeCancel, name='좋아요취소'),
    # path('main3/bookmark', views.bookmark, name='북마크'),
    path('main/like', views.like, name='좋아요'),
    path('main/likeCancel', views.likeCancel, name='좋아요취소'),

    # path('crawl', views.crawl, name='crawl'),
    path('auth/mypage/settings/nickname_duplicate', views.nickname_duplicate, name='nickname_duplicate'),
    path('auth/mypage/settings/nickname_save', views.nickname_save, name='nickname_save'),
    path('auth/mypage/settings/member_update', views.member_update, name='member_update'),
    path('auth/mypage/settings/upload', views.upload, name='upload'),
    path('auth/mypage/comment/comment_delete_mypage', views.comment_delete_mypage, name='comment_delete_mypage'),

    path('auth/details/', views.details, name='상세정보'),
    path('auth/details/update_views', views.update_views, name='조회수 증가'),
    path('auth/details/comment', views.comment, name='코멘트'),
    path('auth/details/comment_delete_details', views.comment_delete_details, name='comment_delete_details'),
    path('auth/details/go_page', views.Pagination.go_page, name='go_page'),
    path('auth/details/reportLayer', views.reportLayer, name='신고'),
    path('auth/details/report', views.report, name='신고전송'),
    path('auth/details/map/', views.map, name='map'),
    path('auth/details/map/api/get_geocode/', views.get_geocode, name='get_geocode'),

    path('auth/practice/sendmail/', views.sendmail, name='sendmail'),
    path('auth/login/resend_mail', views.resend_mail, name='resend_mail'),

    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),

    path('likeShoe', views.like_shoe, name='신발좋아요'),
    path('full/likeShoe', views.like_shoe, name='신발좋아요'),
    path('auth/details/likeShoe', views.like_shoe, name='신발좋아요'),
    path('auth/mypage/likeShoe', views.like_shoe, name='신발좋아요'),
    path('auth/mypage/bookmark/likeShoe', views.like_shoe, name='신발좋아요'),

    path('full/delete_recent_searches', views.delete_recent_searches, name="최근검색어삭제"),
    path('full/all_recent_delete', views.all_recent_delete, name="최근검색어전체삭제"),
    path('delete_recent_searches', views.delete_recent_searches, name="최근검색어삭제"),
    path('all_recent_delete', views.all_recent_delete, name="최근검색어전체삭제"),
    path('auth/details/delete_recent_searches', views.delete_recent_searches, name="최근검색어삭제"),
    path('auth/details/all_recent_delete', views.all_recent_delete, name="최근검색어전체삭제"),
    path('auth/mypage/delete_recent_searches', views.delete_recent_searches, name="최근검색어삭제"),
    path('auth/mypage/all_recent_delete', views.all_recent_delete, name="최근검색어전체삭제"),
    path('auth/mypage/bookmark/delete_recent_searches', views.delete_recent_searches, name="최근검색어삭제"),
    path('auth/mypage/bookmark/all_recent_delete', views.all_recent_delete, name="최근검색어전체삭제"),
    path('auth/mypage/draw/delete_recent_searches', views.delete_recent_searches, name="최근검색어삭제"),
    path('auth/mypage/draw/all_recent_delete', views.all_recent_delete, name="최근검색어전체삭제"),
    path('auth/mypage/comment/delete_recent_searches', views.delete_recent_searches, name="최근검색어삭제"),
    path('auth/mypage/comment/all_recent_delete', views.all_recent_delete, name="최근검색어전체삭제"),
    path('auth/mypage/board/delete_recent_searches', views.delete_recent_searches, name="최근검색어삭제"),
    path('auth/mypage/board/all_recent_delete', views.all_recent_delete, name="최근검색어전체삭제"),
    path('auth/mypage/review/delete_recent_searches', views.delete_recent_searches, name="최근검색어삭제"),
    path('auth/mypage/review/all_recent_delete', views.all_recent_delete, name="최근검색어전체삭제"),
    path('auth/mypage/settings/delete_recent_searches', views.delete_recent_searches, name="최근검색어삭제"),
    path('auth/mypage/settings/all_recent_delete', views.all_recent_delete, name="최근검색어전체삭제"),

    path('googleCrawl', views.googleCrawl, name="googleCrawl"),

    path('crawl', cron.crawl2, name='crawl'),
    path('imgchange', cron.imgchange, name='imgchange'),

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

