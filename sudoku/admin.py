from django.contrib import admin
from .models import Board, Room, Puzzle

# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    readonly_fields = ['puzzle']

admin.site.register(Room, RoomAdmin)
admin.site.register((Board, Puzzle))