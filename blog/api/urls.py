from django.contrib import admin

from django.urls import path
from blog.api import views as api_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/register', api_views.RegisterAPIView.as_view(), name='register'),
    path('auth/login', TokenObtainPairView.as_view(), name='login'),
    path('auth/profile', api_views.ProfileAPIView.as_view(), name='profile'),
    path('blogs', api_views.BlogsAPIView.as_view(), name='blogs'),
    path('blogs/<int:id>', api_views.BlogAPIView.as_view(), name='blog'),
    path('blogs/<int:blog_id>/comments', api_views.CommentsAPIView.as_view(), name='comments'),
    path('comments/<int:id>', api_views.CommentAPIView.as_view(), name='comment'),

]
