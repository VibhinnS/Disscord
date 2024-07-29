from django.contrib import admin
from django.urls import path, include
from disscord_servers.views import ServerViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'servers', ServerViewSet)

urlpatterns = [
    
    path('', include(router.urls))

]
