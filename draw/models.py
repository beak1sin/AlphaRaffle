from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User

class Member(models.Model):
	member_no = models.AutoField(db_column='member_no', primary_key=True)
	member_id = models.CharField(db_column='member_id', max_length=50)
	member_pwd = models.CharField(db_column='member_pwd', max_length=50)
	member_realname = models.CharField(db_column='member_realname', max_length=200)
	member_email = models.CharField(db_column='member_email', max_length=255)
	member_nickname = models.CharField(db_column='member_nickname', max_length=20)
	member_birth = models.CharField(db_column='member_birth', max_length=200)
	member_nikeid = models.CharField(db_column='member_nikeid', max_length=200)
	member_phonenumber = models.CharField(db_column='member_phonenumber', max_length=200)
	usage_flag = models.CharField(db_column='usage_flag', max_length=10, default='1')
	register_date = models.DateTimeField(db_column='register_date')
	profile_img_url = models.CharField(db_column='profile_img_url', max_length=200, default='-', null=True)
	is_active = models.BooleanField(db_column='is_active', default=False)

	class Meta:
		managed = False
		db_table = 'member'

	def __str__(self):
		return "아이디: " + self.member_id + ", id : " + str(self.member_no) + ", 닉네임 : " + self.member_nickname
	
class Shoe(models.Model):
	shoename = models.CharField(max_length=200) 		# 신발명
	shoeengname = models.CharField(max_length=200) 		# 신발영어명	
	shoebrand = models.CharField(max_length=200)		# 신발브랜드
	serialno = models.CharField(max_length=50,unique=True, default= None)			# 제품번호
	pubdate = models.CharField(max_length=200)			# 발매일
	shoeprice = models.CharField(max_length=200)		# 발매가
	shoedetail = models.TextField(default = '-')		# 신발 설명
	shoelikecount = models.IntegerField(default=0)  # 좋아요 개수
	likes = models.ManyToManyField(Member, related_name='liked_posts')
	views = models.PositiveBigIntegerField(default = 0)

	def __str__(self):
		return "제품코드: " + self.serialno + "      ,     신발명 : " + self.shoename
	
	def increase_views(self):
		self.views += 1
		self.save()

	# 색인
	def get_absolute_url(self):
		cleaned_serialno = ''.join(char for char in self.serialno if ord(char) > 31)
		return f'/auth/details/?serialnum={cleaned_serialno}'

class Shoeimg(models.Model):
	serialno = models.CharField(max_length=50, default= None)
	shoeimg = models.CharField(max_length=200, unique=True)	

class Shoesiteimg(models.Model):
	sitename = models.CharField(max_length=200,unique=True)   

class Shoesite(models.Model):
	serialno = models.CharField(max_length=50, default= None)
	sitename = models.CharField(max_length=200)   
	nameentry = models.CharField(max_length=200, null=True, blank=True)         
	birthentry = models.CharField(max_length=200, null=True, blank=True)         
	phoneentry = models.CharField(max_length=200, null=True, blank=True)   
	nikeidentry = models.CharField(max_length=200, null=True, blank=True)
	pub_date = models.DateTimeField('date published', null=True, blank=True)   # 발매기간
	end_date = models.DateTimeField('date end', null=True, blank=True)
	sitelink = models.CharField(max_length=200)
	shoesiteunique = models.CharField(max_length=255,unique=True)

	def __str__(self):
		return "제품코드: " + self.serialno + " , 사이트 : " + self.sitename


class Comment(models.Model):
	serialno = models.CharField(max_length=200, db_column='serialno')
	member_nickname = models.CharField(max_length=20, db_column='member_nickname')
	comment = models.CharField(max_length=200, db_column='comment')
	created_date = models.DateTimeField(db_column='created_date')
	approved_comment = models.BooleanField(db_column='approved_comment', default=False)

class SearchTerm(models.Model):
    member_no = models.CharField(max_length=255)
    term = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
class VerificationCode(models.Model):
	member_id = models.CharField(db_column='member_id', max_length=50)
	code = models.CharField(max_length=6)
	expiry_time = models.DateTimeField()

# 색인
from django.contrib.sitemaps import Sitemap

class ShoeSitemap(Sitemap):
    def items(self):
        return Shoe.objects.all()

sitemaps = {
    'shoes': ShoeSitemap,
}