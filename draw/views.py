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
from django.contrib import messages

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
        context['result_msg'] = '이미 존재하는 아이디입니다.'
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
    context = {}
    shoe = Shoe.objects.all()
    
    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk= member_no)
        print(member_no)

    else:
        member_no = None
        member = None

    context["member_no"] = member_no
    context = {'shoe':shoe, 'member':member }
    return render(request, "draw/main.html", context)


@csrf_exempt
def member_login(request):
    context = {}
    memberid = request.POST['member_loginid']
    memberpwd = request.POST['member_loginpwd']

    if 'member_no' in request.session:
        context['flag'] = '1'
        context['result_msg'] = 'Login 되어 있습니다.'
    else:

        rsTmp = Member.objects.filter(member_id=memberid, member_pwd=memberpwd)

        if rsTmp:
            # Session에 member_no를 저장
            rsMember = Member.objects.get(member_id=memberid, member_pwd=memberpwd)
            memberno = rsMember.member_no
            membername = rsMember.member_realname
            rsMember.access_latest = datetime.now()
            rsMember.save()

            request.session['member_no'] = memberno
            request.session['member_name'] = membername

            context['flag'] = '0'
            context['result_msg'] = 'Login 성공... '
            return redirect('/')

        else:
            context['flag'] = '1'
            context['result_msg'] = 'Login error... 아이디와 비번을 확인하세요.'
            messages.info(request, 'Your password has been changed successfully!')
            return render(request, 'draw/login.html')
    return redirect('/')

    

@csrf_exempt
def logout(request):
    context = {}

    request.session.flush()
    return redirect('/')

@csrf_exempt
def login(request):
    return render(request, 'draw/login.html')

@csrf_exempt
def myPage(request):

    # context = {}
    # shoe = Shoe.objects.all()
    
    # if request.session.has_key('member_no'):
    #     member_no = request.session['member_no']
    #     member = Member.objects.get(pk= member_no)
    #     print(member_no)

    # else:
    #     member_no = None
    #     member = None

    # context["member_no"] = member_no
    # context = {'shoe':shoe, 'member':member }
    # return render(request, "draw/myPage.html", context)

    context = {}

    if 'member_no' in request.session:
        memberno = request.session['member_no']
        member = Member.objects.get(member_no=memberno)
        context['member_no'] = member.member_no
        context['member_id'] = member.member_id
        context['member_realname'] = member.member_realname
        context['member_nickname'] = member.member_nickname
        context['member_phonenumber'] = member.member_phonenumber
        context['member_nikeid'] = member.member_nikeid
        context['member_birth'] = member.member_birth

        context['flag'] = "0"
        context['result_msg'] = "Member read..."
        context = {'member':member }
        return render(request, "draw/myPage.html", context)

    else:
        return redirect('/')

@csrf_exempt
def member_update(request):
    context = {}

    membernickname = request.GET['member_nickname']
    memberbirth = request.GET['member_birth']
    membernikeid = request.GET['member_nikeid']
    memberphonenumber = request.GET['member_phonenumber']

    if 'member_no' in request.session:
        memberno = request.session['member_no']
        rsMember = Member.objects.get(member_no=memberno)

        rsMember.member_nickname = membernickname
        rsMember.member_birth = memberbirth
        rsMember.member_nikeid = membernikeid
        rsMember.member_phonenumber = memberphonenumber
        rsMember.save()

        context['flag'] = '0'
        context['result_msg'] = '정보 변경되었습니다'

        return JsonResponse(context, content_type="application/json")
        # return redirect('/')

    else:
        context['flag'] = '1'
        context['result_msg'] = '회원 정보가 없습니다.'

        return JsonResponse(context, content_type="application/json")

@csrf_exempt
def details(request):
    context = {}
    shoe = Shoe.objects.all()
    
    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk= member_no)
        print(member_no)

    else:
        member_no = None
        member = None

    context["member_no"] = member_no
    context = {'shoe':shoe, 'member':member }
    return render(request, "draw/details.html", context)

@csrf_exempt
def delete(request):
    context = {}
    shoe = Shoe.objects.all()
    
    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk= member_no)
        print(member_no)

    else:
        member_no = None
        member = None

    context["member_no"] = member_no
    context = {'shoe':shoe, 'member':member }
    return render(request, "draw/delete.html", context)






