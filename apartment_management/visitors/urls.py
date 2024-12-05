from django.conf.urls.i18n import urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('visitor/create/', views.visitor_create, name='visitor_create'),
    path('visitor/<int:pk>/update/', views.visitor_update, name='visitor_update'),
    path('visitor/<int:pk>/delete/', views.visitor_delete, name='visitor_delete'),
    path('search/', views.search_visitors, name='search_visitors'),
    path('register/resident/', views.resident_register, name='resident_register'),
    path('register/receptionist/', views.receptionist_register, name='receptionist_register'),

]