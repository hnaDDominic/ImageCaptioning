from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/caption-feedback/', views.handle_caption_feedback, name='caption_feedback'),
    path('statistics/', views.statistics_dashboard, name='statistics_dashboard'),
]