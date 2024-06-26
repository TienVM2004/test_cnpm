from django.contrib import admin
from .models import * 
# Register your models here.


@admin.register(Profile)
class ProfileAdminView(admin.ModelAdmin): 
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']