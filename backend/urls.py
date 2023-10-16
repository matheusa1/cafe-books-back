"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from book.api import viewsets as bookviewsets
from user.api import viewsets as userviewsets
from book.views import BookAPIView
from user.views import UserAPIView, LoginView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



route = routers.DefaultRouter()

route.register(r'book', bookviewsets.BookViewsSet, basename="Book")
route.register(r'user', userviewsets.UserViewsSet, basename="User")
route.register(r'category', bookviewsets.CategoryViewsSet, basename="Category")
route.register(r'author', bookviewsets.AuthorViewsSet, basename="Author")
route.register(r'bookcategory', bookviewsets.BookCategoryViewsSet, basename="BookCategory")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/book/', BookAPIView.as_view()),
    path('api/user/', UserAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/book/category/', CategoryAPIView.as_view()),
    path('api/book/author/', AuthorAPIView.as_view()),
    path('', include(route.urls))
]
