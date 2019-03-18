"""
webproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.contrib import admin
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page="/"), name='logout'),
    path('bookSearch/', views.booksearch, name='booksearch'),
    path('bookInsert/', views.bookInsert, name="bookins"),
    path('authorInsert/', views.authorInsert, name="authorins"),
    path('authorSearch/', views.authorSearch, name="authorsearch"),
    path('publisherInsert/', views.publisherInsert, name="publisherins"),
    path('publisherSearch/', views.publisherSearch, name="publishersearch"),
    path('bookquery/', views.bookquery, name="bookquery"),
    path('bookInsertv2/', views.bookInsertQuery, name="bookinsv2"),
    path('authorquery/', views.authorquery, name="authorquery"),
    path('authorInsertv2/', views.authorInsertQuery, name="authorinsv2"),
    path('publisherquery/', views.publisherquery, name="publisherquery"),
    path('publisherInsertv2/', views.publisherInsertQuery, name="publisherinsv2"),
]

