from django.contrib import admin
from restaurant.models import *

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Seat)
admin.site.register(User)
admin.site.register(Waiting)
admin.site.register(GlobalNum)


