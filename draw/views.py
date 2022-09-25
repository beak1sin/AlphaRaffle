from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from .models import Shoe, Member, Shoeimg, Shoesite
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta, datetime
from django.db.models import Q
import time
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core import serializers
from django.contrib import messages
import json
from pathlib import Path
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

# 기존 회원가입 방식   
# @csrf_exempt
# def member_insert(request):
#     context = {}

#     # memberid = request.POST['member_id']
#     # memberpwd = request.POST['member_pwd']
#     # memberrealname = request.POST['member_realname']
#     # membernickname = request.POST['member_nickname']
#     # memberbirth = request.POST['member_birth']
#     # membernikeid = request.POST['member_nikeid']
#     # memberphonenumber = request.POST['member_phonenumber']

#     # memberid = request.POST.get('member_id')
#     # memberpwd = request.POST.get('member_pwd')
#     # memberrealname = request.POST.get('member_realname')
#     # membernickname = request.POST.get('member_nickname')
#     # memberbirth = request.POST.get('member_birth')
#     # membernikeid = request.POST.get('member_nikeid')
#     # memberphonenumber = request.POST.get('member_phonenumber')

#     memberid = request.GET['member_id']
#     memberpwd = request.GET['member_pwd']
#     memberrealname = request.GET['member_realname']
#     membernickname = request.GET['member_nickname']
#     memberbirth = request.GET['member_birth']
#     membernikeid = request.GET['member_nikeid']
#     memberphonenumber = request.GET['member_phonenumber']


#     rs = Member.objects.create(member_id=memberid,
#                                member_pwd=memberpwd,
#                                member_realname=memberrealname,
#                                member_nickname=membernickname,
#                                member_birth=memberbirth,
#                                member_nikeid=membernikeid,
#                                member_phonenumber=memberphonenumber,
#                                usage_flag='1',
#                                register_date=datetime.now()
#                                )

#     context['flag'] = '1'
#     context['result_msg'] = '회원가입 되었습니다. Home에서 로그인하세요.'

#     return JsonResponse(context, content_type="application/json")

# 새로운 회원가입 방식
@csrf_exempt
def member_insert(request):
    context = {}

    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)

    memberid = bodyjson['member_id']
    memberpwd = bodyjson['member_pwd']
    memberrealname = bodyjson['member_realname']
    membernickname = bodyjson['member_nickname']
    memberbirth = bodyjson['member_birth']
    membernikeid = bodyjson['member_nikeid']
    memberphonenumber = bodyjson['member_phonenumber']

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
    context['result_msg'] = '회원가입 되었습니다. Home에서 로그인하세요.'

    return JsonResponse(context, content_type="application/json")

def home(request):
    context = {}
    shoe = Shoe.objects.all()
    
    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk= member_no)
        #print(member_no)

    else:
        member_no = None
        member = None

    context["member_no"] = member_no
    context = {'shoe':shoe, 'member':member }
    return render(request, "draw/main.html", context)

# 기존 멤버로그인 
# @csrf_exempt
# def member_login(request):
#     context = {}
#     # memberid = request.POST['member_loginid']
#     # memberpwd = request.POST['member_loginpwd']

#     # memberid = request.POST.get('member_loginid')
#     # memberpwd = request.POST.get('member_loginpwd')

#     memberid = request.GET['member_loginid']
#     memberpwd = request.GET['member_loginpwd']
#     print(memberid)
#     print(memberpwd)
#     if 'member_no' in request.session:
#         context['flag'] = '1'
#         context['result_msg'] = 'Already Login 되어 있습니다.'

#     else:

#         rsTmp = Member.objects.filter(member_id=memberid, member_pwd=memberpwd)

#         if rsTmp:
#             # Session에 member_no를 저장
#             rsMember = Member.objects.get(member_id=memberid, member_pwd=memberpwd)
#             memberno = rsMember.member_no
#             membername = rsMember.member_realname
#             rsMember.access_latest = datetime.now()
#             rsMember.save()

#             request.session['member_no'] = memberno
#             request.session['member_nickname'] = membername

#             # context['flag'] = '0'
#             # context['result_msg'] = 'Login 성공... '
#             context = {
#                 'flag': '0',
#                 'result_msg': 'Login complete 성공...'
#             }
#             # return redirect('/')
#             # return render(request, "draw/main.html", context)
#         else:
#             context['flag'] = '1'
#             context['result_msg'] = 'Login error... 아이디와 비번을 확인하세요.'
#             # return render(request, 'draw/login.html')
#             # return render(request, "draw/login.html", context)
#     # return HttpResponseRedirect('auth/login/', context) 
#     # return JsonResponse(context, content_type="application/json; charset=utf-8")
#     return JsonResponse(context, json_dumps_params={'ensure_ascii': False}, status=200)
#     # queryset_json = json.loads(serializers.serialize('json', context, ensure_ascii=False))
#     # return JsonResponse({'reload_all': False, 'queryset_json': queryset_json})
#     # return render(request, "draw/main.html", context)

# 새로운 멤버로그인
@csrf_exempt
def member_login(request):
    context = {}

    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)

    memberid = bodyjson['member_loginid']
    memberpwd = bodyjson['member_loginpwd']

    if 'member_no' in request.session:
        context['flag'] = '1'
        context['result_msg'] = 'Already Login 되어 있습니다.'

    else:

        rsTmp = Member.objects.filter(member_id=memberid, member_pwd=memberpwd)

        if rsTmp:
            # Session에 member_no를 저장
            rsMember = Member.objects.get(member_id=memberid, member_pwd=memberpwd)
            memberno = rsMember.member_no
            membername = rsMember.member_realname
            rsMember.access_latest = datetime.datetime.now()
            rsMember.save()

            request.session['member_no'] = memberno
            request.session['member_nickname'] = membername

            context = {
                'flag': '0',
                'result_msg': 'Login complete 성공...'
            }
        else:
            context['flag'] = '1'
            context['result_msg'] = 'Login error... 아이디와 비번을 확인하세요.'
    return JsonResponse(context, content_type="application/json")

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

# 기존 회원정보수정 방식 
# @csrf_exempt
# def member_update(request):
#     context = {}

#     membernickname = request.GET['member_nickname']
#     memberbirth = request.GET['member_birth']
#     membernikeid = request.GET['member_nikeid']
#     memberphonenumber = request.GET['member_phonenumber']

#     if 'member_no' in request.session:
#         memberno = request.session['member_no']
#         rsMember = Member.objects.get(member_no=memberno)

#         rsMember.member_nickname = membernickname
#         rsMember.member_birth = memberbirth
#         rsMember.member_nikeid = membernikeid
#         rsMember.member_phonenumber = memberphonenumber
#         rsMember.save()

#         context['flag'] = '0'
#         context['result_msg'] = '정보 변경되었습니다'

#         return JsonResponse(context, content_type="application/json")
#         # return redirect('/')

#     else:
#         context['flag'] = '1'
#         context['result_msg'] = '회원 정보가 없습니다.'

#         return JsonResponse(context, content_type="application/json")

# 새로운 회원정보수정 방식
@csrf_exempt
def member_update(request):
    context = {}

    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)

    membernickname = bodyjson['member_nickname']
    memberbirth = bodyjson['member_birth']
    membernikeid = bodyjson['member_nikeid']
    memberphonenumber = bodyjson['member_phonenumber']

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
    pk = request.GET['serialnum']

    context = {}

    shoe = get_object_or_404(Shoe, serialno=pk) 
    #site = Shoesite.objects.filter(Q(serialno=pk)&Q(Published_date__gte=start_date, Published_date__lte=end_date))
    site = Shoesite.objects.filter(serialno=pk)
    img = get_object_or_404(Shoeimg, serialno=pk) 
    print(pk)
    print(site)
    print(img)
    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk= member_no)
        print(member_no)

    else:
        member_no = None
        member = None

    context["member_no"] = member_no
    context = {'shoe':shoe, 'member':member, 'site': site, 'img':img }
    print(shoe.serialno)
    return render(request, 'draw/details.html', context)
    #return JsonResponse(context, content_type="application/json")

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

@csrf_exempt
def member_delete(request):
    context = {}
    memberpwd = request.GET.get('member_pwd')
    memberno = request.session['member_no']
    rsMember = Member.objects.get(member_no=memberno)

    if (rsMember.member_pwd == memberpwd):
        Member.objects.get(member_no=memberno).delete()
        request.session.flush()
        context['flag'] = '1'
        context['result_msg'] = '회원 탈퇴 완료하였습니다.'
    else:
        context['flag'] = '0'
        context['result_msg'] = '비밀번호가 일치하지 않습니다.'

    return JsonResponse(context, content_type="application/json")

def practice(request):
    return render(request, 'draw/practice.html')



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
from bs4 import BeautifulSoup
import time
import re
import os
import shutil
import json
import requests
import datetime

currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
year = date.strftime("%Y")
drawpath = Path(__file__).resolve().parent
#======== 셀 레 니 움 설 정 ========#
#options = webdriver.ChromeOptions()
#헤들리스로 만들기-----------------
#options.add_argument('headless')
#options.add_argument('--disable-gpu')
#options.add_argument('lang=ko_KR')
#----------------------------------
def luckd_crowler(no):
    path = 'C:/Users/mundd/chromedriver.exe'
    #driver = webdriver.Chrome(path,chrome_options=options)
    url = 'https://www.luck-d.com/release/product/%d/'%no
    #print(no)
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    time.sleep(0.01)
    #신발 한글이름
    shoename = soup.select("h3.page_title")[0].text
    #신발 영어이름
    try:
        subname  = soup.select("h5.sub_title")[0].text
    except:
        subname = shoename

    #신발 이미지 링크들
    imglist = []
    imglen  = soup.select("div.carousel-inner>div.item")


    #제품코드
    product_info_data = soup.select('span.product_info_data')

    serialno = product_info_data[1].text
    ###제품설명
    #product_detail = soup.select(' div.product_info_div > div:nth-child(1) > div')[0].text.strip() 
    #print(product_detail)

    try:
        Shoe.objects.create(shoename = shoename , shoeengname = subname, serialno = serialno, shoethumbnail = os.path.join(str(drawpath)+"/static/draw/images/"+shoename+str(0)+'.jpeg'))
    except:
        pass
    try:
        shoe = Shoe.objects.get(serialno = serialno)
    except:
        pass


    for i in range(len(imglen)):
        img_file = imglen[i].img['src']
        img_name = os.path.join(str(drawpath)+"/static/draw/images/"+shoename+str(i)+'.jpeg')
        try:
            Shoeimg.objects.create(serialno= serialno, shoeimg = img_name)
            urllib.request.urlretrieve(img_file, img_name)
        except:
            pass

    #사이트별 
    sitecard = soup.select('div.site_card')    
    for i in range(len(sitecard)):
        #사이트명
        sitename = soup.select('h4.agent_site_title')[i].text
        #로고
        logo_file = sitecard[i].img['src']
        logo_name = str(drawpath)+"/static/draw/logoimg/"+sitename+'.jpeg'
        urllib.request.urlretrieve(logo_file, logo_name)
      
 
        #종료일
        end_date = soup.select('p.release_date_time')[i].text
        if end_date == '종료':
            end_date = '2022-09-01 00:00:00'
        else :
            end_date = end_date.replace("월",'-')
            end_date = end_date.replace("일",'')
            end_date = end_date.replace("까",'')
            end_date = end_date.replace("지",'')
            end_date = end_date.replace(" ",'')
            end_date = "".join(end_date)
            end_date = year +'-'+ end_date 
        #링크
        link = sitecard[i].a['href']
        try:
            Shoesite.objects.create(serialno = serialno , logoimg = logo_name, sitename = sitename, sitelink = link )
        except:
            pass

def crawl(request):
    url = 'https://www.luck-d.com/'
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    time.sleep(0.01)
    shoenum = []
    
    sitecard = soup.select('div.site_card')
    for i in range(len(sitecard)):
        link = sitecard[i].a['href']
        shoenum.append(link[17:21].split('/')[0])
    print(shoenum)

    for num in shoenum:
        try:
            luckd_crowler(int(num))

        except:
            pass
    return render(request, "draw/main.html")