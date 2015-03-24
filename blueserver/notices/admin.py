from django.contrib import admin
from notices.models import Notice,UserProfile

admin.site.register(Notice)
# Register your models here.
admin.site.register(UserProfile)