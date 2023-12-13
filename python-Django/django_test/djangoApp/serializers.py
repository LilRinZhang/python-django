from rest_framework import serializers
from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from .models import Category, Post

# ユーザーシリアライザー
class UserSerializer(serializers.ModelSerializer):
    """ユーザーシリアライザー"""
    class Meta:
        model = get_user_model()
        fields = '__all__'

# カテゴリシリアライザ
class CategorySerializer(serializers.ModelSerializer):
    """カテゴリシリアライザ"""
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class PostSerializer(serializers.ModelSerializer):
    """投稿シリアライザ"""
    class Meta:
        model = Post
        fields = '__all__'

class SearchCategory(filters.FilterSet):
    """カテゴリサーチ"""
    category_name = filters.CharFilter(lookup_expr='contains')
    class Meta:
        model = Category
        fields = ('id', 'category_name')
