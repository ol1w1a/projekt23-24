from django.urls import path
from . import views

urlpatterns = [
    path('',views.idea_list,name='idea_list'),
    path('idea/<int:pk>/', views.idea_detail, name = 'idea_detail'),
    path('add/',views.idea_create, name='idea_create'),
]