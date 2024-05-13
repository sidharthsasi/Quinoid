from django.shortcuts import render
from rest_framework import status,pagination,generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.exceptions import NotFound


# Create your views here.


class BlogPostListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = BlogPost.objects.filter(author=request.user)
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class BlogPostDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            raise NotFound()

    def get(self, request, pk):
        post = self.get_object(pk)
        self.check_object_permissions(request, post)
        serializer = BlogPostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        self.check_object_permissions(request, post)
        serializer = BlogPostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



class BlogPostPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BlogPostListView(APIView):
    pagination_class = BlogPostPagination

    def get(self, request):
        posts = BlogPost.objects.order_by('-publication_date')
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(posts, request)
        serializer = BlogPostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    


class BlogPostSearchListView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']