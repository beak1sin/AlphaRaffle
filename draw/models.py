from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Shoe(models.Model):
	shoename = models.CharField(max_length=200) 		# 신발명
	shoeengname = models.CharField(max_length=200) 		# 신발영어명	
	shoebrand = models.CharField(max_length=200)		# 신발브랜드
	serialno = models.CharField(max_length=50,unique=True, default= None)			# 발매사이트
	pubdate = models.CharField(max_length=200)			# 발매일
	shoeprice = models.CharField(max_length=200)		# 발매가
	shoedetail = models.TextField(default = '-')		# 신발 설명

	def __str__(self):
		return self.shoename
		
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
	is_active = models.BooleanField(db_column='is_active', default=False)

	class Meta:
		managed = False
		db_table = 'member'

	def __str__(self):
		return "아이디: " + self.member_id + ", 이메일 : " + self.member_email
	
class Comment(models.Model):
	serialno = models.CharField(max_length=200, db_column='serialno')
	member_nickname = models.CharField(max_length=20, db_column='member_nickname')
	comment = models.CharField(max_length=200, db_column='comment')
	created_date = models.DateTimeField(db_column='created_date')
	approved_comment = models.BooleanField(db_column='approved_comment', default=False)

