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
# jpeg -> avif 변환 
from PIL import Image
import pillow_avif
import unicodedata

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
            serialno = detail_info_find[6:].replace('/', '_').strip()
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

    imgDownload = False
    try:
        Shoe.objects.create(shoename = shoename , shoeengname = subname, serialno = serialno,
                        shoebrand = shoebrand, pubdate = shoepubdate, shoedetail = product_detail, shoeprice = shoeprice, product_no = no)
        imgDownload = True
    except Exception as e:
        print(f"An error occurred {no}: {e}")
        pass
    
    # shoeDB = Shoe.objects.filter(serialno = serialno)
    # shoeDB.update(shoename = shoename , shoeengname = subname,
    #                 shoebrand = shoebrand, pubdate = shoepubdate, shoedetail = product_detail, shoeprice = shoeprice)

    if imgDownload:
        if len(imglen)>=1:            
            for i in range(len(imglen)):
                img_file = imglen[i].img['src']
                temp_img_name = os.path.join(str(Path(__file__).resolve().parent.parent)+"/draw/static/draw/images/"+serialno+str(i)+'.jpeg')
                avif_img_name = os.path.join(str(Path(__file__).resolve().parent.parent)+"/draw/static/draw/images/"+serialno+str(i)+'.avif')
                
                # 이미지를 임시 JPEG 파일로 다운로드
                urllib.request.urlretrieve(img_file, temp_img_name)

                try:
                    # JPEG 파일을 열어 AVIF로 저장
                    with Image.open(temp_img_name) as img:
                        if img.mode == "P":
                            img = img.convert("RGBA")
                        img.save(avif_img_name, "AVIF")

                    # 임시 JPEG 파일 삭제
                    os.remove(temp_img_name)
                except Exception as e:
                    print(f'error: {e}')
                
                try:
                    Shoeimg.objects.create(serialno= serialno, shoeimg = serialno+str(i))
                except:
                    pass
                
                
        else:
            
            img2 = soup.select("div.img_div")
            img_file = img2[0].img['src']
            temp_img_name = os.path.join(str(Path(__file__).resolve().parent.parent)+"/draw/static/draw/images/"+serialno+str(0)+'.jpeg')
            avif_img_name = os.path.join(str(Path(__file__).resolve().parent.parent)+"/draw/static/draw/images/"+serialno+str(0)+'.avif')

            # 이미지를 임시 JPEG 파일로 다운로드
            urllib.request.urlretrieve(img_file, temp_img_name)

            
            try:
                # JPEG 파일을 열어 AVIF로 저장  
                with Image.open(temp_img_name) as img:
                    if img.mode == "P":
                        img = img.convert("RGBA")
                    img.save(avif_img_name, "AVIF")

                # 임시 JPEG 파일 삭제
                os.remove(temp_img_name)
            except Exception as e:
                print(f'error: {e}')
            
            try:
                Shoeimg.objects.create(serialno= serialno, shoeimg = serialno+str(0))
            except:
                pass
        
    
    
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

        shoeunique = serialno+sitename+sitelink

        try:
            Shoesite.objects.create(serialno = serialno , sitename = sitename, sitelink = sitelink, shoesiteunique = shoeunique)
            # Shoesite.objects.create()
        except:
            pass
        # print(sitename, logo_file, sitelink)
        
        if "docs.google.com" in sitelink:
            telegram_crawl = Telegram_crawl()
            # redirct url
            response = requests.get(sitelink, allow_redirects=True)
            sitelink = response.url
            
            if 'closedform' in sitelink:
                pass
            else:
                try:
                    nameentry, phoneentrylen, birthentrylen,  nikeidentry = entrycrawl(sitelink)
                    if birthentrylen is None:
                        birthentry = None
                        birthlen = None
                    else:
                        birthentry = birthentrylen[0]
                        birthlen = birthentrylen[1] # 생년월일 길이

                    if phoneentrylen is None:
                        phoneentry = None
                        phonehyphen = None
                    else:
                        phoneentry = phoneentrylen[0]
                        phonehyphen = phoneentrylen[1] # 폰 하이픈 여부

                    Shoesite.objects.filter(shoesiteunique = shoeunique).update(nameentry = nameentry, birthentry = birthentry, phoneentry = phoneentry, nikeidentry = nikeidentry)
                    telegram_crawl.crawl_entry_msg(nameentry, birthentry, phoneentry, nikeidentry)
                except Exception as e:
                    telegram_crawl.crawl_entry_error_msg(e)
        # if 'luck-d' in sitelink:
        #     response = requests.get(sitelink)
        #     html = response.text
        #     soup = BeautifulSoup(html,'html.parser')
        #     matched = re.search(r'let link = decodeURIComponent\(\'(.*?)\'\);', html, re.S)
        #     sitelink = matched.group(1)

        # #종료일
        end_date = soup.select('li.release_time > label > span')[i].text.strip()

        # 종료일이 미정일 경우
        if '미정' in end_date:
            end_date = '2024-12-31 23:59:59'
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

            # 시간이 발매일 경우
            elif '발매' in end_date:
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
                    end_date = end_date + ":00"
                    pub_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

                Shoesite.objects.filter(shoesiteunique = shoeunique).update(pub_date = pub_date_datetime)

            # 시간이 시작일 경우
            elif '시작' in end_date:
                end_date = end_date.replace("월",'-')
                end_date = end_date.replace(" ",'')
                end_date = end_date.replace("일",' ')
                end_date = end_date.replace("시",'')
                end_date = end_date.replace("작",'')        
                # end_date = end_date + ":59"
                end_date = "".join(end_date)
                end_date = year +'-'+ end_date
                
                if len(end_date) == 11:
                    end_date = end_date.replace(" ",'')
                    pub_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                elif len(end_date) == 16:
                    end_date = end_date + ":00"
                    pub_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
                    
                Shoesite.objects.filter(shoesiteunique = shoeunique).update(pub_date = pub_date_datetime)

        # 오프라인인 경우 주소 추가
        if 'offline' in sitelink:
            # print(sitelink)
            offline_url = 'https://www.luck-d.com' + sitelink
            offline_html = requests.get(offline_url).text
            offline_soup = BeautifulSoup(offline_html,'html.parser')
            time.sleep(0.01)

            address = offline_soup.select('div.agent_site_info > label > .agent_site_info_data')[1].text.strip()
            normalized_address = unicodedata.normalize('NFC', address)

            Shoesite.objects.filter(shoesiteunique = shoeunique).update(address = normalized_address)

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
    nameentry,phoneentry,birthentry,nikeidentry = None, None, None, None
    for i in range(len(googleEntry)):
        # 필수 체크박스이고 체크박스가 한개인 경우
        if googleEntry[i][1] == 4 and googleEntry[i][2] == 1:
            checkbox_dict[googleEntry[i][3]] = googleEntry[i][4]
        # input인 경우
        if googleEntry[i][1] == 0:
            if '성함' in googleEntry[i][0] or '이름' in googleEntry[i][0]:
                nameentry = googleEntry[i][3]
            # else :
            #     nameentry = None
                
            if '연락처' in googleEntry[i][0] or '전화번호' in googleEntry[i][0] or '휴대폰' in googleEntry[i][0] or '핸드폰' in googleEntry[i][0]:

                if googleEntry[i][5] is None:
                    phoneentry = [googleEntry[i][3],11]
                else:
                    if '11' in googleEntry[i][5]:
                        phoneentry = [googleEntry[i][3],11]
                        
                    else:
                        phoneentry = [googleEntry[i][3],'-']
            # else :
            #     phoneentry = None

            if '생년월일' in googleEntry[i][0] or '생일' in googleEntry[i][0]:
                # if googleEntry[i][5] is not None and ('6' in googleEntry[i][5] or '6' in googleEntry[i][0]):
                #     birthentry = [ googleEntry[i][3], 6]
                # elif googleEntry[i][5] is not None and ('8' in googleEntry[i][5] or '8' in googleEntry[i][0]):
                #     birthentry = [ googleEntry[i][3], 8]
                if googleEntry[i][5] is None:
                    if '6' in googleEntry[i][0]:
                        birthentry = [ googleEntry[i][3], 6]
                    elif '8' in googleEntry[i][0]:
                        birthentry = [ googleEntry[i][3], 8]
                else:
                    if '6' in googleEntry[i][5]:
                        birthentry = [ googleEntry[i][3], 6]
                    elif '8' in googleEntry[i][5]:
                        birthentry = [ googleEntry[i][3], 8]
            # else :
            #     birthentry = None

            if '아이디' in googleEntry[i][0] or 'ID' in googleEntry[i][0] or 'id' in googleEntry[i][0]:
                nikeidentry = googleEntry[i][3]
            # else :
            #     nikeidentry = None


    return nameentry,phoneentry,birthentry,nikeidentry

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
            telegram_crawl.serverRestart_complete_msg()
            print('서버 재배포 성공')
        except Exception as e:
            # 서버 재배포 실패 메세지(텔레그램)
            telegram_crawl.serverRestart_error_msg()
            print(f'서버 재배포 실패 : {e}')

        # cloudflare 캐시 삭제
        cloudflareCacheDeleteAPI()
        return
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
            # 코루틴 실행
            # run_in_new_loop(self.bot.send_message(self.chat_id, '크롤링 성공'))
        except Exception as e:
            print('텔레그램 오류')
            print(f"An error occurred: {e}")
        return
    
    def crawl_error_msg(self, error):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, f'크롤링 실패:  {error}'))
            # run_in_new_loop(self.bot.send_message(self.chat_id, f'크롤링 실패:  {error}'))
        except Exception as e:
            print('텔레그램 오류')
            print(f"An error occurred: {e}")
        return

    def serverRestart_complete_msg(self):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, '서버 재배포 성공'))
            # run_in_new_loop(self.bot.send_message(self.chat_id, '서버 재배포 성공'))
        except Exception as e:
            print('서버 재배포 오류')
            print(f"An error occurred: {e}")
        return

    def serverRestart_error_msg(self):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, '서버 재배포 실패'))
            # run_in_new_loop(self.bot.send_message(self.chat_id, '서버 재배포 실패'))
        except Exception as e:
            print('서버 재배포 실패 오류')
            print(f"An error occurred: {e}")
        return
    
    def daily_verificationCode_delete(self):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, '만료된 인증번호 삭제완료'))
            # run_in_new_loop(self.bot.send_message(self.chat_id, '만료된 인증번호 삭제완료'))
        except Exception as e:
            print('텔레그램 만료 인증번호 삭제 메세지 전송 실패')
            print(f"An error occurred: {e}")
        return
    
    def crawl_entry_msg(self, nameentry, birthentry, phoneentry, nikeidentry):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, f'entry 크롤링 성공 = nameentry: {nameentry}, birthentry: {birthentry}, phoneentry: {phoneentry}, nikeidentry: {nikeidentry}'))
            # run_in_new_loop(self.bot.send_message(self.chat_id, f'entry 크롤링 성공 = nameentry: {nameentry}, birthentry: {birthentry}, phoneentry: {phoneentry}, nikeidentry: {nikeidentry}'))
        except Exception as e:
            print('telegram entry 메세지 전송 실패')
            print(f"An error occurred: {e}")
        return
    
    def crawl_entry_error_msg(self, error):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, f'entry 크롤링 실패:  {error}'))
            # run_in_new_loop(self.bot.send_message(self.chat_id, f'entry 크롤링 실패:  {error}'))
        except Exception as e:
            print('텔레그램 오류')
            print(f"An error occurred: {e}")
        return
    
    def mijungCheck_msg(self):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, '종료미정 체크'))
        except Exception as e:
            print('종료미정 체크 실패')
            print(f"An error occurred: {e}")
        return

def run_in_new_loop(coroutine):
    """새로운 이벤트 루프에서 코루틴을 실행하는 도우미 함수"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(coroutine)
        return result
    finally:
        loop.close()

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
        # shoenum = ['8034', '8033', '8032', '8031', '8030', '8029', '8028', '8027', '8026', '8022', '8021', '8020', '8019', '8018', '7988', '7987', '7986', '7985', '7984', '7977', '7974', '7973', '7972', '7971', '7970', '7969', '7949', '7938', '7937', '7926', '7925', '7924', '7894', '774', '7697', '7696', '7687', '7681', '7639', '7574', '7568', '7567', '7506', '7498', '7311', '7303', '7301', '7270', '7182', '7059', '7043', '7013', '7005', '6795', '6721', '6663', '6572', '6316', '6315', '6077', '5736', '5733', '5732', '5731', '5729', '5728', '5607', '5606', '5605', '5604', '5603', '5602', '5601', '5567', '5493', '5406', '5314', '5302', '5249', '5027', '5004', '4903', '4870', '4797', '4769', '4768', '4754', '4432', '3999', '3994', '3993', '3992', '3638', '3453', '3395', '3319', '3125', '2709', '2708', '2401', '2265']
        # shoenum = ['8205', '8196', '8195', '8194', '8193', '8192', '8191', '8190', '8189', '8188', '8182', '8177', '8176', '8157', '8156', '8155', '8154', '8153', '8152', '8151', '8127', '8126', '8123', '8122', '8118', '8101', '8100', '8099', '8098', '8038', '8022', '8021', '8020', '7506', '7306', '7303', '7301', '7272', '7270', '7234', '7223', '7005', '6874', '6796', '6721', '6534', '6426', '6213', '5394', '5252', '5251', '5249', '5248', '5062', '5061', '4133', '3783', '2264', '1896']
        # shoenum = ['8022']
        # print(len(shoenum),shoenum)

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
            serialno = detail_info_find[6:]
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
        

        if "docs.google.com" in sitelink:
            response = requests.get(sitelink, allow_redirects=True)

            # If there is a redirect, this will give the final URL
            sitelink = response.url

            print(sitelink)
            # telegram_crawl = Telegram_crawl()
            if 'closedform' in sitelink:
                print('???????????')
                pass
            else:
                try:
                    nameentry, phoneentrylen, birthentrylen,  nikeidentry = entrycrawl(sitelink)
                    if birthentrylen is None:
                        birthentry = None
                        birthlen = None
                    else:
                        birthentry = birthentrylen[0]
                        birthlen = birthentrylen[1] # 생년월일 길이

                    if phoneentrylen is None:
                        phoneentry = None
                        phonehyphen = None
                    else:
                        phoneentry = phoneentrylen[0]
                        phonehyphen = phoneentrylen[1] # 폰 하이픈 여부
                    print(nameentry, birthentry, birthlen, phoneentry, phonehyphen, nikeidentry)
                    # Shoesite.objects.filter(shoesiteunique = shoeunique).update(nameentry = nameentry, birthentry = birthentry, phoneentry = phoneentry, nikeidentry = nikeidentry )
                    # telegram_crawl.crawl_entry_msg(nameentry, birthentry, phoneentry, nikeidentry)
                except Exception as e:
                    # telegram_crawl.crawl_entry_error_msg(e)
                    print('error:'+e)
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
            end_date = '2024-12-31 23:59:59'
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

            # 시간이 발매일 경우
            elif '발매' in end_date:
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
                    end_date = end_date + ":00"
                    pub_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

                # Shoesite.objects.filter(shoesiteunique = shoeunique).update(pub_date = pub_date_datetime)

            # 시간이 시작일 경우
            elif '시작' in end_date:
                end_date = end_date.replace("월",'-')
                end_date = end_date.replace(" ",'')
                end_date = end_date.replace("일",' ')
                end_date = end_date.replace("시",'')
                end_date = end_date.replace("작",'')        
                # end_date = end_date + ":59"
                end_date = "".join(end_date)
                end_date = year +'-'+ end_date
                
                if len(end_date) == 11:
                    end_date = end_date.replace(" ",'')
                    pub_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d')
                elif len(end_date) == 16:
                    end_date = end_date + ":00"
                    pub_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

                # Shoesite.objects.filter(shoesiteunique = shoeunique).update(pub_date = pub_date_datetime)

        if 'offline' in sitelink:
            # print(sitelink)
            offline_url = 'https://www.luck-d.com' + sitelink
            offline_html = requests.get(offline_url).text
            offline_soup = BeautifulSoup(offline_html,'html.parser')
            time.sleep(0.01)

            address = offline_soup.select('div.agent_site_info > label > .agent_site_info_data')[1].text.strip()
            normalized_address = unicodedata.normalize('NFC', address)

            # Shoesite.objects.filter(shoesiteunique = shoeunique).update(address = normalized_address)
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

def mijungCheck():
    telegram_crawl = Telegram_crawl()
    try:
        shoesite1231 = Shoesite.objects.filter(end_date='2024-12-31 23:59:59')
        shoelist = []
        for site in shoesite1231:
            shoe = Shoe.objects.get(serialno=site.serialno)
            shoelist.append(shoe)
        product_no_list = []
        for shoe in shoelist:
            # 각 Shoe 객체의 product_no 필드에 접근
            product_no_list.append(shoe.product_no)
        for i in range(len(shoelist)):
            no = int(product_no_list[i])
            url = 'https://www.luck-d.com/release/product/%d/'%no
            html = requests.get(url).text
            soup = BeautifulSoup(html,'html.parser')
            time.sleep(0.1)

            detail_info = soup.select('ul.detail_info>li')
            # print(detail_info)
            for j in range(len(detail_info)):
                detail_info_find = soup.select('ul.detail_info>li')[j].text
                if '제품 코드' in detail_info_find:
                    serialno = detail_info_find[6:].replace('/', '_').strip()
                
            #사이트별       
            sitecard = soup.select('div.release_card')    

            end_date = str(datetime.datetime.now().replace(microsecond=0))
            end_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
            site.end_date = end_date_datetime
            site.save()
            for k in range(len(sitecard)):
                #사이트명
                sitename = soup.select('div.release_card_header > span')[k].text

                sitelink = sitecard[k].a['href']

                shoeunique = serialno+sitename+sitelink

                if site.shoesiteunique == shoeunique:
                    end_date = soup.select('li.release_time > label > span')[k].text.strip()
                    if '미정' in end_date:
                        end_date = '2024-12-31 23:59:59'
                        end_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
                        site.end_date = end_date_datetime
                        site.save()
    except Exception as e:
        print(f'An error occurred: {e}')
        
    telegram_crawl.mijungCheck_msg()

import os
import re

def imgchange():
    # 이미지 폴더 경로 설정
    # image_folder = '/usr/local/share/AlphaRaffle/draw/static/draw/images'
    image_folder = '/Users/jb/AlphaRaffle/draw/static/draw/images'
    # print('실행')
    # 파일명 분석을 위한 정규 표현식 패턴
    shoes = Shoe.objects.filter()

    # 이미지 폴더 내의 모든 파일을 순회
    for filename in os.listdir(image_folder):
        # print(filename)
        for shoe in shoes:
            # 파일명이 shoename과 serialno를 포함하는지 확인
            if shoe.serialno in filename:
                if shoe.shoename in filename:
                    nfc_string = unicodedata.normalize('NFC', filename)
                    new_filename = nfc_string.replace(shoe.shoename, '').replace(' ', '')
                    try:
                        os.rename(os.path.join(image_folder, filename), os.path.join(image_folder, new_filename))
                        print('성공')
                    except Exception as e:
                        print(f'error: {e}')
                # shoename 제거 및 serialno 앞의 공백 제거
                # filename.replace(shoe.shoename, '')
                # print(shoe.shoename)
                # print(filename)
                # new_filename = filename.replace(shoe.shoename, '').replace(' ', '')  # shoename과 공백 제거
                # print(new_filename)
                # 파일 재명명
                # os.rename(os.path.join(image_folder, filename), os.path.join(image_folder, new_filename))

    return redirect('/')

def avif():
    # 이미지 폴더 경로 설정
    # image_folder = '/usr/local/share/AlphaRaffle/draw/static/draw/images'
    # image_folder = '/Users/jb/AlphaRaffle/draw/static/draw/images'
    image_folder = '/Users/jb/AlphaRaffle/draw/static/draw/necessary'
    # print('실행')
    # 파일명 분석을 위한 정규 표현식 패턴
    # shoes = Shoe.objects.filter()

    # 이미지 폴더 내의 모든 파일을 순회
    for filename in os.listdir(image_folder):
        if 'jpeg' in filename or 'png' in filename or 'jpg' in filename:
            try:
                nfc_string = unicodedata.normalize('NFC', filename)
                file_path = os.path.join(image_folder, nfc_string)
                img = Image.open(file_path)
                if img.mode == "P":
                    img = img.convert("RGBA")
                avif_path = os.path.join(image_folder, nfc_string.replace('.jpeg', '.avif').replace('.jpg', '.avif').replace('.png', '.avif'))
                img.save(avif_path, "AVIF")
            except Exception as e:
                print(f'error: {e}')

    return redirect('/')

def deleteimg():
    # image_folder = '/usr/local/share/AlphaRaffle/draw/static/draw/images'
    # image_folder = '/Users/jb/AlphaRaffle/draw/static/draw/images'
    image_folder = '/Users/jb/AlphaRaffle/draw/static/draw/necessary'
    for filename in os.listdir(image_folder):
        if 'jpeg' in filename or 'png' in filename or 'jpg' in filename:
        # if 'avif' in filename:    
            try:
                nfc_string = unicodedata.normalize('NFC', filename)
                file_path = os.path.join(image_folder, nfc_string)
                os.remove(file_path)
                print('삭제 성공')
            except Exception as e:
                print(f'error: {e}')

    return redirect('/')

def cloudflareCacheDeleteAPI():
    import environ
    BASE_DIR = Path(__file__).resolve().parent
    environ.Env.read_env(env_file=os.path.join(BASE_DIR, '.env'))           
    # Cloudflare API 정보
    API_ENDPOINT = "https://api.cloudflare.com/client/v4/zones/256758d25057f54765029dd28e859cdf/purge_cache"
    API_KEY = os.environ.get('CLOUDFLARE_API_KEY')
    EMAIL = os.environ.get('CLOUDFLARE_EMAIL')

    headers = {
        "X-Auth-Email": EMAIL,
        "X-Auth-Key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "purge_everything": True
    }

    response = requests.post(API_ENDPOINT, headers=headers, json=data)

    if response.status_code == 200:
        print("Cache cleared successfully!")
    else:
        print("Error clearing cache:", response.text)

def changeavif():
    import PIL.Image
    from PIL import Image
    img = Image.open('/Users/jb/Downloads/알파래플_핸드오프_Folder/SVG/ar011.png')
    img_resized = img.resize((96, 60), Image.Resampling.LANCZOS)
    # print(img_resized)
    img_resized.save('/Users/jb/Downloads/알파래플_핸드오프_Folder/SVG/ar011-96x96.png', format='PNG')

def changeavif2():
    img = Image.open('/Users/jb/Downloads/알파래플_핸드오프_Folder/SVG/ar011.png')

    # 방법 1: 비율 유지 리사이즈
    aspect_ratio = img.width / img.height
    new_width = 96
    new_height = int(new_width / aspect_ratio)
    img_resized_1 = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # 방법 2: 썸네일 생성
    size = (96, 96)
    img_resized_2 = img.copy()
    img_resized_2.thumbnail(size, Image.Resampling.LANCZOS)

    # 방법 3: 크기 변경 후 자르기
    img_resized_3 = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    left = (img_resized_3.width - 96)/2
    top = (img_resized_3.height - 96)/2
    right = (img_resized_3.width + 96)/2
    bottom = (img_resized_3.height + 96)/2
    img_resized_3 = img_resized_3.crop((left, top, right, bottom))

    # 이미지를 PNG로 저장
    img_resized_1.save('/Users/jb/Downloads/알파래플_핸드오프_Folder/SVG/ar011-96x96_1.png', format='PNG')
    img_resized_2.save('/Users/jb/Downloads/알파래플_핸드오프_Folder/SVG/ar011-96x96_2.png', format='PNG')
    img_resized_3.save('/Users/jb/Downloads/알파래플_핸드오프_Folder/SVG/ar011-96x96_3.png', format='PNG')

def changeavif3(size):
    img = Image.open('/Users/jb/Downloads/알파래플_핸드오프_Folder/SVG/ar011.png')

    # 원본 이미지의 비율 유지하면서, 너비가 96픽셀이 되도록 크기 조절
    aspect_ratio = img.width / img.height
    new_width = size
    new_height = int(new_width / aspect_ratio)
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # 최종 이미지를 생성하고 하얀색으로 채우기
    final_img = Image.new('RGB', (size, size), 'white')

    # 원본 이미지를 최종 이미지의 중앙에 붙여넣기
    y_offset = (final_img.height - img_resized.height) // 2
    final_img.paste(img_resized, (0, y_offset))

    # 이미지를 PNG로 저장
    final_img.save(f'/Users/jb/Downloads/알파래플_핸드오프_Folder/SVG/apple-touch-icon-{size}x{size}.png', format='PNG')

def debuging():
    shoesite = Shoesite.objects.filter(end_date='2024-12-31 23:59:59')
    end_date = datetime.datetime.now()
    # end_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    end_date_datetime = end_date.strftime('%Y-%m-%d %H:%M:%S')
    for site in shoesite:
        site.end_date = end_date_datetime
        site.save()
