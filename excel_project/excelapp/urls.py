from django.urls import path
from . import views
# from .views import register, login_view
urlpatterns = [
    path('', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('', views.upload_file, name='upload'),
    path('map/', views.map_columns, name='map_columns'),
]
