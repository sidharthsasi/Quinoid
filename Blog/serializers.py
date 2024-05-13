from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author','publication_date', 'created_at', 'updated_at']
        read_only_fields = ['author', 'created_at', 'updated_at']