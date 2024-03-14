from django.contrib import admin

# Register your models here.

from . models import Customer, Contact, FriendRequest

admin.site.register(Customer)
admin.site.register(Contact)
admin.site.register(FriendRequest)
