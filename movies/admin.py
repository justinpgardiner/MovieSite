from django.contrib import admin

# Register your models here.
from .models import Movie

class MoveAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

admin.site.register(Movie, MoveAdmin)