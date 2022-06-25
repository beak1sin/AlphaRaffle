from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from .models import Shoe, Member
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta, datetime
import schedule
from django.db.models import Q
import time
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
User = get_user_model()
# Create your views here.

def member_register(request):
    return render(request, 'draw/login.html')

@csrf_exempt
def member_idcheck(request):
    context = {}
    memberid = request.GET['member_id']

    rs = Member.objects.filter(member_id=memberid)

    if (len(rs)) > 0:
        context['flag'] = '1'
        context['result_msg'] = '아이디가 있습니다.'
    else:
        context['flag'] = '0'
        context['result_msg'] = '사용 가능한 아이디 입니다.'

    return JsonResponse(context, content_type="application/json")

@csrf_exempt
def member_insert(request):
    context = {}

    memberid = request.POST['member_id']
    memberpwd = request.POST['member_pwd']
    memberrealname = request.POST['member_realname']
    membernickname = request.POST['member_nickname']
    memberbirth = request.POST['member_birth']
    membernikeid = request.POST['member_nikeid']
    memberphonenumber = request.POST['member_phonenumber']

    rs = Member.objects.create(member_id=memberid,
                               member_pwd=memberpwd,
                               member_realname=memberrealname,
                               member_nickname=membernickname,
                               member_birth=memberbirth,
                               member_nikeid=membernikeid,
                               member_phonenumber=memberphonenumber,
                               usage_flag='1',
                               register_date=datetime.now()
                               )

    context['flag'] = '1'
    context['result_msg'] = '회원가입 되었습니다.<br>Home에서 로그인하세요.'

    return JsonResponse(context, content_type="application/json")


def home(request):
    return render(request, 'draw/login.html')

def login(request):
    return render(request, 'draw/login.html')

def logout(request):
    return render(request, 'draw/login.html')

def create(request):
    return render(request, 'draw/login.html')

def myPage(request):
    return render(request, 'draw/login.html')
