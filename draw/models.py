from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Shoe(models.Model):
	shoename = models.CharField(max_length=200) 		# 신발명
	shoeimg = models.ImageField(blank = True)
	Link = models.CharField(max_length=200)				# 신발링크
	Site = models.CharField(max_length=200)				# 발매사이트
	nameentry = models.CharField(max_length=200, default= None, blank = True)			
	birthentry = models.CharField(max_length=200, default= None, blank = True)			
	phoneentry = models.CharField(max_length=200, default= None, blank = True)	
	nikeidentry = models.CharField(max_length=200, default= None, blank = True)	
	pub_date = models.DateTimeField('date published')	# 발매기간
	end_date = models.DateTimeField('date end')
	def __str__(self):
		return self.shoename


class Member(models.Model):
	member_no = models.AutoField(db_column='member_no', primary_key=True)
	member_id = models.CharField(db_column='member_id', max_length=50)
	member_pwd = models.CharField(db_column='member_pwd', max_length=50)
	member_realname = models.CharField(db_column='member_realname', max_length=200)
	member_email = models.CharField(db_column='member_email', max_length=255)
	member_nickname = models.CharField(db_column='member_nickname', max_length=200)
	member_birth = models.CharField(db_column='member_birth', max_length=200)
	member_nikeid = models.CharField(db_column='member_nikeid', max_length=200)
	member_phonenumber = models.CharField(db_column='member_phonenumber', max_length=200)
	usage_flag = models.CharField(db_column='usage_flag', max_length=10, default='1')
	register_date = models.DateTimeField(db_column='register_date', )

	class Meta:
		managed = False
		db_table = 'member'

	def __str__(self):
		return "아이디: " + self.member_id + ", 이메일 : " + self.member_email

