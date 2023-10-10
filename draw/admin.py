
from django.contrib import admin
from .models import Shoe, Member, Shoeimg, Shoesiteimg, Shoesite, Comment, SearchTerm, VerificationCode

# Register your models here.
admin.site.register(Shoe)
admin.site.register(Member)
admin.site.register(Shoeimg)
admin.site.register(Shoesiteimg)
admin.site.register(Shoesite)
admin.site.register(Comment)
admin.site.register(SearchTerm)
admin.site.register(VerificationCode)