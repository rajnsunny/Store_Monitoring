from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store_monitoring_app.urls')),
    # Add other app URLs if you have more apps in your project
]
