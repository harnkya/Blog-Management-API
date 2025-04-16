from rest_framework import serializers
from blog.models import Blog, Comment
from datetime import date


class BlogSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()  # Custom field to get the author's username
    def get_author(self, obj):
        return obj.author.username  # Author'ın username'ini döndürür

    class Meta:
        model = Blog
        fields = '__all__'
        exception = ['created_at', 'updated_at']  # read_only fields


class CommentSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()  # Custom field to get the author's username
    def get_author(self, obj):
        return obj.author.username  # returns the author's username

    blog = serializers.SerializerMethodField()  # Custom field to get the blog's title
    def get_blog(self, obj):
        return obj.blog.title  # returns the blog's title

    class Meta:
        model = Comment
        fields = '__all__'
