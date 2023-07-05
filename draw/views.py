from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import auth
from urllib.parse import quote
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from draw.models import Shoe, Member, Shoeimg, Shoesite, Shoesiteimg, Comment, SearchTerm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
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
from django.core.mail import send_mail

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone

nowtime = timezone.now()
User = get_user_model()
# Create your views here.

@csrf_protect
def start(request):
    context = {}
    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk= member_no)
        #print(member_no)
        
    else:
        member_no = None
        member = None

    context["member_no"] = member_no
    context = {'member':member }

    return render(request, 'draw/start.html', context)

@csrf_protect
def member_idcheck(request):
    context = {}

    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    memberid = bodyjson['member_id']

    rs = Member.objects.filter(member_id=memberid)

    if (len(rs)) > 0:
        context['flag'] = '1'
        context['result_msg'] = '이미 존재하는 아이디입니다.'
    else:
        context['flag'] = '0'
        context['result_msg'] = '사용 가능한 아이디 입니다.'

    return JsonResponse(context, content_type="application/json")

# 새로운 회원가입 방식
@csrf_protect
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
                               register_date=datetime.datetime.now()
                               )
    rs.save()

    current_site = get_current_site(request)
    message = render_to_string('draw/user_activate_email.html',                         {
                'user': rs,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(rs.pk)).encode().decode(),
                'token': account_activation_token.make_token(rs),
            })
    mail_subject = "[AlphaRaffle] 회원가입 인증 메일입니다."
    user_email = rs.member_id
    email = EmailMessage(mail_subject, message, to=[user_email])
    email.send()

    context['flag'] = '1'
    # context['result_msg'] = '회원가입 인증메일을 보냈습니다. 인증 후 로그인 바랍니다.'
    context['result_msg'] = '회원가입이 완료되었습니다.'

    return JsonResponse(context, content_type="application/json")

# 메일 인증
@csrf_protect
def send_mail(request):
    bodydata = request.body.decode('utf-8')
    context = {}
    bodyjson = json.loads(bodydata)
    memberid = bodyjson['member_loginid']
    rs = Member.objects.get(member_id=memberid)
    current_site = get_current_site(request)
    message = render_to_string('draw/user_activate_email.html',                         {
                'user': rs,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(rs.pk)).encode().decode(),
                'token': account_activation_token.make_token(rs),
            })
    mail_subject = "[AlphaRaffle] 회원가입 인증 메일입니다."
    user_email = rs.member_id
    email = EmailMessage(mail_subject, message, to=[user_email])
    email.send()
    context['flag'] = '0'
    context['result_msg'] = '회원가입 재인증메일을 보냈습니다. 인증 후 로그인 바랍니다.'
    return JsonResponse(context, content_type="application/json")

# 메일 인증 토큰
def activate(request, uid64, token):

    uid = force_str(urlsafe_base64_decode(uid64))
    user = Member.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        # return HttpResponse('메일인증 성공')
        current_domain = request.META['HTTP_HOST']

        # 도메인 이동 버튼을 포함한 HTML 페이지 반환
        return HttpResponse('''
            <h1>메일 인증 성공!</h1>
            <p>메일 인증이 성공적으로 완료되었습니다.</p>
            <a href="https://{}/">이동하기</a>
        '''.format(current_domain))
    else:
        return HttpResponse('비정상적인 접근입니다.')

def home3(request):
    context = {}
    droppedSite = Shoesite.objects.filter(end_date__gte=nowtime).order_by('-end_date')
    endSite = Shoesite.objects.filter(end_date__lt=nowtime).order_by('-end_date')
    droppedSerial = []
    endSerial = []
    for site in droppedSite:
        droppedSerial.append(site.serialno)
    for site in endSite:
        endSerial.append(site.serialno)
    # print(serial)
    droppedShoe = Shoe.objects.filter(serialno__in = droppedSerial)
    print(droppedShoe)
    endShoe = Shoe.objects.filter(serialno__in = endSerial)
    # print(shoe)
    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk= member_no)
        #print(member_no)

    else:
        member_no = None
        member = None

    context["member_no"] = member_no
    context = {'droppedShoe':droppedShoe, 'endShoe':endShoe, 'member':member }
    return render(request, "draw/main3.html", context)

# @csrf_protect
# def home(request):
#     context = {}
#     shoe = Shoe.objects.all()
#     # for shoe in shoe:
#     #     shoecount = ShoeLike.objects.filter(serialno = shoe.serialno)
#     #     context["shoecount"] = zip(shoecount)
#     if request.session.has_key('member_no'):
#         member_no = request.session['member_no']
#         member = Member.objects.get(pk= member_no)
        
#     else:
#         member_no = None
#         member = None

    
#     # shoeLike = ShoeLike.objects.all().values('member_no')
    
#     # sh1 = shoeLike.values('member_no')
    
#     context = { 'shoe':shoe, 'member':member}

#     return render(request, "draw/main.html", context)

@csrf_protect
def home(request):
    # shoe = Shoe.objects.all()[0:12]
    # shoe = Shoe.objects.all().order_by('-id')[0:12]
    member = None
    member_no = None

    droppedSite = Shoesite.objects.filter(end_date__gte=nowtime).order_by('end_date')   #진행중
    endSite = Shoesite.objects.filter(end_date__lt=nowtime).order_by('-end_date')       #종료
    upcomingSite = Shoesite.objects.filter(pub_date__gt=nowtime).order_by('pub_date')   #발매예정
    droppedSerial = []
    endSerial = []
    upcomingSerial = []

    for site in droppedSite:
        droppedSerial.append(site.serialno)
    for site in endSite:
        endSerial.append(site.serialno)
    for site in upcomingSite:
        upcomingSerial.append(site.serialno)

    droppedShoe = Shoe.objects.filter(serialno__in = droppedSerial)
    endShoe = Shoe.objects.filter(serialno__in = endSerial).order_by('-id')[0:12]
    upcomingShoe = Shoe.objects.filter(serialno__in = upcomingSerial)

    endShoe_count = Shoe.objects.filter(serialno__in = endSerial).count()

    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk=member_no)

    context = {'member': member, 'droppedShoe': droppedShoe, 'endShoe': endShoe, 'upcomingShoe': upcomingShoe ,'endShoe_count': endShoe_count}  # member 객체를 context에 추가

    if request.method == 'POST':
        context2 = {}
        bodydata = request.body.decode('utf-8')
        bodyjson = json.loads(bodydata)
        page = bodyjson['page']
        
        per_page = 12
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        # shoe = Shoe.objects.all()[start_index:end_index]
        # shoe = Shoe.objects.all().order_by('-id')[start_index:end_index]
        endShoe = Shoe.objects.filter(serialno__in = endSerial).order_by('-id')[start_index:end_index]
        # shoes = serializers.serialize('json', shoe)
        shoes = serializers.serialize('json', endShoe)
        likes = []  # 멤버별 신발 좋아요 여부를 저장할 리스트

        if request.session.has_key('member_no'):
            member_no = request.session['member_no']
            member = Member.objects.get(pk=member_no)
            # for shoe in shoe:
            #     likes.append(member in shoe.likes.all())
            for shoe in endShoe:
                likes.append(member in shoe.likes.all())
        context2 = {'shoes': shoes, 'likes': likes}
        return JsonResponse(context2, content_type="application/json")

    return render(request, "draw/main.html", context)

# 새로운 멤버로그인
@csrf_protect
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
            is_active = rsMember.is_active

            if is_active:
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
                context['member_loginid'] = memberid
                context['flag'] = '1'
                context['inactive'] = '1'
                context['result_msg'] = '비활성화 되어 있습니다. 인증 후 로그인 바랍니다.'
        else:
            context['flag'] = '1'
            context['result_msg'] = 'Login error... 아이디와 비번을 확인하세요.'
    return JsonResponse(context, content_type="application/json")

@csrf_protect
def logout(request):
    context = {}

    request.session.flush()
    return redirect('/')

@csrf_protect
def login(request):
    context = {}

    if request.session.has_key('member_no'):
        shoe = Shoe.objects.filter()
        member_no = request.session['member_no']
        member = Member.objects.get(pk= member_no)
        context["member_no"] = member_no
        context = {'shoe':shoe, 'member':member }
        
        # return render(request, 'draw/main.html', context)
        return redirect('/main/')

    else:
        member_no = None
        member = None
        return render(request, 'draw/login.html', context)

    

    return render(request, 'draw/login.html', context)

@csrf_protect
def join(request):
    return render(request, 'draw/join.html')

@csrf_protect
def myPage(request):

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

        liked_shoes = member.liked_posts.all()

        context = {'member':member ,'liked_shoes':liked_shoes}
        return render(request, "draw/myPage.html", context)

    else:
        return redirect('/auth/login/')

# 새로운 회원정보수정 방식
@csrf_protect
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

@csrf_protect
def details(request):
    pk = request.GET['serialnum']

    context = {}

    shoe = get_object_or_404(Shoe, serialno=pk) 
    #site = Shoesite.objects.filter(Q(serialno=pk)&Q(Published_date__gte=start_date, Published_date__lte=end_date))
    site = Shoesite.objects.filter(serialno=pk)
    notGoogleSite = site.exclude(sitelink__contains='google')
    googleSite = Shoesite.objects.filter(serialno=pk, sitelink__contains='google')
    # print(googleSite)
    # print(type(googleSite))
    googleSiteOnly = {}
    # if googleSite 
    for googleSiteGet in googleSite.values():
        print('00000000')
        # print(type(googleSiteGet))
        # print(googleSiteGet['sitelink'])
        url = googleSiteGet['sitelink']
        url = googleFormCrawl(url)
        # print(url)
        googleSiteGet['sitelink'] = url
        # print(googleSiteGet['sitelink'])
        googleSiteOnly = googleSiteGet
        print(googleSiteOnly)
    img = Shoeimg.objects.filter(serialno=pk)
    
    shoebrand = shoe.shoebrand.split(' ')

    while 'x' in shoebrand:
        shoebrand.remove('x')
    
    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk= member_no)
        #print(member_no)

    else:
        member_no = None
        member = None

    # 댓글
    comment = Comment.objects.filter(serialno=pk)
    if comment.values():
        pass
    else:
        comment = {'serialno': ''}

    context["member_no"] = member_no
    context = {'shoe':shoe, 'member':member, 'site': site, 'img':img, 'shoebrand': shoebrand, 'notGoogleSite': notGoogleSite, 'googleSite': googleSite, 'googleSiteOnly': googleSiteOnly, 'comment': comment }
    #print(shoe.serialno)
    return render(request, 'draw/details.html', context)
    #return JsonResponse(context, content_type="application/json")

@csrf_protect
def update_views(request):
    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)

    pk = bodyjson['serialnoAJAX']

    context = {}

    shoe = get_object_or_404(Shoe, serialno=pk) 
    shoe.increase_views()
    return JsonResponse(context, content_type="application/json")
    
@csrf_protect
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

@csrf_protect
def member_delete(request):
    context = {}

    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)

    memberpwd = bodyjson['member_pwd']

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
@csrf_exempt
def search(request):
    
        #?serialno=recent_searches
    return render(request, "draw/full?serialno=.html", context)
    
@csrf_protect
def full(request):
    shoe = Shoe.objects.all().order_by('-id')[0:12]
    member = None
    member_no = None
    recent_searches = None
    term = None
    shoe_count = Shoe.objects.all().count()

    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk=member_no)
        recent_searches = SearchTerm.objects.filter(member_no=member_no).order_by('-created_at')[:10]

    if request.method == 'GET':
        term = request.GET.get("search_term")
        print(term)
        if term != None:
            recent = SearchTerm.objects.filter(term=term,member_no=member_no)
            if recent !=None:
                recent.delete()
            try: 
                SearchTerm.objects.create(term=term,member_no=member_no)
            except:
                pass
            shoe = Shoe.objects.filter(shoename__contains = term).order_by('-id')[0:12]
            shoe_count = Shoe.objects.filter(shoename__contains = term).count()
        else:
            shoe = Shoe.objects.all().order_by('-id')[0:12]
            shoe_count = Shoe.objects.all().count()
        context = {'shoe': shoe, 'member': member, 'shoe_count': shoe_count ,'recent_searches': recent_searches}

    context = {'shoe': shoe, 'member': member, 'shoe_count': shoe_count ,'recent_searches': recent_searches}  # member 객체를 context에 추가

    if request.method == 'POST':
        context2 = {}
        bodydata = request.body.decode('utf-8')
        bodyjson = json.loads(bodydata)
        page = bodyjson['page']
        per_page = 12
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        # shoe = Shoe.objects.all()[start_index:end_index]
        # shoe = Shoe.objects.all().order_by('-id')[start_index:end_index]
        term = request.GET.get("search_term")
        if term != None:
            shoe = Shoe.objects.filter(shoename__contains = term).order_by('-id')[start_index:end_index]
            shoe_count = Shoe.objects.filter(shoename__contains = term).count()
        else:
            shoe = Shoe.objects.all().order_by('-id')[start_index:end_index] 
            shoe_count = Shoe.objects.all().count()           
        shoes = serializers.serialize('json', shoe)
        likes = []  # 멤버별 신발 좋아요 여부를 저장할 리스트

        if request.session.has_key('member_no'):
            member_no = request.session['member_no']
            member = Member.objects.get(pk=member_no)
            for shoe in shoe:
                likes.append(member in shoe.likes.all())
        context2 = {'shoes': shoes, 'likes': likes}
        return JsonResponse(context2, content_type="application/json")

    return render(request, "draw/full.html", context)


@csrf_protect
def like_shoe(request):
    context = {}
    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    serialno = bodyjson['serialnoAJAX']
    
    shoe = get_object_or_404(Shoe, serialno=serialno)

    if 'member_no' in request.session:
        member_no = request.session['member_no']
        member_no_obj = Member.objects.get(member_no=member_no)
        context['flag'] = '1'
        context['result_msg'] = '로그인 되어 있는 상태'
        # if member_no in shoe.likes.all():
        #     shoe.likes.remove(member_no)
        #     liked = False
        # else:
        #     shoe.likes.add(member_no)
        #     liked = True
        if Member.objects.filter(member_no=member_no, liked_posts=shoe).exists():
            # 이미 좋아요한 경우
            shoe.likes.remove(member_no)
            shoe.shoelikecount -= 1
            liked = False
        else:
            # 좋아요하지 않은 경우
            shoe.likes.add(member_no)
            shoe.shoelikecount += 1
            liked = True
        shoe.save()
        context['liked'] = liked
        context['count'] = shoe.shoelikecount
        context["member_no"] = member_no_obj.member_no
    else:
        context['flag'] = '0'
        context['result_msg'] = '로그인이 필요한 서비스 입니다'
        member_no_obj = None
        member_no = None
    
    return JsonResponse(context, content_type="application/json")

@csrf_protect
def filtering(request):
    context = {}
    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    
    brandList = bodyjson['brandListAJAX']
    regionList = bodyjson['regionListAJAX']
    onofflineList = bodyjson['onofflineListAJAX']
    releaseList = bodyjson['releaseListAJAX']
    deliveryList = bodyjson['deliveryListAJAX']
    print('------------------------')
    print(brandList, regionList, onofflineList, releaseList, deliveryList)
    # for i in range(len(brandList)):
    #     shoe = list(Shoe.objects.filter(shoebrand = brandList[i]).values())
    # print(shoe)
    shoe = list(Shoe.objects.filter(shoebrand__in=brandList).values())
    print(shoe)
    context['flag'] = '0'
    context['result_msg'] = '필터링 작업'
    context['shoe'] = shoe
    return JsonResponse(context, content_type="application/json")

@csrf_protect
def like(request):
    context = {}
    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    
    serial_no = str(' ') + str(bodyjson['serialnoAJAX'])
    #print('serialno =', serial_no)
    
    #print(shoe)
    if 'member_no' in request.session:
        member_no = request.session['member_no']
        #shoe = Shoe.objects.get(serialno=serialno)
        shoe = Shoe.objects.get(serialno = serial_no)
        # member = Member.objects.filter(member_no=member_no)
        # shoe.shoelikeuser.add(member.member_no)

        context['flag'] = '1'
        context['result_msg'] = '로그인 되어 있는 상태'
    else :
        context['flag'] = '0'
        context['result_msg'] = '로그인이 필요한 서비스 입니다'

    return JsonResponse(context, content_type="application/json")

@csrf_protect
def likeCancel(request):
    context = {}
    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    
    serialno = bodyjson['serialnoAJAX']
    
    if 'member_no' in request.session:
        member_no = request.session['member_no']
        rs = ShoeLike.objects.filter(Q(serialno=serialno)&Q(member_no = member_no))      
        rs.delete()

        context['flag'] = '1'
        context['result_msg'] = '로그인 되어 있는 상태'
    else :
        context['flag'] = '0'
        context['result_msg'] = '로그인이 필요한 서비스 입니다'

    return JsonResponse(context, content_type="application/json")

@csrf_protect
def reportLayer(request):
    context = {}
    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    
    if 'member_no' in request.session:
        context['flag'] = '1'
        context['result_msg'] = '로그인 되어 있는 상태'
    else :
        context['flag'] = '0'
        context['result_msg'] = '로그인 안되어 있는 상태'

    return JsonResponse(context, content_type="application/json")

@csrf_protect
def report(request):
    context = {}
    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    reportValue = bodyjson['reportValueAJAX']
    
    if 'member_no' in request.session:
        context['flag'] = '1'
        context['result_msg'] = '신고완료'
        context['reportValue'] = reportValue
    else :
        context['flag'] = '0'
        context['result_msg'] = '로그인 안되어 있는 상태'

    return JsonResponse(context, content_type="application/json")

@csrf_protect
def comment(request):
    context = {}
    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    
    comment = bodyjson['commentValueAJAX']
    serialno = bodyjson['serialnoAJAX']
    
    if 'member_no' in request.session:
        member_no = request.session['member_no']
        member = Member.objects.get(member_no=member_no)
        comment_member_nickname = member.member_nickname

        rs = Comment.objects.create(serialno=serialno,
                                    comment=comment,
                                    member_nickname=comment_member_nickname,
                                    created_date=datetime.datetime.now(),
                                    approved_comment=False
                                    )
        rs.save()

        context['flag'] = '1'
        context['result_msg'] = '로그인 되어 있는 상태'
    else :
        context['flag'] = '0'
        context['result_msg'] = '로그인 안되어 있는 상태'

    return JsonResponse(context, content_type="application/json")
'''
@csrf_protect
def search(request):
    context = {}

    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk= member_no)
        #print(member_no)
        
    else:
        member_no = None
        member = None

    context["member_no"] = member_no
    context = {'member':member }
    
    return render(request, 'draw/search.html', context)
'''

def naverSearch(request):
    return render(request, 'draw/naver07438b501f2bcdb23c19460dc9cca09d.html')

def naverSearchwww(request):
    return render(request, 'draw/naver73749ca69b9eff6e2574852408ea3ecf.html')

def practice(request):
    return render(request, 'draw/practice.html')

from django.views.generic import View

class customHandler404(View):
    def get(self, request):
        context = {}
        return render(request, "draw/errors/404.html",context)
    
class customHandler500(View):
    def get(self, request):
        context = {}
        return render(request, "draw/errors/500.html",context)



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
import random

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
    #path = 'C:/Users/mundd/chromedriver.exe'
    #driver = webdriver.Chrome(path,chrome_options=options)
    url = 'https://www.luck-d.com/release/product/%d/'%no
    #print(no)
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    time.sleep(0.01)
    #신발 한글이름
    shoename = soup.select("h1.page_title")[0].text
    #신발 영어이름
    try:
        subname  = soup.select("h2.sub_title")[0].text
    except:
        subname = shoename

    #신발 브랜드
    try:
        shoebrandlist = soup.select('h3.brand')[0].text.split()
        shoebrand = ' '.join(shoebrandlist)
    except:
        shoebrand = '-'

    #신발 이미지 링크들
    imglist = []
    imglen  = soup.select("div.carousel-inner>div.item")


    detail_info = soup.select('ul.detail_info>li')

    for i in range(len(detail_info)):
        detail_info_find = soup.select('ul.detail_info>li')[i].text
        if '제품 코드' in detail_info_find:
            serialno = detail_info_find[5:]
        if '발매일' in detail_info_find:
            shoepubdate = detail_info_find[3:]
        if '가격' in detail_info_find:
            shoeprice = detail_info_find[2:]
        if '제품 설명' in detail_info_find:
            product_detail = detail_info_find[5:].strip()
        else:
            product_detail = '-'
    
    
    # print(serialno, shoepubdate, shoeprice, product_detail)

    if len(serialno) <= 2:
        print('no serial number')
        return 
    else:
        pass

    # print(shoename, subname, serialno, shoebrand, shoepubdate, product_detail, shoeprice)

    try:
        Shoe.objects.create(shoename = shoename , shoeengname = subname, serialno = serialno,
                        shoebrand = shoebrand, pubdate = shoepubdate, shoedetail = product_detail, shoeprice = shoeprice)
    except:
        print(no,'already exist shoe')
        pass
    
    shoeDB = Shoe.objects.filter(serialno = serialno)
    shoeDB.update(shoename = shoename , shoeengname = subname,
                    shoebrand = shoebrand, pubdate = shoepubdate, shoedetail = product_detail, shoeprice = shoeprice)
    
    if len(imglen)>=1:            
        for i in range(len(imglen)):
            img_file = imglen[i].img['src']
            img_name = os.path.join(str(Path(__file__).resolve().parent)+"/static/draw/images/"+shoename+serialno+str(i)+'.jpeg')
            
            try:
                Shoeimg.objects.create(serialno= serialno, shoeimg = shoename+serialno+str(i))
            except:
                pass
            
            urllib.request.urlretrieve(img_file, img_name)
    else:
        
        img2 = soup.select("div.img_div")
        img_file = img2[0].img['src']
        img_name = os.path.join(str(Path(__file__).resolve().parent)+"/static/draw/images/"+shoename+serialno+str(0)+'.jpeg')
        
        try:
            Shoeimg.objects.create(serialno= serialno, shoeimg = shoename+serialno+str(0))
        except:
            pass
        
        urllib.request.urlretrieve(img_file, img_name)
    
    
    #사이트별 
    sitecard = soup.select('div.release_card')    

    for i in range(len(sitecard)):
        #사이트명
        sitename = soup.select('div.release_card_header > span')[i].text
        #로고
        logo_file = sitecard[i].img['src']
        logo_name = str(Path(__file__).resolve().parent)+"/static/draw/logoimg/"+sitename+'.jpeg'
        #print(logo_file,logo_name)

        try:
            Shoesiteimg.objects.create(sitename = sitename)
        except:
            print('Shoesiteimg already exist or error')
            pass
        leng = len('https://static.luck-d.com/agent_site/')

        #print(quote(logo_file[leng:]), logo_name)
        urllib.request.urlretrieve('https://static.luck-d.com/agent_site/'+quote(logo_file[leng:]), logo_name)
        
        sitelink = sitecard[i].a['href']

        shoeunique = serialno+sitename+sitelink

        try:
            Shoesite.objects.create(serialno = serialno , sitename = sitename, sitelink = sitelink, shoesiteunique = shoeunique)
            # Shoesite.objects.create()
        except:
            pass
        # print(sitename, logo_file, sitelink)

        # #종료일
        end_date = soup.select('li.release_time > label > span')[i].text.strip()

        # #시간이 종료일 경우
        if '종료' in end_date:
            end_date = '2022-09-01 00:00:00'
            end_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
            Shoesite.objects.filter(shoesiteunique = shoeunique).update(end_date = end_date_datetime)
        else :
            # 시간이 까지일 경우
            if '까지' in end_date:
                end_date = end_date.replace("월",'-')
                end_date = end_date.replace(" ",'')
                end_date = end_date.replace("일",' ')
                end_date = end_date.replace("까",'')
                end_date = end_date.replace("지",'')
                # end_date = end_date + ":59"
                end_date = "".join(end_date)
                end_date = year +'-'+ end_date
                if len(end_date) == 11:
                    end_date = end_date.replace(" ",'')
                    end_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                elif len(end_date) == 16:
                    end_date = end_date + ":59"
                    end_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
                    
                Shoesite.objects.filter(shoesiteunique = shoeunique).update(end_date = end_date_datetime)
            # 시간이 발매 시작일 경우
            else:
                end_date = end_date.replace("월",'-')
                end_date = end_date.replace(" ",'')
                end_date = end_date.replace("일",' ')
                end_date = end_date.replace("발",'')
                end_date = end_date.replace("매",'')      
                # end_date = end_date + ":59"
                end_date = "".join(end_date)
                end_date = year +'-'+ end_date
                if len(end_date) == 11:
                    end_date = end_date.replace(" ",'')
                    pub_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                elif len(end_date) == 16:
                    end_date = end_date + ":59"
                    pub_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
                
                Shoesite.objects.filter(shoesiteunique = shoeunique).update(pub_date = pub_date_datetime)

def crawl(request):
    url = 'https://www.luck-d.com/'
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    time.sleep(0.01)
    shoenum = []
    
    sitecard = soup.select('div.product_info_layer > div.product_thumb')

    for i in range(len(sitecard)):    
        link = sitecard[i].attrs['onclick']
        shoenum.append(link[39:].split('/')[0])
    
    shoenum = list(set(shoenum))
    print(shoenum)

    for num in shoenum:
        now = datetime.datetime.now()
        print(now)
        randomTime = random.randint(30, 60)
        luckd_crowler(int(num))
        time.sleep(randomTime)

    return redirect('/')

# 티셔츠 신청 test7 (202302131500)
# 티셔츠 신청
def googleFormCrawl(url):
    # url = 'https://docs.google.com/forms/d/e/1FAIpQLSeD5cUf-XH9Q5lxF3_EQurNnnXNolM-oARjVxnW7XP2QVx9sA/viewform'
    # url = 'https://docs.google.com/forms/d/e/1FAIpQLSc_RlwPQjfqI7DRfEf9CFzNTQbI6pmqOkI26FfJ5kvj7V6A5g/viewform'
    # url = 'https://docs.google.com/forms/d/e/1FAIpQLSc_RlwPQjfqI7DRfEf9CFzNTQbI6pmqOkI26FfJ5kvj7V6A5g/formResponse'
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    matched = re.search(r'var FB_PUBLIC_LOAD_DATA_ = (.*);', html, re.S)
    # print('------------------------')
    # print(matched)
    if matched == None:
        return url
    entryList = matched.group(1)
    output_entryList = json.loads(entryList)

    output_entryList2 = []
    for i in range(len(output_entryList[1][1])):
        output_entryList2.append(output_entryList[1][1][i])
        

    googleEntry = []
    for i in range(len(output_entryList2)):
        # print(output_entryList2[i])
        # print()

        # 타이틀
        title = output_entryList2[i][1]
        
        # checkbox value 값
        # try:
        #     print(output_entryList2[i][4][0][1][0][0])
        # except:
        #     None
        try:
            checkboxValue = output_entryList2[i][4][0][1][0][0]
        except:
            checkboxValue = None
        
        # checkbox entry 값
        # try:
        #     print(output_entryList2[i][4][0][0])
        # except:
        #     None
        try:
            entry = output_entryList2[i][4][0][0]
        except:
            entry = None
            
        # input 글자 제한 수
        try:
            inputLimitChar = output_entryList2[i][4][0][4][0][2][0]
        except:
            inputLimitChar = None
        
        # 유형 index(0: input, 3: dropdown, 4: checkbox, 8: text)
        # print(output_entryList2[i][3])
        index = output_entryList2[i][3]

        # 체크박스 개수
        # try:
        #     print(len(output_entryList2[i][4][0][1]))
        # except:
        #     None
        try:
            checkboxLength = len(output_entryList2[i][4][0][1])
        except:
            checkboxLength = None
        
        # print(title, 'index:'+ str(index), checkboxLength, entry, checkboxValue, inputLimitChar)
        googleEntry.append([])
        googleEntry[i].append(title)
        googleEntry[i].append(index)
        googleEntry[i].append(checkboxLength)
        googleEntry[i].append(entry)
        googleEntry[i].append(checkboxValue)
        googleEntry[i].append(inputLimitChar)
        
    # 0: title, 1: index, 2: checkboxLength, 3: entry, 4: checkboxValue, 5: inputLimitChar
    checkbox_dict = {}
    input_dict = {}
    for i in range(len(googleEntry)):
        # 필수 체크박스이고 체크박스가 한개인 경우
        if googleEntry[i][1] == 4 and googleEntry[i][2] == 1:
            checkbox_dict[googleEntry[i][3]] = googleEntry[i][4]
        # input인 경우
        if googleEntry[i][1] == 0:
            if '성함' in googleEntry[i][0] or '이름' in googleEntry[i][0]:
                input_dict[googleEntry[i][3]] = '이재백'
            if '연락처' in googleEntry[i][0] or '전화번호' in googleEntry[i][0] or '휴대폰' in googleEntry[i][0] or '핸드폰' in googleEntry[i][0]:
                if '11' in googleEntry[i][5]:
                    input_dict[googleEntry[i][3]] = '01023956787'
                else:
                    input_dict[googleEntry[i][3]] = '010-2395-6787'
            if '생년월일' in googleEntry[i][0] or '생일' in googleEntry[i][0]:
                if '6' in googleEntry[i][5]:
                    input_dict[googleEntry[i][3]] = '961016'
                else:
                    input_dict[googleEntry[i][3]] = '19961016'
            if '아이디' in googleEntry[i][0] or 'ID' in googleEntry[i][0] or 'id' in googleEntry[i][0]:
                input_dict[googleEntry[i][3]] = 'dbswlrla112@naver.com'
    for index, (entry,value) in enumerate(checkbox_dict.items()):
        if index == 0:
            url = url + '?' + 'entry.' + str(entry) + '=' + value
        else:
            url = url + '&' + 'entry.' + str(entry) + '=' + value
    for entry,value in input_dict.items():
        url = url + '&' + 'entry.' + str(entry) + '=' + value
    print(url)    
    return url

def sendmail(request):
    send_mail('안녕하세요. AlphaRaffle입니다.',
              '안녕하세요. 자동메시지입니다.\n\nHave a Nice Day~!',
              'dbswlrla1112@gmail.com',
              ['dbswlrla112@gmail.com'],
              fail_silently=False)

    return redirect('/auth/practice')
    