from django.contrib import admin
from django.urls import path
from logs.views import analyze_view, dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('analyze/', analyze_view),
    path('', dashboard, name='dashboard'),
]