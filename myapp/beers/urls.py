from django.urls import path
from django.contrib import admin
from . import views

app_name = 'beers'
urlpatterns = [
    #path('', views.indexView, name='index'),
    path('', views.loginView, name='login'),
    path('login/', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('home/', views.homeView, name='home'),
    path('beer/<int:pk>/', views.beerView, name='beer'),
    path('review/<int:pk>/', views.reviewView, name='review'),
    path('about/', views.aboutView, name='about'),
    path('logout/', views.logoutView, name='logout'),

    #path('logout/', views.loginView, name='login')
    #path('create_new/', views.create_new),
    #path('beer/<int:beer_id>', views.beer),
    #path('rate/<int:beer_id>', views.rate, name='rate'),
    #path('delete/<int:beer_id>', views.delete, name='delete'),


]