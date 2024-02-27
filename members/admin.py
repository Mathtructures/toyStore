from django.contrib import admin
from .models import Member

# Register your models here.
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name','username','id','is_staff','is_superuser','is_active')
  
admin.site.register(Member,MemberAdmin)