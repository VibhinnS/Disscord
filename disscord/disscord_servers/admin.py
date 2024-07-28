from django.contrib import admin
from .models import Server, Channel
# Register your models here.

class ChannelInline(admin.TabularInline):
    model = Channel
    extra = 1

class ServerAdmin(admin.ModelAdmin):
    inlines = [ChannelInline]

admin.site.register(Server, ServerAdmin)