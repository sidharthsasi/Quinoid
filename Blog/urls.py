from django.urls import path
from .views import *

urlpatterns = [
    path('post-create/', BlogPostListCreateAPIView.as_view(), name='post--create'),
    path('post-detail/<int:pk>/', BlogPostDetailAPIView.as_view(), name='post-detail'),
    path('post-update/<int:pk>/update/', BlogPostDetailAPIView.as_view(), name='post-update'),
    path('post-delete/<int:pk>/delete/', BlogPostDetailAPIView.as_view(), name='post-delete'),
    path('blogpost-list/', BlogPostListView.as_view(), name='blogpost-list'),
    path('blogpost-search/', BlogPostSearchListView.as_view(), name='blogpost-search'),
]