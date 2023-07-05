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
        from draw.models import Shoe, Member, Shoeimg, Shoesite, Shoesiteimg

    else:

        from ..draw.models import Shoe, Member, Shoeimg, Shoesite, Shoesiteimg

from draw.models import Shoe, Member, Shoeimg, Shoesite, Shoesiteimg

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
        if 'luck-d' in sitelink:
            response = requests.get(sitelink)
            html = response.text
            soup = BeautifulSoup(html,'html.parser')
            matched = re.search(r'let link = decodeURIComponent\(\'(.*?)\'\);', html, re.S)
            sitelink = matched.group(1)

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

# def crawl():
#     url = 'https://www.luck-d.com/'
#     html = requests.get(url).text
#     soup = BeautifulSoup(html,'html.parser')
#     time.sleep(0.01)
#     shoenum = []
    
#     sitecard = soup.select('div.product_info_layer > div.product_thumb')

#     for i in range(len(sitecard)):    
#         link = sitecard[i].attrs['onclick']
#         shoenum.append(link[39:].split('/')[0])
    
#     shoenum = list(set(shoenum))
#     print(shoenum)

#     for num in shoenum:
#         now = datetime.datetime.now()
#         print(now)
#         randomTime = random.randint(30, 60)
#         luckd_crowler(int(num))
#         time.sleep(randomTime)
        
#     return redirect('/')

def crawl():
    try:
        url = 'https://www.luck-d.com/'
        html = requests.get(url).text
        soup = BeautifulSoup(html,'html.parser')
        time.sleep(0.01)
        shoenum = []
        
        sitecard = soup.select('div.product_info_layer > div.product_thumb')

        for i in range(len(sitecard)):    
            link = sitecard[i].attrs['onclick']
            shoenum.append(link[39:].split('/')[0])
        
        shoenum = sorted(list(set(shoenum)), reverse=True)
        print(len(shoenum),shoenum)

        for num in shoenum:
            now = datetime.datetime.now()
            print(now)
            randomTime = random.randint(30, 60)
            luckd_crowler(int(num))
            # time.sleep(randomTime)
        crawl_complete_msg()
        return redirect('/')
    except Exception as e:
        print(f"An error occurred: {e}")
        print('에러로 인한 크롤링 중단')
        crawl_error_msg()
        raise

import telegram
import asyncio

token = os.environ.get('telegram_token')
bot = telegram.Bot(token=token)
chat_id = os.environ.get('telegram_chat_id')

def crawl_complete_msg():
    try:
        asyncio.run(bot.send_message(chat_id=chat_id, text='크롤링 성공'))
    except Exception as e:
        print('텔레그램 오류')
        print(f"An error occurred: {e}")
    return

def crawl_error_msg():
    try:
        asyncio.run(bot.send_message(chat_id=chat_id, text='크롤링 실패'))
    except Exception as e:
        print('텔레그램 오류')
        print(f"An error occurred: {e}")
    return