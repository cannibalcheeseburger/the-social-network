from django.contrib import admin
from  .models import Agenda,Users,Aye,Nay
# Register your models here.

admin.site.register(Agenda)
admin.site.register(Users)
admin.site.register(Aye)
admin.site.register(Nay)