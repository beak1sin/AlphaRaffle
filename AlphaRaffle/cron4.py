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
import traceback
import telegram
import asyncio
import aiohttp
import subprocess

currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
year = date.strftime("%Y")
drawpath = Path(__file__).resolve().parent




class Telegram_crawl:
    token = os.environ.get('telegram_token')
    bot = telegram.Bot(token=token)
    chat_id = os.environ.get('telegram_chat_id')

    async def crawl_complete_msg(self):
        try:
            await self.bot.send_message(self.chat_id, '크롤링 성공')
            # 코루틴 실행
            # run_in_new_loop(self.bot.send_message(self.chat_id, '크롤링 성공'))
        except Exception as e:
            print('텔레그램 오류')
            print(f"An error occurred: {e}")
        return
    
    async def crawl_error_msg(self, error):
        try:
            await self.bot.send_message(self.chat_id, f'크롤링 실패:  {error}')
            # run_in_new_loop(self.bot.send_message(self.chat_id, f'크롤링 실패:  {error}'))
        except Exception as e:
            print('텔레그램 오류')
            print(f"An error occurred: {e}")
        return

    async def serverRestart_complete_msg(self):
        try:
            await self.bot.send_message(self.chat_id, '서버 재배포 성공')
            # run_in_new_loop(self.bot.send_message(self.chat_id, '서버 재배포 성공'))
        except Exception as e:
            print('서버 재배포 오류')
            print(f"An error occurred: {e}")
        return

    async def serverRestart_error_msg(self, error):
        try:
            await self.bot.send_message(self.chat_id, f'서버 재배포 실패: {error}')
            # run_in_new_loop(self.bot.send_message(self.chat_id, '서버 재배포 실패'))
        except Exception as e:
            print('서버 재배포 실패 오류')
            print(f"An error occurred: {e}")
        return

    async def cacheDelete_complete_msg(self):
        try:
            await self.bot.send_message(self.chat_id, '캐시 삭제 성공')
            # run_in_new_loop(self.bot.send_message(self.chat_id, '서버 재배포 성공'))
        except Exception as e:
            print('서버 재배포 오류')
            print(f"An error occurred: {e}")
        return

    async def cacheDelete_error_msg(self, error):
        try:
            await self.bot.send_message(self.chat_id, f'캐시 삭제 실패: {error}')
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
    
    async def crawl_entry_msg(self, nameentry, birthentry, phoneentry, nikeidentry):
        try:
            await self.bot.send_message(self.chat_id, f'entry 크롤링 성공 = nameentry: {nameentry}, birthentry: {birthentry}, phoneentry: {phoneentry}, nikeidentry: {nikeidentry}')
            # run_in_new_loop(self.bot.send_message(self.chat_id, f'entry 크롤링 성공 = nameentry: {nameentry}, birthentry: {birthentry}, phoneentry: {phoneentry}, nikeidentry: {nikeidentry}'))
        except Exception as e:
            print('telegram entry 메세지 전송 실패')
            print(f"An error occurred: {e}")
        return
    
    async def crawl_entry_error_msg(self, error):
        try:
            await self.bot.send_message(self.chat_id, f'entry 크롤링 실패:  {error}')
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
    
    def mijungCheck_error_msg(self, error):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, f'종료미정 체크 실패:  {error}'))
        except Exception as e:
            print('텔레그램 오류')
            print(f"An error occurred: {e}")
        return
    
    def nullCheck_msg(self):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, '종료 null 체크'))
        except Exception as e:
            print('종료미정 체크 실패')
            print(f"An error occurred: {e}")
        return
    
    def nullCheck_error_msg(self, error):
        try:
            asyncio.run(self.bot.send_message(self.chat_id, f'종료 null 체크 실패:  {error}'))
        except Exception as e:
            print('텔레그램 오류')
            print(f"An error occurred: {e}")
        return

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


def crontab_aio():
    asyncio.run(crawl_ex())

async def crawl_ex():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://luck-d.com") as resp:
            if resp.status == 200:
                telegram_crawl = Telegram_crawl()
                try:
                    html = await resp.text()
                    soup = BeautifulSoup(html,'html.parser')
                    sitecard = soup.select('div.product_info_layer > div.product_thumb')
                    shoenum = []
                    for i in range(len(sitecard)):    
                        link = sitecard[i].attrs['onclick']
                        shoenum.append(link[39:].split('/')[0].replace("'",""))
                    # print(shoenum)

                    # for num in shoenum:
                    #     now = datetime.datetime.now()
                    #     randomTime = random.randint(30, 60)
                    #     # luckd_crowler(int(num))
                    #     await luckd_crawl_ex(int(num), session)
                    response_sizes = await asyncio.gather(*(luckd_crawl_ex(int(num), session) for num in shoenum))
                    total_response_size = sum(response_sizes)
                    print(f"Total Response Size: {total_response_size /1024/1024}MB")
                    await telegram_crawl.crawl_complete_msg() 
                except:
                    await telegram_crawl.crawl_error_msg(traceback.format_exc())
                    return

                try:
                    # 서브프로세스 실행 담당
                    subprocess.call(['/usr/local/share/AlphaRaffle/bin/start.sh'])
                    await telegram_crawl.serverRestart_complete_msg()
                except:
                    await telegram_crawl.serverRestart_error_msg(traceback.format_exc())
                    return
                try:
                    # 캐시 삭제
                    cloudflareCacheDeleteAPI()
                    await telegram_crawl.cacheDelete_complete_msg()
                except:
                    await telegram_crawl.cacheDelete_error_msg(traceback.format_exc())
                    return


async def luckd_crawl_ex(no, session):
    url = f'https://www.luck-d.com/release/product/{no}/'
    async with session.get(url) as resp:
        if resp.status == 200:
            html = requests.get(url).text
            soup = BeautifulSoup(html,'html.parser')
            
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

            product_detail = '-'
            category = None
            product_color = None

            for i in range(len(detail_info)):
                detail_info_find = soup.select('ul.detail_info>li')[i].text
                if '제품 코드' in detail_info_find:
                    serialno = detail_info_find[6:].replace('/', '_').strip()
                if '발매일' in detail_info_find:
                    shoepubdate = detail_info_find[3:].strip()
                if '발매가' in detail_info_find or '가격' in detail_info_find:
                    shoeprice = detail_info_find[3:].strip()            
                if '카테고리' in detail_info_find:
                    category = detail_info_find[4:].strip()
                if '제품 색상' in detail_info_find:
                    product_color = detail_info_find[5:].strip()            
                if '제품 설명' in detail_info_find:
                    product_detail = detail_info_find[5:].strip()

            # print(serialno, shoepubdate, shoeprice, product_detail)

            try:
                soldout_number = None
                kream_number = None
                trade_info = soup.select('img.trade_platform_img')
                for i in range(len(trade_info)):
                    onclick_string = trade_info[i].get('onclick')
                    if 'soldout' in onclick_string:
                        soldout_number = onclick_string.lower().split('product%2f')[-1].split("');")[0]
                    if 'kream' in onclick_string:
                        kream_number = onclick_string.lower().split('products/')[-1].split("');")[0]
            except Exception as e:
                print(f'soldout, kream 크롤링 실패: {traceback.format_exc()}')
                soldout_number = None
                kream_number = None

            if len(serialno) <= 2:
                print('no serial number')
                return
            else:
                pass

            imgDownload = False
            try:
                Shoe.objects.create(shoename = shoename , shoeengname = subname, serialno = serialno,
                                shoebrand = shoebrand, pubdate = shoepubdate, shoedetail = product_detail, 
                                shoeprice = shoeprice, category = category, product_color = product_color, 
                                product_no = no, soldout_number = soldout_number, kream_number = kream_number)
                imgDownload = True
            except Exception as e:
                Shoe.objects.filter(serialno=serialno).update(shoename = shoename , shoeengname = subname,
                        shoebrand = shoebrand, pubdate = shoepubdate, shoedetail = product_detail, 
                        shoeprice = shoeprice, category = category, product_color = product_color, 
                        product_no = no, soldout_number = soldout_number, kream_number = kream_number)
                print(f"An error occurred {no}: {e}, update complete")
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
                        except:
                            telegram_crawl.crawl_entry_error_msg(traceback.format_exc())

                # #종료일
                end_date = soup.select('li.release_time > label > span')[i].text.strip()

                # 종료일이 미정일 경우
                if '미정' in end_date:
                    end_date = '2024-12-31 23:59:59'
                    end_date_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
                    Shoesite.objects.filter(shoesiteunique = shoeunique).update(end_date = end_date_datetime)
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
                    continue

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




if __name__ == '__main__':
    start = time.perf_counter()
    # asyncio.run(crawl_ex())
    # crontab_aio()
    end = time.perf_counter()
    print(f"elapsed time = {end - start}s")