from django.contrib import admin

# Register your models here.
from .models import Movie, Review

class MoveAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

admin.site.register(Movie, MoveAdmin)
admin.site.register(Review)