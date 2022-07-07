from django.urls import path
from draw import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'draw'

urlpatterns = [

    path('',views.home, name = '홈'),
    path('auth/login/', views.login, name='로그인'),
    path('auth/logout/', views.logout, name='로그아웃'),
    path('auth/mypage/', views.myPage, name='마이페이지'),
    path('auth/details/', views.details, name='상세정보'),
    path('auth/delete/', views.delete, name='회원탈퇴'),
    path('member_idcheck', views.member_idcheck, name='member_idcheck'),
    path('member_insert', views.member_insert, name='member_insert'),
    path('member_login', views.member_login, name='member_login'),
    path('auth/mypage/member_update', views.member_update, name='member_update'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

