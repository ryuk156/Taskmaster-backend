from django.contrib import admin

from taskmanager.models import Board,Column,Card

# Register your models here.


admin.site.register(Board)
admin.site.register(Column)
admin.site.register(Card)
