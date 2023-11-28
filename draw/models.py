from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

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
	product_no = models.CharField(max_length=10, blank=True, null=True)

	def __str__(self):
		return "제품코드: " + self.serialno + "      ,     신발명 : " + self.shoename
	
	def increase_views(self):
		self.views += 1
		self.save()

	# 색인
	def get_absolute_url(self):
		cleaned_serialno = ''.join(char for char in self.serialno if ord(char) > 31)
		return f'/auth/details/?serialnum={cleaned_serialno}'

	def calculate_average_overall_rating(self):
		return self.ratings.aggregate(models.Avg('overall_rating'))['overall_rating__avg'] or 0

	def calculate_average_comfort(self):
		return self.ratings.aggregate(models.Avg('comfort'))['comfort__avg'] or 0

	def calculate_average_size_fit(self):
		return self.ratings.aggregate(models.Avg('size_fit'))['size_fit__avg'] or 0

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
	address = models.CharField(max_length=100, blank=True, null=True)

	def __str__(self):
		return "제품코드: " + self.serialno + " , 사이트 : " + self.sitename


class Rating(models.Model):
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    overall_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])  # 총 평가
    comfort = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])  # 체감 편의성
    size_fit = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])  # 체감 사이즈
    
    created_at = models.DateTimeField(auto_now_add=True)

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

class DeletionReason(models.Model):
	quality = models.BooleanField(default=False)
	difficult = models.BooleanField(default=False)
	comfortable = models.BooleanField(default=False)
	service = models.BooleanField(default=False)
	bug = models.BooleanField(default=False)
	feedback = models.BooleanField(default=False)
	others = models.TextField(blank=True, null=True)

from django.core.exceptions import ValidationError
import os
	
def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'.png .jpeg .jpg .gif .svg만 업로드 가능')

def validate_avif_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.avif']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'.avif만 업로드 가능')

class Banner(models.Model):
	title = models.CharField(max_length=100)
	image = models.ImageField(upload_to='bannerimg/', blank=True, null=True, help_text='.png .jpeg .jpg .gif .svg만 업로드 가능', validators=[validate_image_extension])
	avifimage = models.FileField(upload_to='bannerimg/', blank=True, null=True, help_text='.avif만 업로드 가능', validators=[validate_avif_extension])

	def clean(self):
		# image와 avifimage 둘 다 값이 있거나 둘 다 없는 경우 ValidationError 발생
		if (self.image and self.avifimage) or (not self.image and not self.avifimage):
			raise ValidationError('image와 avifimage 둘 중 하나만 업로드해야 합니다.')

	def save(self, *args, **kwargs):
		self.full_clean()
		super(Banner, self).save(*args, **kwargs)
		
	def __str__(self):
		return "제목: " + self.title

from django.dispatch import receiver
from django.db.models.signals import pre_delete

@receiver(pre_delete, sender=Banner)
def delete_files(sender, instance, **kwargs):
    if instance.image:
        print('Deleting image file:', instance.image.path)
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

    if instance.avifimage:
        print('Deleting AVIF file:', instance.avifimage.path)
        if os.path.isfile(instance.avifimage.path):
            os.remove(instance.avifimage.path)

# 색인
from django.contrib.sitemaps import Sitemap

class ShoeSitemap(Sitemap):
    def items(self):
        return Shoe.objects.all()

sitemaps = {
    'shoes': ShoeSitemap,
}