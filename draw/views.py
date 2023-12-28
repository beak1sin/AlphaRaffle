from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import auth
from urllib.parse import quote
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from draw.models import Shoe, Member, Shoeimg, Shoesite, Shoesiteimg, Comment, SearchTerm, VerificationCode, Banner, DeletionReason, Rating
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

from django.conf import settings

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

    if Member.objects.filter(member_id=memberid).exists():
        context['flag'] = '1'
        context['result_msg'] = '이미 존재하는 아이디입니다.'
    else:
        context['flag'] = '0'
        context['result_msg'] = '사용 가능한 아이디 입니다.'

    return JsonResponse(context, content_type="application/json")

@csrf_protect
def member_nicknamecheck(request):
    context = {}

    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    membernickname = bodyjson['member_nickname']

    if Member.objects.filter(member_nickname=membernickname).exists():
        context['flag'] = '1'
        context['result_msg'] = '이미 존재하는 닉네임입니다.'
    else:
        context['flag'] = '0'
        context['result_msg'] = '사용 가능한 닉네임 입니다.'

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

    if Member.objects.filter(Q(member_id=memberid) | Q(member_nickname=membernickname)).exists():
        context['flag'] = '1'
        context['result_msg'] = '이미 존재하는 회원이거나 중복된 닉네임입니다..'
    else:
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
        send_mail(
            mail_subject,
            "-",
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            html_message=message,
        )
        context['flag'] = '0'
        context['result_msg'] = '사용 가능한 회원 입니다.'
    return JsonResponse(context, content_type="application/json")

# 메일 인증
@csrf_protect
def resend_mail(request):
    bodydata = request.body.decode('utf-8')
    context = {}
    bodyjson = json.loads(bodydata)
    memberid = bodyjson['member_id']
    rs = Member.objects.get(member_id=memberid)
    if rs:
        current_site = get_current_site(request)
        message = render_to_string('draw/user_activate_email.html',                         {
                    'user': rs,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(rs.pk)).encode().decode(),
                    'token': account_activation_token.make_token(rs),
                })
        mail_subject = "[AlphaRaffle] 회원가입 재인증 메일입니다."
        user_email = rs.member_id
        send_mail(
                mail_subject,
                "-",
                settings.DEFAULT_FROM_EMAIL,
                [user_email],
                html_message=message,
            )
        context['flag'] = '1'
        context['result_msg'] = '회원가입 재인증메일을 보냈습니다. 인증 후 로그인 바랍니다.'
    else:
        context['flag'] = '0'
        context['result_msg'] = '존재하지 않는 이메일입니다.'
    
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

@csrf_protect
def home(request):
    # shoe = Shoe.objects.all()[0:12]
    # shoe = Shoe.objects.all().order_by('-id')[0:12]
    member = None
    member_no = None
    recent_searches = None

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
        recent_searches = SearchTerm.objects.filter(member_no=member_no).order_by('-created_at')[:10]
    
    context = {'member': member, 'droppedShoe': droppedShoe, 'endShoe': endShoe, 'upcomingShoe': upcomingShoe ,'endShoe_count': endShoe_count, 'recent_searches': recent_searches}  # member 객체를 context에 추가

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

    banner = Banner.objects.filter().order_by('-id')
    context['banner'] = banner

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
        return redirect('/')
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
                context['result_msg'] = '비활성화 되어 있습니다. 이메일 인증 후 로그인 바랍니다.'
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
    
        # 로그인 상태에서 비밀번호 변경
        if request.GET.get('autoClick') == 'true':
            return render(request, 'draw/login.html', context)
        else:
            return redirect('/')

    else:
        member_no = None
        member = None
        return render(request, 'draw/login.html', context)

@csrf_protect
def join(request):
    return render(request, 'draw/join.html')

@csrf_protect
def auth_forgot_id(request):
    context = {}

    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    memberid = bodyjson['member_id']

    rs = Member.objects.filter(member_id=memberid)

    if (len(rs)) > 0:
        rs = Member.objects.get(member_id=memberid)
        auth = VerificationCode.objects.filter(member_id=rs.member_id)
        if len(auth) > 0:
            auth.delete()
            context['flag'] = '1'
            context['result_msg'] = '인증번호를 전송하였습니다.'
        else:
            context['flag'] = '1'
            context['result_msg'] = '인증번호를 전송하였습니다.'
        code = str(random.randint(100000, 999999))
        expiry_time = datetime.datetime.now() + timedelta(minutes=5)
        VerificationCode.objects.create(member_id=rs.member_id, code=code, expiry_time=expiry_time)
        message = render_to_string('draw/verification_email.html',                         {
                    'verification_code': code
                })
        mail_subject = "[AlphaRaffle] 인증번호 6자리입니다."
        user_email = rs.member_id
        # email = EmailMessage(mail_subject, message, to=[user_email])
        # email.send()
        send_mail(
            mail_subject,
            "-",
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            html_message=message,
        )
    else:
        context['flag'] = '0'
        context['result_msg'] = '존재하지 않는 이메일입니다.'

    return JsonResponse(context, content_type="application/json")

@csrf_protect
def verification(request):
    context = {}

    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    code = bodyjson['code']

    auth = VerificationCode.objects.filter(code=code, expiry_time__gte=datetime.datetime.now())

    if (len(auth)) > 0:
        context['flag'] = '1'
        context['result_msg'] = '인증이 완료되었습니다.'
    else:
        context['flag'] = '0'
        context['result_msg'] = '인증실패했습니다.'

    return JsonResponse(context, content_type="application/json")


@csrf_protect
def new_password(request):
    context = {}

    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    memberid = bodyjson['memberid']
    pwdencryted = bodyjson['pwdencrypted']
    try:
        member = Member.objects.get(member_id=memberid)
    except:
        return JsonResponse(context, content_type="application/json")

    if member:
        member.member_pwd = pwdencryted
        member.save()
        context['flag'] = '1'
        context['result_msg'] = '비밀번호가 변경되었습니다.'
    else:
        context['flag'] = '0'
        context['result_msg'] = '회원정보가 없습니다.'


    return JsonResponse(context, content_type="application/json")

@csrf_protect
def myPage(request):

    context = {}
    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk=member_no)
        recent_searches = SearchTerm.objects.filter(member_no=member_no).order_by('-created_at')[:10]

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

        comment = Comment.objects.filter(member_nickname=member.member_nickname)
        comment_count = comment.count()
        for com in comment:
            com.shoename = Shoe.objects.get(serialno=com.serialno).shoename

        context = {'member':member ,'liked_shoes':liked_shoes, 'comment': comment, 'comment_count': comment_count, 'recent_searches': recent_searches}
        return render(request, "draw/myPage.html", context)

    else:
        return redirect('/auth/login/')

# 새로운 회원정보수정 방식
@csrf_protect
def member_update(request):
    context = {}

    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)

    memberrealname = bodyjson['realnameAJAX']
    memberbirth = bodyjson['birthAJAX']
    membernikeid = bodyjson['nikeidAJAX']
    memberphonenumber = bodyjson['phonenumberAJAX']

    if 'member_no' in request.session:
        memberno = request.session['member_no']
        isMem = Member.objects.filter(member_no=memberno, member_realname=memberrealname, member_birth=memberbirth, member_nikeid=membernikeid, member_phonenumber=memberphonenumber)
        if isMem:
            context['flag'] = '0'
            context['result_msg'] = '수정된 사항이 없습니다.'
            return JsonResponse(context, content_type="application/json")
        else:
            rsMember = Member.objects.get(member_no=memberno)

            rsMember.member_realname = memberrealname
            rsMember.member_birth = memberbirth
            rsMember.member_nikeid = membernikeid
            rsMember.member_phonenumber = memberphonenumber
            rsMember.save()
            
            context = {'memberrealname': memberrealname, 'memberbirth': memberbirth, 'membernikeid': membernikeid, 'memberphonenumber': memberphonenumber}
            context['flag'] = '1'
            context['result_msg'] = '정보 변경되었습니다'
    else:
        context['flag'] = '0'
        context['result_msg'] = '회원 정보가 없습니다.'

    return JsonResponse(context, content_type="application/json")

# mypage 닉네임 중복확인
@csrf_protect
def nickname_duplicate(request):
    context = {}

    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)

    membernickname = bodyjson['nicknameAJAX'] 

    if 'member_no' in request.session:
        if Member.objects.filter(member_nickname=membernickname).exists():
            context['flag'] = '0'
            context['result_msg'] = '중복된 닉네임입니다.'
        else:
            context['flag'] = '1'
            context['result_msg'] = '사용 가능한 닉네임입니다.'
    else:
        context['flag'] = '0'
        context['result_msg'] = '회원 정보가 없습니다.'

    return JsonResponse(context, content_type="application/json")

# mypage 닉네임 수정
@csrf_protect
def nickname_save(request):
    context = {}

    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)

    membernickname = bodyjson['nicknameAJAX'] 

    if 'member_no' in request.session:
        memberno = request.session['member_no']
        if Member.objects.filter(member_nickname=membernickname).exists():
            context['flag'] = '0'
            context['result_msg'] = '중복된 닉네임입니다.'
        else:
            Member.objects.filter(member_no=memberno).update(member_nickname=membernickname)
            context['new_nickname'] = membernickname
            context['flag'] = '1'
            context['result_msg'] = '닉네임을 변경하였습니다.'
    else:
        context['flag'] = '0'
        context['result_msg'] = '회원 정보가 없습니다.'

    return JsonResponse(context, content_type="application/json")
    
import oci
import environ
import magic

@csrf_protect
def upload(request):
    context = {}
    if request.method == 'POST':
        if request.session.has_key('member_no'):
            member_no = request.session['member_no']
            member = Member.objects.get(pk= member_no)
            member_nickname = member.member_nickname

            try:
                file = request.FILES['file']
            except Exception as e:
                return
                # context['message'] = e
                # return JsonResponse(context, content_type="application/json")
            file_name = file.name

            mime = magic.from_buffer(file.read(), mime=True)
            file.seek(0)  # 파일 포인터를 초기 위치로 되돌립니다.
            allowed_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/avif']
            if mime not in allowed_mime_types:
                context['flag'] = '0'
                context['message'] = '* 허용되지 않는 파일 확장자입니다.'
                return JsonResponse(context, content_type="application/json")
            if file.size > 200 * 1024:
                file, file_name = compress_to_limit(file)
                # context['flag'] = '0'
                # context['message'] = '* 파일 크기가 1MB를 넘습니다.'
                # return JsonResponse(context, content_type="application/json")

            BASE_DIR = Path(__file__).resolve().parent.parent
            environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))

            ORACLE_TENANCY = os.environ.get('ORACLE_TENANCY')
            ORACLE_REGION = os.environ.get('ORACLE_REGION')
            ORACLE_OBJECT_MANAGER_DELETE_READ_OCID = os.environ.get('ORACLE_OBJECT_MANAGER_DELETE_READ_OCID')
            ORACLE_OBJECT_MANAGER_DELETE_READ_KEY_FILE = os.environ.get('ORACLE_OBJECT_MANAGER_DELETE_READ_KEY_FILE')
            ORACLE_OBJECT_MANAGER_DELETE_READ_FINGERPRINT = os.environ.get('ORACLE_OBJECT_MANAGER_DELETE_READ_FINGERPRINT')
            config = {
                "user": ORACLE_OBJECT_MANAGER_DELETE_READ_OCID, # YOUR_USER_OCID
                "key_file": ORACLE_OBJECT_MANAGER_DELETE_READ_KEY_FILE, # PATH_TO_YOUR_PRIVATE_KEY
                "fingerprint": ORACLE_OBJECT_MANAGER_DELETE_READ_FINGERPRINT, # YOUR_FINGERPRINT
                "tenancy": ORACLE_TENANCY, # YOUR_TENANCY_OCID
                "region": ORACLE_REGION, # YOUR_REGION
                "compartment_id": ORACLE_TENANCY # YOUR_COMPARTMENT_OCID
            }

            object_storage = oci.object_storage.ObjectStorageClient(config)
            namespace = object_storage.get_namespace().data

            bucket_name = "shoeneakers-storage"
            object_prefix = 'profiles/' + member_nickname + '-'

            list_objects_response = object_storage.list_objects(namespace, bucket_name, prefix=object_prefix)
            if list_objects_response.data.objects:  # 기존에 프로필 사진 파일 여부 검사
                for obj in list_objects_response.data.objects:
                    object_storage.delete_object(namespace, bucket_name, obj.name)
            
            object_name = object_prefix + file_name
            object_storage.put_object(namespace, bucket_name, object_name, file) 
            
            image_url = f"https://objectstorage.{config['region']}.oraclecloud.com/n/{namespace}/b/{bucket_name}/o/{object_name}"

            Member.objects.filter(pk= member_no).update(profile_img_url=image_url)
            context['flag'] = '1'
            context["message"] = "File uploaded successfully!"
            context["image_url"] = image_url
        else:
            member_no = None
            member = None

        return JsonResponse(context)
    context["message"] = "Invalid request method."
    return JsonResponse(context)

from PIL import Image, ExifTags
import io

def compress_to_limit(file, max_size_kb=200, step=10):
    image = Image.open(file)
    image = correct_image_orientation(image)

    if image.mode == 'RGBA':
        image = image.convert('RGB')

    quality = 90
    file_bytes = None

    while quality > 10:
        output = io.BytesIO()
        image.save(output, format="JPEG", quality=quality)
        file_size_kb = len(output.getvalue()) / 1024

        if file_size_kb <= max_size_kb:
            file_bytes = output.getvalue()
            break

        quality -= step

    if not file_bytes:
        # Reduce image dimensions if quality reduction alone doesn't help
        ratio = max_size_kb / file_size_kb
        new_width = int(image.width * ratio**0.5)
        new_height = int(image.height * ratio**0.5)
        
        image = image.resize((new_width, new_height))
        output = io.BytesIO()
        image.save(output, format="JPEG", quality=quality)
        file_bytes = output.getvalue()

    return io.BytesIO(file_bytes), file.name

def correct_image_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = image._getexif()
        if exif is not None and orientation in exif:
            if exif[orientation] == 2:
                image = image.transpose(Image.FLIP_LEFT_RIGHT)
            elif exif[orientation] == 3:
                image = image.rotate(180)
            elif exif[orientation] == 4:
                image = image.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif exif[orientation] == 5:
                image = image.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif exif[orientation] == 6:
                image = image.rotate(-90, expand=True)
            elif exif[orientation] == 7:
                image = image.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)
        return image
    except (AttributeError, KeyError, IndexError):
        # In case of issues with the image's Exif data
        return image

@csrf_protect
def comment_delete_mypage(request):
    context = {}
    if request.method == 'POST':
        if request.session.has_key('member_no'):
            data = json.loads(request.body)
            pk = data.get('pk')
            comment = data.get('comment')
            created_date = data.get('created_date')
            shoename = data.get('shoename')

            member_no = request.session['member_no']
            member = Member.objects.get(pk= member_no)
            member_nickname = member.member_nickname

            serialno = Shoe.objects.get(shoename=shoename).serialno

            Comment.objects.filter(id=pk, comment=comment, member_nickname=member_nickname, serialno=serialno).delete()

            context["message"] = "댓글 삭제 완료!"

    return JsonResponse(context)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
@csrf_protect
def details(request):
    pk = request.GET['serialnum'].replace(' ','')

    context = {}

    shoe = get_object_or_404(Shoe, serialno=pk) 
    #site = Shoesite.objects.filter(Q(serialno=pk)&Q(Published_date__gte=start_date, Published_date__lte=end_date))
    site = Shoesite.objects.filter(serialno=pk)
    notGoogleSite = site.exclude(Q(sitelink__contains='google') | Q(sitelink__contains='offline'))
    googleSite = Shoesite.objects.filter(serialno=pk, sitelink__contains='google')
    offlineSite = Shoesite.objects.filter(serialno=pk, sitelink__contains='offline')
    # print(googleSite)
    # print(type(googleSite))
    googleSiteOnly = {}
    # if googleSite 
    for googleSiteGet in googleSite.values():
        url = googleSiteGet['sitelink']
        # url = googleFormCrawl(url)
        googleSiteGet['sitelink'] = url
        googleSiteOnly = googleSiteGet
    img = Shoeimg.objects.filter(serialno=pk)
    
    shoebrand = shoe.shoebrand.split(' x ')
    if len(shoebrand) > 1:
        shoebrand.append(shoe.shoebrand)

    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk= member_no)
        recent_searches = SearchTerm.objects.filter(member_no=member_no).order_by('-created_at')[:10]
    else:
        member_no = None
        member = None
        recent_searches = None

    # 댓글
    comment = Comment.objects.filter(serialno=pk).order_by('-created_date')
    comment_count = comment.count()
    if comment.values():
        for com in comment:
            com.profile_img_url = Member.objects.get(member_nickname=com.member_nickname).profile_img_url
        paginator = Paginator(comment, 5)
        page = request.GET.get('page')
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            # 페이지가 정수가 아닐 경우 첫 번째 페이지 반환
            comments = paginator.page(1)
        except EmptyPage:
            # 페이지 범위를 벗어난 경우 마지막 페이지 반환
            comments = paginator.page(paginator.num_pages)
        start_page = ((comments.number - 1) // 5) * 5 + 1
        end_page = min(start_page + 4, paginator.num_pages)
        page_numbers = list(range(start_page, end_page + 1))

        # 페이지가 6이상인지 확인 (isPage6 true면 이전페이지 다음페이지 생성)
        if (comment_count / paginator.per_page) >= 6:
            isPage6 = True
            if start_page == 1:
                previous_page = 1
                next_page = 6
            else:
                previous_page = start_page - 5
                next_page = start_page + 5
        else:
            isPage6 = False
            previous_page = None
            next_page = None
    else:
        comments = {'serialno': ''}
        start_page = None
        end_page = None
        page_numbers = None
        previous_page = None
        next_page = None
        isPage6 = None
    
    
    
    
    if '_' in pk:
        serialnoSlash = pk.replace('_', '/')
    else:
        serialnoSlash = None

    if '_' in shoe.shoename:
        shoenameSlash = shoe.shoename.replace('_', '/')
    else:
        shoenameSlash = None

    if '_' in shoe.shoeengname:
        shoeengnameSlash = shoe.shoeengname.replace('_', '/')
    else:
        shoeengnameSlash = None

    
    current_time = datetime.datetime.now()
    context["current_time"] = current_time

    for site in googleSite:
        if site.end_date == None:
            site.is_valid_date = True
        else:
            if site.end_date <= current_time:
                site.is_valid_date = False
            else:
                site.is_valid_date = True

    for site in notGoogleSite:
        if site.end_date == None:
            site.is_valid_date = True
        else:
            if site.end_date <= current_time:
                site.is_valid_date = False
            else:
                site.is_valid_date = True

    for site in offlineSite:
        if site.end_date != None:
            site.is_valid_date = False
        if site.end_date == None and site.pub_date != None:
            # 오프라인 발매 시간에 이틀이 지날때까지는 true
            if site.pub_date + datetime.timedelta(days=5) > current_time:
                site.is_valid_date = True
            else:
                site.is_valid_date = False
    
    # shoebrand가 같은걸로 필터링한 다른 신발
    anotherBrandShoes = Shoe.objects.filter(shoebrand__contains=shoe.shoebrand).exclude(id=shoe.id).order_by('-id')[:10]

    # category가 같은걸로 필터링한 다른 신발
    anotherCategoryShoes = Shoe.objects.filter(category__contains=shoe.category).exclude(id=shoe.id).order_by('-id')[:10]

    # x 콜라보 제품 중에 shoebrand 제외한 나머지 shoebrand list 확인.
    anotherBrandShoesExcludeLast_objects = []
    if len(shoebrand) > 1:
        for brand in shoebrand[:-1]:
            # 첫번째의 값인 anotherBrandShoes를 필터링 시킨 shoe.shoebrand를 제외한 나머지 데이터들 필터링한 다른 신발
            anotherBrandShoesExcludeLast = Shoe.objects.filter(shoebrand__contains=brand).exclude(id=shoe.id).order_by('-id')[:10]
            anotherBrandShoesExcludeLast_objects.append(anotherBrandShoesExcludeLast)
    combined_objects = zip(anotherBrandShoesExcludeLast_objects, shoebrand[:-1])
    context["member_no"] = member_no
    context = {'shoe':shoe, 'member':member, 'site': site, 'img':img, 'shoebrand': shoebrand, 
               'notGoogleSite': notGoogleSite, 'googleSite': googleSite, 'offlineSite': offlineSite, 
               'googleSiteOnly': googleSiteOnly, 'comment': comments, 'comment_count': comment_count, 
               'serialnoSlash': serialnoSlash, 'shoenameSlash': shoenameSlash, 'shoeengnameSlash': shoeengnameSlash, 
               'recent_searches': recent_searches, 'start_page': start_page, 'end_page': end_page, 
               'page_numbers': page_numbers, 'previous_page': previous_page, 'next_page': next_page, 'isPage6': isPage6,
               'anotherBrandShoes': anotherBrandShoes, 'anotherCategoryShoes': anotherCategoryShoes, 
               'combined_objects': combined_objects }

    return render(request, 'draw/details.html', context)

@csrf_protect
class Pagination():
    def go_page(request):
        context = {}

        bodydata = request.body.decode('utf-8')
        bodyjson = json.loads(bodydata)
        pk = bodyjson['serialnoAJAX']
        

        # 댓글
        comment = Comment.objects.filter(serialno=pk).order_by('-created_date')
        comment_count = comment.count()
        if comment.values():
            for com in comment:
                com.profile_img_url = Member.objects.get(member_nickname=com.member_nickname).profile_img_url
            paginator = Paginator(comment, 5)
            page = bodyjson['pageAJAX']
            try:
                comments = paginator.page(page)
            except PageNotAnInteger:
                # 페이지가 정수가 아닐 경우 첫 번째 페이지 반환
                comments = paginator.page(1)
            except EmptyPage:
                # 페이지 범위를 벗어난 경우 마지막 페이지 반환
                comments = paginator.page(paginator.num_pages)
            start_page = ((comments.number - 1) // 5) * 5 + 1
            end_page = min(start_page + 4, paginator.num_pages)
            page_numbers = list(range(start_page, end_page + 1))

            # 페이지가 6이상인지 확인 (isPage6 true면 이전페이지 다음페이지 생성)
            if (comment_count / paginator.per_page) >= 6:
                isPage6 = True
                if start_page == 1:
                    previous_page = 1
                    next_page = 6
                else:
                    previous_page = start_page - 5
                    next_page = start_page + 5
            else:
                isPage6 = False
                previous_page = None
                next_page = None
        else:
            comments = {'serialno': ''}
            start_page = None
            end_page = None
            page_numbers = None
            previous_page = None
            next_page = None
            isPage6 = None

        # profile_img_url를 임의로 추가한거라 json.serialize가 안돼서 리스트화시켜서 append함.
        comments_json = []
        for com in comments:
            created_date = com.created_date
            am_pm = created_date.strftime("%p")
            formatted_date = created_date.strftime("%Y년 %-m월 %-d일 %-I:%M")

            if am_pm == 'AM':
                formatted_date += " 오전"
            else:
                formatted_date += " 오후"

            com_data = {
                "id": com.id,
                "member_nickname": com.member_nickname,
                "created_date": formatted_date,
                "comment": com.comment,
                "profile_img_url": com.profile_img_url,
                # 여기에 Comment 모델의 다른 필드들도 추가할 수 있습니다.
            }
            comments_json.append(com_data)

        # context['comments'] = comments_json_str
        if request.session.has_key('member_no'):
            member_no = request.session['member_no']
            member = Member.objects.get(pk= member_no)
        else:
            member_no = None
            member = None

        context = {'comment': comments_json, 'comment_count': comment_count, 'member_no': member_no, 'start_page': start_page, 'end_page': end_page, 'page_numbers': page_numbers, 'previous_page': previous_page, 'next_page': next_page, 'isPage6': isPage6, 'has_previous': comments.has_previous(), 'has_next': comments.has_next(), 'current_page': comments.number, 'last_page': comments.paginator.num_pages }

        return JsonResponse(context, content_type="application/json")


@csrf_protect
def map(request):
    context = {}
    serialno = request.GET['serialnum']
    sitename = request.GET['sitename']
    if serialno and sitename:
        # 주어진 serialno를 가지며, address가 null이 아닌 Shoesite 객체들을 필터링
        shoesite_queryset = Shoesite.objects.filter(serialno=serialno, address__isnull=False)

        # sitename이 URL 파라미터로 전달된 값을 포함하는 객체를 필터링
        matching_sitename = shoesite_queryset.filter(sitename__icontains=sitename)
        # 위에서 선택한 객체를 제외한 나머지 객체
        other_sites = shoesite_queryset.exclude(sitename__icontains=sitename)

        # 두 쿼리셋을 합침 (먼저 matching_sitename, 그다음 other_sites)
        shoesite_list = list(matching_sitename) + list(other_sites)
        
        # 컨텍스트에 결과 리스트를 추가
        context['shoesite'] = shoesite_list
    else:
        context['error'] = "Serial number or site name is missing."
    return render(request, 'draw/map.html', context)

def get_geocode(request):
    query = request.GET.get('query')
    
    if not query:
        return JsonResponse({'error': 'Query parameter is missing.'}, status=400)
    
    url = f'https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={query}'
    headers = {
        "X-NCP-APIGW-API-KEY-ID": "f7pin7r31a",
        "X-NCP-APIGW-API-KEY": "lULMysuFlNCXBkmF4TjdouyHi8oZEmPR4oCbKpct"
    }
    
    response = requests.get(url, headers=headers)
    
    return JsonResponse(response.json())

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
def comment_delete_details(request):
    context = {}
    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)

    nickname = bodyjson['nicknameAJAX']
    pk = bodyjson['pkAJAX']

    if request.method == 'POST':
        if request.session.has_key('member_no'):
            memberno = request.session['member_no']
            comment_memberno = Member.objects.get(member_nickname=nickname).member_no
            print(type(memberno), type(comment_memberno))
            if memberno == comment_memberno:
                Comment.objects.filter(pk=pk, member_nickname=nickname).delete()
                context['flag'] = '1'
                context['result_msg'] = '댓글 삭제를 완료하였습니다.'
            else:
                context['flag'] = '0'
                context['result_msg'] = '본인 댓글이 아닙니다.'

        else:
            context['flag'] = '0'
            context['result_msg'] = '로그인 후 이용바랍니다.'

    return JsonResponse(context, content_type="application/json")

from functools import reduce
from operator import or_, and_
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

    # 필터링
    if request.method == 'GET' and 'brand' in request.GET:
        brandList = request.GET.get("brand").split(",")
        # q_list = [Q(shoebrand__contains=element) for element in brandList]
        # combined_q = reduce(or_, q_list)
        # shoe = Shoe.objects.filter(combined_q).order_by('-id')[0:12]
        # shoe_count = Shoe.objects.filter(combined_q).count()
        q_list = [Q(shoebrand__contains=element) for element in brandList]
        if 'OTHERS' in brandList:
            q_list = [q for q in q_list if not ('shoebrand__contains', 'OTHERS') in q.children]
            exclude_others = ['NIKE', 'NIKE SB', 'JORDAN', 'ADIDAS', 'ADIDAS ORIGINALS', 'ADIDAS YEEZY', 'NEW BALANCE', 'REEBOK', 'PUMA', 'VANS', 'CONVERSE', 'ASICS']
            others_list = [~Q(shoebrand__contains=element) for element in exclude_others]
            combined_exclude = reduce(and_, others_list)
            q_list.extend([combined_exclude])
            
        combined_q = reduce(or_, q_list)
        shoe = Shoe.objects.filter(combined_q).order_by('-id')[0:12]
        shoe_count = Shoe.objects.filter(combined_q).count()
        # if len(brandList) > 1:
        #     shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-id')[0:12]
        #     shoe_count = Shoe.objects.filter(shoebrand__in = brandList).count()
        # else:
        #     shoe = Shoe.objects.filter(shoebrand__contains=brandList[0]).order_by('-id')[0:12]
        #     shoe_count = Shoe.objects.filter(shoebrand__contains=brandList[0]).count()

    # 정렬
    if request.method == 'GET' and 'sort' in request.GET:
        sort = request.GET.get("sort")
        if 'latest' in sort:
            shoe = Shoe.objects.filter().order_by('-id')[0:12]
        elif 'bookmark' in sort:
            shoe = Shoe.objects.filter().order_by('-shoelikecount')[0:12]
        elif 'views' in sort:
            shoe = Shoe.objects.filter().order_by('-views')[0:12]
        elif 'comments' in sort:
            shoe = Shoe.objects.filter().order_by('-id')[0:12]
        context = {'shoe': shoe}

    # 검색
    if request.method == 'GET' and 'search_term' in request.GET:
        term = request.GET.get("search_term")

        if term != None:
            if term == '':
                shoe = Shoe.objects.all().order_by('-id')[0:12]
                shoe_count = Shoe.objects.all().count()
            else:
                recent = SearchTerm.objects.filter(term=term,member_no=member_no)
                if recent !=None:
                    recent.delete()
                try: 
                    SearchTerm.objects.create(term=term,member_no=member_no)
                except:
                    pass
                shoe = Shoe.objects.filter(Q(Q(shoename__contains = term) | Q(serialno__contains = term)) | Q(serialno__contains = term)).order_by('-id')[0:12]
                shoe_count = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term)).count()
        else:
            shoe = Shoe.objects.all().order_by('-id')[0:12]
            shoe_count = Shoe.objects.all().count()
        # context = {'shoe': shoe, 'member': member, 'shoe_count': shoe_count ,'recent_searches': recent_searches}
    

    # 검색, 정렬 기준
    if request.method == 'GET' and 'search_term' in request.GET and 'sort' in request.GET:
        sort = request.GET.get("sort")
        term = request.GET.get("search_term")
        if 'latest' in sort:
            shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term)).order_by('-id')[0:12]
        elif 'bookmark' in sort:
            shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term)).order_by('-shoelikecount')[0:12]
        elif 'views' in sort:
            shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term)).order_by('-views')[0:12]
        elif 'comments' in sort:
            shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term)).order_by('-id')[0:12]
        shoe_count = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term)).count()
    
    # 필터링, 정렬 기준
    if request.method == 'GET' and 'brand' in request.GET and 'sort' in request.GET:
        brandList = request.GET.get("brand").split(',')
        sort = request.GET.get("sort")
        if 'latest' in sort:
            shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-id')[0:12]
        elif 'bookmark' in sort:
            shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-shoelikecount')[0:12]
        elif 'views' in sort:
            shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-views')[0:12]
        elif 'comments' in sort:
            shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-id')[0:12]
        shoe_count = Shoe.objects.filter(shoebrand__in=brandList).count()

    # 검색, 필터링 기준
    if request.method == 'GET' and 'search_term' in request.GET and 'brand' in request.GET:
        term = request.GET.get("search_term")
        brandList = request.GET.get("brand").split(',')
        if term == '':
            shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-id')[0:12]
            shoe_count = Shoe.objects.filter(shoebrand__in=brandList).count()
        else:
            recent = SearchTerm.objects.filter(term=term,member_no=member_no)
            if recent !=None:
                recent.delete()
            try: 
                SearchTerm.objects.create(term=term,member_no=member_no)
            except:
                pass
            shoe = Shoe.objects.filter(Q(Q(shoename__contains = term) | Q(serialno__contains = term)) | Q(serialno__contains = term), shoebrand__in = brandList).order_by('-id')[0:12]
            shoe_count = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term), shoebrand__in = brandList).count()

    # 검색, 정렬, 필터링 기준
    if request.method == 'GET' and 'search_term' in request.GET and 'sort' in request.GET and 'brand' in request.GET:
        term = request.GET.get("search_term")
        sort = request.GET.get("sort")
        brandList = request.GET.get("brand").split(',')
        if term == '':
            if 'latest' in sort:
                shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-id')[0:12]
            elif 'bookmark' in sort:
                shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-shoelikecount')[0:12]
            elif 'views' in sort:
                shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-views')[0:12]
            elif 'comments' in sort:
                shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-id')[0:12]
            shoe_count = Shoe.objects.filter(shoebrand__in=brandList).count()
        else:
            if 'latest' in sort:
                shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term), shoebrand__in = brandList).order_by('-id')[0:12]
            elif 'bookmark' in sort:
                shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term), shoebrand__in = brandList).order_by('-shoelikecount')[0:12]
            elif 'views' in sort:
                shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term), shoebrand__in = brandList).order_by('-views')[0:12]
            elif 'comments' in sort:
                shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term), shoebrand__in = brandList).order_by('-id')[0:12]
            shoe_count = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term), shoebrand__in = brandList).count()
            
            recent = SearchTerm.objects.filter(term=term,member_no=member_no)
            if recent !=None:
                recent.delete()
            try: 
                SearchTerm.objects.create(term=term,member_no=member_no)
            except:
                pass

    context = {'shoe': shoe, 'member': member, 'shoe_count': shoe_count ,'recent_searches': recent_searches}  # member 객체를 context에 추가

    if request.method == 'POST':
        context2 = {}
        bodydata = request.body.decode('utf-8')
        bodyjson = json.loads(bodydata)
        page = bodyjson['page']
        per_page = 12
        start_index = (page - 1) * per_page
        end_index = start_index + per_page

        shoe = Shoe.objects.all().order_by('-id')[start_index:end_index] 
        shoe_count = Shoe.objects.all().count()

        # 필터링
        try:
            brandList = request.GET.get("brand").split(',')
        except:
            brandList = None
        if brandList != None:
            # if len(brandList) > 1:
            #     shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-id')[start_index:end_index]
            #     shoe_count = Shoe.objects.filter(shoebrand__in=brandList).count()
            # else:
            #     shoe = Shoe.objects.filter(shoebrand__contains=brandList[0]).order_by('-id')[start_index:end_index]
            #     shoe_count = Shoe.objects.filter(shoebrand__contains=brandList[0]).count()
            q_list = [Q(shoebrand__contains=element) for element in brandList]
            if 'OTHERS' in brandList:
                q_list = [q for q in q_list if not ('shoebrand__contains', 'OTHERS') in q.children]
                exclude_others = ['NIKE', 'NIKE SB', 'JORDAN', 'ADIDAS', 'ADIDAS ORIGINALS', 'ADIDAS YEEZY', 'NEW BALANCE', 'REEBOK', 'PUMA', 'VANS', 'CONVERSE', 'ASICS']
                others_list = [~Q(shoebrand__contains=element) for element in exclude_others]
                combined_exclude = reduce(and_, others_list)
                q_list.extend([combined_exclude])
                
            combined_q = reduce(or_, q_list)
            shoe = Shoe.objects.filter(combined_q).order_by('-id')[start_index:end_index]
            shoe_count = Shoe.objects.filter(combined_q).count()

        # 검색
        term = request.GET.get("search_term")
        if term != None:
            shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term)).order_by('-id')[start_index:end_index]
            shoe_count = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term)).count()

        # 정렬 기준
        sort = request.GET.get("sort")
        if sort != None:
            if 'latest' in sort:
                shoe = Shoe.objects.filter().order_by('-id')[start_index:end_index]
            elif 'bookmark' in sort:
                shoe = Shoe.objects.filter().order_by('-shoelikecount')[start_index:end_index]
            elif 'views' in sort:
                shoe = Shoe.objects.filter().order_by('-views')[start_index:end_index]
            elif 'comments' in sort:
                shoe = Shoe.objects.filter().order_by('-id')[start_index:end_index]

        # 검색, 정렬 기준
        if term != None and sort != None:
            if 'latest' in sort:
                shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term)).order_by('-id')[start_index:end_index]
            elif 'bookmark' in sort:
                shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term)).order_by('-shoelikecount')[start_index:end_index]
            elif 'views' in sort:
                shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term)).order_by('-views')[start_index:end_index]
            elif 'comments' in sort:
                shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term)).order_by('-id')[start_index:end_index]
        
        # 필터링, 정렬 기준
        if brandList != None and sort != None:
            if 'latest' in sort:
                shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-id')[start_index:end_index]
            elif 'bookmark' in sort:
                shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-shoelikecount')[start_index:end_index]
            elif 'views' in sort:
                shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-views')[start_index:end_index]
            elif 'comments' in sort:
                shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-id')[start_index:end_index]

        # 검색, 필터링 기준
        if term != None and brandList != None:
            shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term), shoebrand__in = brandList).order_by('-id')[start_index:end_index]
            shoe_count = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term), shoebrand__in = brandList).count()

        # 검색, 정렬, 필터링 기준
        if term != None and sort != None and brandList != None:
            if 'latest' in sort:
                shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term), shoebrand__in=brandList).order_by('-id')[start_index:end_index]
            elif 'bookmark' in sort:
                shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term), shoebrand__in=brandList).order_by('-shoelikecount')[start_index:end_index]
            elif 'views' in sort:
                shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term), shoebrand__in=brandList).order_by('-views')[start_index:end_index]
            elif 'comments' in sort:
                shoe = Shoe.objects.filter(Q(shoename__contains = term) | Q(serialno__contains = term), shoebrand__in=brandList).order_by('-id')[start_index:end_index]

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
    # print('------------------------')
    # print(brandList, regionList, onofflineList, releaseList, deliveryList)
    # for i in range(len(brandList)):
    #     shoe = list(Shoe.objects.filter(shoebrand = brandList[i]).values())
    # print(shoe)
    shoe = Shoe.objects.filter(shoebrand__in=brandList).order_by('-id')
    shoe_count = Shoe.objects.filter(shoebrand__in = brandList).count()
    shoes = serializers.serialize('json', shoe)
    # print(shoes)
    likes = []  # 멤버별 신발 좋아요 여부를 저장할 리스트
    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk=member_no)
        for shoe in shoe:
            likes.append(member in shoe.likes.all())
    context['flag'] = '0'
    context['result_msg'] = '필터링 작업'
    context['shoes'] = shoes
    context['likes'] = likes
    context['shoe_count'] = shoe_count
    return JsonResponse(context, content_type="application/json")

@csrf_protect
def filtering2(request):
    context = {}
    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    
    selectedBrands = bodyjson['selectedBrands']
    q_list = [Q(shoebrand__contains=element) for element in selectedBrands]
    if len(q_list) > 0: 
        if 'OTHERS' in selectedBrands:
            q_list = [q for q in q_list if not ('shoebrand__contains', 'OTHERS') in q.children]
            exclude_others = ['NIKE', 'NIKE SB', 'JORDAN', 'ADIDAS', 'ADIDAS ORIGINALS', 'ADIDAS YEEZY', 'NEW BALANCE', 'REEBOK', 'PUMA', 'VANS', 'CONVERSE', 'ASICS']
            others_list = [~Q(shoebrand__contains=element) for element in exclude_others]
            combined_exclude = reduce(and_, others_list)
            q_list.extend([combined_exclude])
            
        combined_q = reduce(or_, q_list)
        shoe = Shoe.objects.filter(combined_q).order_by('-id')[0:12]
        shoe_count = Shoe.objects.filter(combined_q).count()
    else:
        shoe = Shoe.objects.filter().order_by('-id')[0:12]
        shoe_count = Shoe.objects.filter().count()
    # shoe = Shoe.objects.filter(shoebrand__in=selectedBrands).order_by('-id')[0:12]
    # shoe_count = Shoe.objects.filter(shoebrand__in = selectedBrands).count()
    shoes = serializers.serialize('json', shoe)

    likes = []  # 멤버별 신발 좋아요 여부를 저장할 리스트
    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk=member_no)
        for shoe in shoe:
            likes.append(member in shoe.likes.all())
    context['flag'] = '0'
    context['result_msg'] = '필터링 작업'
    context['shoes'] = shoes
    context['likes'] = likes
    context['shoe_count'] = shoe_count
    return JsonResponse(context, content_type="application/json")  

@csrf_protect
def filtering_order(request):
    context = {}
    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    
    order = bodyjson['orderAJAX']
    print(order)

    if 'latest' in order:
        shoe = Shoe.objects.filter().order_by('-id')[0:12]
    elif 'bookmark' in order:
        shoe = Shoe.objects.filter().order_by('-shoelikecount')[0:12]
    elif 'views' in order:
        shoe = Shoe.objects.filter().order_by('-views')[0:12]
    elif 'comments' in order:
        shoe = Shoe.objects.filter().order_by('-id')[0:12]
    shoes = serializers.serialize('json', shoe)
    likes = []
    if request.session.has_key('member_no'):
        member_no = request.session['member_no']
        member = Member.objects.get(pk=member_no)
        for shoe in shoe:
            likes.append(member in shoe.likes.all())

    context = {'flag': '1', 'shoes': shoes, 'likes': likes}
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
        # post_comment(request)
        context['flag'] = '1'
        context['result_msg'] = '로그인 되어 있는 상태'
    else :
        context['flag'] = '0'
        context['result_msg'] = '로그인 후 이용바랍니다.'

    return JsonResponse(context, content_type="application/json")

@csrf_protect
def delete_recent_searches(request):
    context = {}
    bodydata = request.body.decode('utf-8')
    bodyjson = json.loads(bodydata)
    
    recent_search = bodyjson['recent_searchAJAX']
    member_no = request.session['member_no']
    recent = SearchTerm.objects.filter(term=recent_search,member_no=member_no)
    if recent:
        recent.delete()
        context['result_msg'] = '삭제 완료'
    else:
        context['result_msg'] = '삭제할 검색어가 없습니다.'

    context['flag'] = '1'
    
    print(recent_search)
    return JsonResponse(context, content_type="application/json")

@csrf_protect
def all_recent_delete(request):
    context = {}
    if 'member_no' in request.session:
        member_no = request.session['member_no']
        recent = SearchTerm.objects.filter(member_no=member_no)
        
        if recent:
            recent.delete()
            context['recent'] = '존재유'
            context['result_msg'] = '전체 삭제 완료'
        else:
            context['recent'] = '존재무'
            context['result_msg'] = '삭제할 검색어가 없습니다.'

        context['flag'] = '1'
        
    else :
        context['flag'] = '0'
        context['result_msg'] = '로그인 안되어 있는 상태'

    return JsonResponse(context, content_type="application/json")

def naverSearch(request):
    return render(request, 'draw/naver07438b501f2bcdb23c19460dc9cca09d.html')

def naverSearchwww(request):
    return render(request, 'draw/naver73749ca69b9eff6e2574852408ea3ecf.html')

def practice(request):
    # 연습용
    shoes = Rating.objects.select_related('shoe')
    print(shoes)
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
    
def custom_404(request, exception):
    return render(request, 'draw/errors/404.html', {}, status=404)

def custom_500(request):
    return render(request, 'draw/errors/500.html', status=500)

def googleCrawl(request):
    url = 'https://docs.google.com/forms/d/e/1FAIpQLSe7DmdJZaJUIAtg-78n6VTASTqCd_ueLeG3CzoHoyfALYQIHg/closedform?pli=1'
    
    # url = 'https://docs.google.com/forms/d/e/1FAIpQLSc_RlwPQjfqI7DRfEf9CFzNTQbI6pmqOkI26FfJ5kvj7V6A5g/viewform'
    # url = 'https://docs.google.com/forms/d/e/1FAIpQLSc_RlwPQjfqI7DRfEf9CFzNTQbI6pmqOkI26FfJ5kvj7V6A5g/formResponse'
    # url = 'https://alpharaffle.com/google_temp'
    html = requests.get(url).text

    # jsondata = html.json()
    # FB_PUBLIC_LOAD_DATA_ = jsondata["FB_PUBLIC_LOAD_DATA_"]
    # print(FB_PUBLIC_LOAD_DATA_)
    soup = BeautifulSoup(html,'html.parser')
    matched = re.search(r'var FB_PUBLIC_LOAD_DATA_ = (.*);', html, re.S)
    # print('------------------------')
    # print(matched)
    if matched == None:
        return None, None, None, None
    entryList = matched.group(1)
    # print(entryList)
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
                nameentry = googleEntry[i][3]
            if '연락처' in googleEntry[i][0] or '전화번호' in googleEntry[i][0] or '휴대폰' in googleEntry[i][0] or '핸드폰' in googleEntry[i][0]:
                if '11' in googleEntry[i][5]:
                    phoneentry = [googleEntry[i][3],11]
                else:
                    phoneentry = [googleEntry[i][3],'-']
            if '생년월일' in googleEntry[i][0] or '생일' in googleEntry[i][0]:
                if '6' in googleEntry[i][5]:
                    birthentry = [ googleEntry[i][3], 6 ]
                else:
                    birthentry = [ googleEntry[i][3], 8 ]
            if '아이디' in googleEntry[i][0] or 'ID' in googleEntry[i][0] or 'id' in googleEntry[i][0]:
                nikeidentry = googleEntry[i][3]

    print(nameentry,phoneentry,birthentry,nikeidentry)


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

@csrf_protect
class Mypage():
    def bookmark(request):
        context = {}
        if request.session.has_key('member_no'):
            member_no = request.session['member_no']
            member = Member.objects.get(pk=member_no)
            recent_searches = SearchTerm.objects.filter(member_no=member_no).order_by('-created_at')[:10]

            context['flag'] = "0"
            context['result_msg'] = "Member read..."

            liked_shoes = member.liked_posts.all()

            context = {'member':member ,'liked_shoes':liked_shoes, 'recent_searches': recent_searches}
            return render(request, "draw/myPage/bookmark.html", context)

        else:
            return redirect('/auth/login/')
        
    def draw(request):
        context = {}
        if request.session.has_key('member_no'):
            member_no = request.session['member_no']
            member = Member.objects.get(pk=member_no)
            recent_searches = SearchTerm.objects.filter(member_no=member_no).order_by('-created_at')[:10]

            context['flag'] = "0"
            context['result_msg'] = "Member read..."

            liked_shoes = member.liked_posts.all()

            context = {'member':member ,'liked_shoes':liked_shoes, 'recent_searches': recent_searches}
            return render(request, "draw/myPage/draw.html", context)

        else:
            return redirect('/auth/login/')

    def comment(request):
        context = {}
        if request.session.has_key('member_no'):
            member_no = request.session['member_no']
            member = Member.objects.get(pk=member_no)
            recent_searches = SearchTerm.objects.filter(member_no=member_no).order_by('-created_at')[:10]

            context['flag'] = "0"
            context['result_msg'] = "Member read..."


            comment = Comment.objects.filter(member_nickname=member.member_nickname)
            comment_count = comment.count()
            for com in comment:
                com.shoename = Shoe.objects.get(serialno=com.serialno).shoename

            context = {'member':member , 'comment': comment, 'comment_count': comment_count, 'recent_searches': recent_searches}
            return render(request, "draw/myPage/comment.html", context)

        else:
            return redirect('/auth/login/')
        
    def board(request):
        context = {}
        if request.session.has_key('member_no'):
            member_no = request.session['member_no']
            member = Member.objects.get(pk=member_no)
            recent_searches = SearchTerm.objects.filter(member_no=member_no).order_by('-created_at')[:10]

            context = {'member':member, 'recent_searches': recent_searches}
            return render(request, "draw/myPage/board.html", context)

        else:
            return redirect('/auth/login/')
        
    def review(request):
        context = {}
        if request.session.has_key('member_no'):
            member_no = request.session['member_no']
            member = Member.objects.get(pk=member_no)
            recent_searches = SearchTerm.objects.filter(member_no=member_no).order_by('-created_at')[:10]

            context = {'member':member, 'recent_searches': recent_searches}
            return render(request, "draw/myPage/review.html", context)

        else:
            return redirect('/auth/login/')
        
    def settings(request):
        context = {}
        if request.session.has_key('member_no'):
            member_no = request.session['member_no']
            member = Member.objects.get(pk=member_no)
            recent_searches = SearchTerm.objects.filter(member_no=member_no).order_by('-created_at')[:10]

            context['member_no'] = member.member_no
            context['member_id'] = member.member_id
            context['member_realname'] = member.member_realname
            context['member_nickname'] = member.member_nickname
            context['member_phonenumber'] = member.member_phonenumber
            context['member_nikeid'] = member.member_nikeid
            context['member_birth'] = member.member_birth

            context['flag'] = "0"
            context['result_msg'] = "Member read..."

            context = {'member':member, 'recent_searches': recent_searches}
            return render(request, "draw/myPage/settings.html", context)

        else:
            return redirect('/auth/login/')
        
    def delete(request):
        context = {}
        if request.session.has_key('member_no'):
            member_no = request.session['member_no']
            member = Member.objects.get(pk= member_no)

        else:
            return redirect('/auth/login/')

        context["member_no"] = member_no
        context = {'member':member }
        return render(request, "draw/myPage/delete.html", context)
    
    def password_check(request):
        context = {}
        if request.session.has_key('member_no'):
            bodydata = request.body.decode('utf-8')
            bodyjson = json.loads(bodydata)

            memberpwd = bodyjson['member_pwd']

            memberno = request.session['member_no']
            rsMember = Member.objects.get(member_no=memberno)

            if (rsMember.member_pwd == memberpwd):
                context['flag'] = '1'
                context['result_msg'] = '비밀번호가 일치합니다.'
            else:
                context['flag'] = '0'
                context['result_msg'] = '비밀번호가 일치하지 않습니다.'
            return JsonResponse(context, content_type="application/json")
        else:
            return redirect('/auth/login/')
        
    def member_delete(request):
        context = {}
        if request.session.has_key('member_no'):
            bodydata = request.body.decode('utf-8')
            bodyjson = json.loads(bodydata)

            memberpwd = bodyjson['member_pwd']

            memberno = request.session['member_no']
            rsMember = Member.objects.get(member_no=memberno)

            if (rsMember.member_pwd == memberpwd):
                checkboxList = bodyjson['checkboxList']
                model_instance = DeletionReason()
                for item in checkboxList:
                    if isinstance(item, list) and item[0] == 'others':
                        # '기타' 항목 처리
                        setattr(model_instance, 'others', item[1])
                    elif hasattr(model_instance, item):
                        # 해당 item 이름을 가진 필드가 모델에 존재하는 경우
                        setattr(model_instance, item, True)
                model_instance.save()
                    
                    
                Member.objects.get(member_no=memberno).delete()
                request.session.flush()
                context['flag'] = '1'
                context['result_msg'] = '회원 탈퇴 완료하였습니다.'
            else:
                context['flag'] = '0'
                context['result_msg'] = '비밀번호가 일치하지 않습니다.'
            return JsonResponse(context, content_type="application/json")
        else:
            return redirect('/auth/login/')

        
