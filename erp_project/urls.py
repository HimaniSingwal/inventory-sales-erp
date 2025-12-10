from django.contrib import admin
from django.urls import path, include   # include add kiya

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),   # yeh new line
]

