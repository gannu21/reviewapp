from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_photos, name='upload_photos'),
    path('history/', views.history_comments, name='history_comments'),
    path('best/', views.your_best, name='your_best'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
]
