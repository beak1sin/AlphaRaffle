from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import auth
from urllib.parse import quote
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
# import os, sys

import os

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        print(path.dirname( path.dirname( path.abspath(__file__) ) ))
        sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ))

        from django.core.wsgi import get_wsgi_application

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AlphaRaffle.settings')
        application = get_wsgi_application()
        from draw.models import Shoe, Member, Shoeimg, Shoesite, Shoesiteimg, VerificationCode

    else:

        from ..draw.models import Shoe, Member, Shoeimg, Shoesite, Shoesiteimg, VerificationCode

from draw.models import Shoe, Member, Shoeimg, Shoesite, Shoesiteimg, VerificationCode

# a = sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# from ..draw.models import Shoe, Member, Shoeimg, Shoesite, Shoesiteimg

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
from django.core.mail import send_mail

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils import timezone

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
from bs4 import BeautifulSoup
import time
import re
import random
import shutil
import json
import requests
import datetime

def hello():
    now = datetime.datetime.now()
    print(now)
    return

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
    shoename = soup.select("h1.page_title")[0].text.replace('/', '_')
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
            serialno = detail_info_find[5:].replace('/', '_')
        if '발매일' in detail_info_find:
            shoepubdate = detail_info_find[3:]
        if '발매가' in detail_info_find or '가격' in detail_info_find:
            shoeprice = detail_info_find[3:]
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

    try:
        Shoe.objects.create(shoename = shoename , shoeengname = subname, serialno = serialno,
                        shoebrand = shoebrand, pubdate = shoepubdate, shoedetail = product_detail, shoeprice = shoeprice)
    except Exception as e:
        print(f"An error occurred: {e}")
        print(no,'already exist shoe')
        pass
    
    # shoeDB = Shoe.objects.filter(serialno = serialno)
    # shoeDB.update(shoename = shoename , shoeengname = subname,
    #                 shoebrand = shoebrand, pubdate = shoepubdate, shoedetail = product_detail, shoeprice = shoeprice)
    
    if len(imglen)>=1:            
        for i in range(len(imglen)):
            img_file = imglen[i].img['src']
            img_name = os.path.join(str(Path(__file__).resolve().parent.parent)+"/draw/static/draw/images/"+shoename+serialno+str(i)+'.jpeg')
            
            try:
                Shoeimg.objects.create(serialno= serialno, shoeimg = shoename+serialno+str(i))
            except:
                pass
            
            urllib.request.urlretrieve(img_file, img_name)
    else:
        
        img2 = soup.select("div.img_div")
        img_file = img2[0].img['src']
        img_name = os.path.join(str(Path(__file__).resolve().parent.parent)+"/draw/static/draw/images/"+shoename+serialno+str(0)+'.jpeg')
        
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
        logo_name = str(Path(__file__).resolve().parent.parent)+"/draw/static/draw/logoimg/"+sitename+'.jpeg'
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
        # if "docs.google.com" in sitelink:
        #     nameentry, birthentry, phoneentry, nikeidentry = entrycrawl(sitelink)
        # if 'luck-d' in sitelink:
        #     response = requests.get(sitelink)
        #     html = response.text
        #     soup = BeautifulSoup(html,'html.parser')
        #     matched = re.search(r'let link = decodeURIComponent\(\'(.*?)\'\);', html, re.S)
        #     sitelink = matched.group(1)

        shoeunique = serialno+sitename+sitelink

        try:
            Shoesite.objects.create(serialno = serialno , sitename = sitename, sitelink = sitelink, shoesiteunique = shoeunique)
            # Shoesite.objects.create()
        except:
            pass
        # print(sitename, logo_file, sitelink)

        # #종료일
        end_date = soup.select('li.release_time > label > span')[i].text.strip()

        # 종료일이 미정일 경우
        if '미정' in end_date:
            end_date = '2023-12-31 12:59:59'
            end_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
            Shoesite.objects.filter(shoesiteunique = shoeunique).update(end_date = end_date_datetime)
            return

        # #시간이 종료일 경우
        if '종료' in end_date:
            end_date = str(datetime.datetime.now().replace(microsecond=0))
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

def entrycrawl(url):
    # url = 'https://docs.google.com/forms/d/e/1FAIpQLSeD5cUf-XH9Q5lxF3_EQurNnnXNolM-oARjVxnW7XP2QVx9sA/viewform'
    # url = 'https://docs.google.com/forms/d/e/1FAIpQLSc_RlwPQjfqI7DRfEf9CFzNTQbI6pmqOkI26FfJ5kvj7V6A5g/viewform'
    # url = 'https://docs.google.com/forms/d/e/1FAIpQLSc_RlwPQjfqI7DRfEf9CFzNTQbI6pmqOkI26FfJ5kvj7V6A5g/formResponse'
    
    html = requests.get(url).text
    soup = BeautifulSoup(html,'html.parser')
    matched = re.search(r'var FB_PUBLIC_LOAD_DATA_ = (.*);', html, re.S)
    # print('------------------------')
    # print(matched)
    if matched == None:
        return None, None, None, None
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
    #return nameentry,phoneentry,birthentry,nikeidentry
# entrycrawl('127.0.0.1:8080/google_temp')

import subprocess

def crawl():
    telegram_crawl = Telegram_crawl()
    try:
        url = 'https://www.luck-d.com/'
        html = requests.get(url).text
        soup = BeautifulSoup(html,'html.parser')
        time.sleep(0.01)
        shoenum = []
        
        sitecard = soup.select('div.product_info_layer > div.product_thumb')

        for i in range(len(sitecard)):    
            link = sitecard[i].attrs['onclick']
            shoenum.append(link[39:].split('/')[0].replace("'",""))
        
        shoenum = sorted(list(set(shoenum)), reverse=True)
        print(len(shoenum),shoenum)

        for num in shoenum:
            now = datetime.datetime.now()
            print(now)
            randomTime = random.randint(30, 60)
            luckd_crowler(int(num))
            # time.sleep(randomTime)

        # 크롤링 성공 메세지(텔레그램)
        telegram_crawl.crawl_complete_msg()
        
        try:
            # uwsgi 재실행 등.. 서버 재배포
            subprocess.call(['/usr/local/share/AlphaRaffle/bin/start.sh'])
            # 서버 재배포 성공 메세지(텔레그램)
            # telegram_crawl.serverRestart_complete_msg()
            print('서버 재배포 성공')
        except:
            # 서버 재배포 실패 메세지(텔레그램)
            # telegram_crawl.serverRestart_error_msg()
            print('서버 재배포 실패')
        return redirect('/')
    except Exception as e:
        print(f"An error occurred: {e}")
        print('에러로 인한 크롤링 중단')
        telegram_crawl.crawl_error_msg(e)
        raise

import telegram
import asyncio

class Telegram_crawl:
    token = os.environ.get('telegram_token')
    bot = telegram.Bot(token=token)
    chat_id = os.environ.get('telegram_chat_id')

    def crawl_complete_msg(self):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, '크롤링 성공'))
        except Exception as e:
            print('텔레그램 오류')
            print(f"An error occurred: {e}")
        return
    
    def crawl_error_msg(self, error):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, f'크롤링 실패:  {error}'))
        except Exception as e:
            print('텔레그램 오류')
            print(f"An error occurred: {e}")
        return

    def serverRestart_complete_msg(self):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, '서버 재배포 성공'))
        except Exception as e:
            print('서버 재배포 오류')
            print(f"An error occurred: {e}")
        return

    def serverRestart_error_msg(self):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, '서버 재배포 실패'))
        except Exception as e:
            print('서버 재배포 실패 오류')
            print(f"An error occurred: {e}")
        return
    
    def daily_verificationCode_delete(self):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, '만료된 인증번호 삭제완료'))
        except Exception as e:
            print('텔레그램 만료 인증번호 삭제 메세지 전송 실패')
            print(f"An error occurred: {e}")
        return

def crawl_test():
    try:
        url = 'https://www.luck-d.com/'
        html = requests.get(url).text
        soup = BeautifulSoup(html,'html.parser')
        time.sleep(0.01)
        shoenum = []
        
        sitecard = soup.select('div.product_info_layer > div.product_thumb')

        for i in range(len(sitecard)):    
            link = sitecard[i].attrs['onclick']
            shoenum.append(link[39:].split('/')[0].replace("'",""))
        
        shoenum = sorted(list(set(shoenum)), reverse=True)
        print(len(shoenum),shoenum)

        for num in shoenum:
            now = datetime.datetime.now()
            print(now)
            randomTime = random.randint(30, 60)
            # luckd_crowler(int(num))
            luckd_crowler_test(int(num))
            # time.sleep(randomTime)
        return redirect('/')
    except Exception as e:
        print(f"An error occurred: {e}")
        print('에러로 인한 크롤링 중단')
        raise


def luckd_crowler_test(no):
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
        if '발매가' in detail_info_find or '가격' in detail_info_find:
            shoeprice = detail_info_find[3:]
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

    # try:
    #     Shoe.objects.create(shoename = shoename , shoeengname = subname, serialno = serialno,
    #                     shoebrand = shoebrand, pubdate = shoepubdate, shoedetail = product_detail, shoeprice = shoeprice)
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    #     print(no,'already exist shoe')
    #     pass
    
    # shoeDB = Shoe.objects.filter(serialno = serialno)
    # shoeDB.update(shoename = shoename , shoeengname = subname,
    #                 shoebrand = shoebrand, pubdate = shoepubdate, shoedetail = product_detail, shoeprice = shoeprice)
    
    if len(imglen)>=1:            
        for i in range(len(imglen)):
            img_file = imglen[i].img['src']
            img_name = os.path.join(str(Path(__file__).resolve().parent.parent)+"/draw/static/draw/images/"+shoename+serialno+str(i)+'.jpeg')
            
            # try:
            #     Shoeimg.objects.create(serialno= serialno, shoeimg = shoename+serialno+str(i))
            # except:
            #     pass
            
            # urllib.request.urlretrieve(img_file, img_name)
    else:
        
        img2 = soup.select("div.img_div")
        img_file = img2[0].img['src']
        img_name = os.path.join(str(Path(__file__).resolve().parent.parent)+"/draw/static/draw/images/"+shoename+serialno+str(0)+'.jpeg')
        
        # try:
        #     Shoeimg.objects.create(serialno= serialno, shoeimg = shoename+serialno+str(0))
        # except:
        #     pass
        
        # urllib.request.urlretrieve(img_file, img_name)
    
    
    #사이트별 
    sitecard = soup.select('div.release_card')    

    for i in range(len(sitecard)):
        #사이트명
        sitename = soup.select('div.release_card_header > span')[i].text
        #로고
        logo_file = sitecard[i].img['src']
        logo_name = str(Path(__file__).resolve().parent.parent)+"/draw/static/draw/logoimg/"+sitename+'.jpeg'
        #print(logo_file,logo_name)

        # try:
        #     Shoesiteimg.objects.create(sitename = sitename)
        # except:
        #     print('Shoesiteimg already exist or error')
        #     pass
        leng = len('https://static.luck-d.com/agent_site/')

        #print(quote(logo_file[leng:]), logo_name)
        # urllib.request.urlretrieve('https://static.luck-d.com/agent_site/'+quote(logo_file[leng:]), logo_name)
        
        sitelink = sitecard[i].a['href']
        print(sitelink)
        # if 'luck-d' in sitelink:
        #     response = requests.get(sitelink)
        #     html = response.text
        #     soup = BeautifulSoup(html,'html.parser')
        #     matched = re.search(r'let link = decodeURIComponent\(\'(.*?)\'\);', html, re.S)
        #     sitelink = matched.group(1)

        shoeunique = serialno+sitename+sitelink

        # try:
        #     Shoesite.objects.create(serialno = serialno , sitename = sitename, sitelink = sitelink, shoesiteunique = shoeunique)
        #     # Shoesite.objects.create()
        # except:
        #     pass
        # print(sitename, logo_file, sitelink)

        # #종료일
        end_date = soup.select('li.release_time > label > span')[i].text.strip()

        # 종료일이 미정일 경우
        if '미정' in end_date:
            end_date = '2023-12-31 12:59:59'
            end_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
            # Shoesite.objects.filter(shoesiteunique = shoeunique).update(end_date = end_date_datetime)
            return

        # #시간이 종료일 경우
        if '종료' in end_date:
            end_date = str(datetime.datetime.now().replace(microsecond=0))
            end_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
            # Shoesite.objects.filter(shoesiteunique = shoeunique).update(end_date = end_date_datetime)
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
                    
                # Shoesite.objects.filter(shoesiteunique = shoeunique).update(end_date = end_date_datetime)
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
                # Shoesite.objects.filter(shoesiteunique = shoeunique).update(pub_date = pub_date_datetime)

def crawl2(request):
    telegram_crawl = Telegram_crawl()
    try:
        url = 'https://www.luck-d.com/'
        html = requests.get(url).text
        soup = BeautifulSoup(html,'html.parser')
        time.sleep(0.01)
        shoenum = []
        
        sitecard = soup.select('div.product_info_layer > div.product_thumb')

        for i in range(len(sitecard)):    
            link = sitecard[i].attrs['onclick']
            shoenum.append(link[39:].split('/')[0].replace("'",""))
        
        shoenum = sorted(list(set(shoenum)), reverse=True)
        print(len(shoenum),shoenum)
        for num in shoenum:
            now = datetime.datetime.now()
            print(now)
            randomTime = random.randint(30, 60)
            luckd_crowler(int(num))
            # time.sleep(randomTime)

        # 크롤링 성공 메세지(텔레그램)
        telegram_crawl.crawl_complete_msg()
        
        try:
            # uwsgi 재실행 등.. 서버 재배포
            subprocess.call(['/usr/local/share/AlphaRaffle/bin/start.sh'])
            # 서버 재배포 성공 메세지(텔레그램)
            print('서버 재배포 성공')
            # telegram_crawl.serverRestart_complete_msg()
        except:
            # 서버 재배포 실패 메세지(텔레그램)
            # telegram_crawl.serverRestart_error_msg()
            print('서버 재배포 실패')
        return redirect('/')
    except Exception as e:
        print(f"An error occurred: {e}")
        print('에러로 인한 크롤링 중단')
        telegram_crawl.crawl_error_msg()
        raise


def daily_verification_delete_crontab():
    telegram_crawl = Telegram_crawl()
    try:
        verificationCode = VerificationCode.objects.filter(expiry_time__lte = datetime.datetime.now()).delete()
    except Exception as e:
        print(f'An error occurred: {e}')

    telegram_crawl.daily_verificationCode_delete()