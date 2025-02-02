from rest_framework import serializers
from django.utils.text import slugify
from .models import Post
from datetime import datetime
from django.utils.timezone import now

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "title", "slug", "main_image_url",'summary', 'category', "content", "is_published", "publish_at", "created_at", "updated_at"]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def validate_title(self, value):
        """بررسی حداقل طول عنوان"""
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters.")
        return value

    def validate_content(self, value):
        """بررسی اینکه محتوا حتماً یک لیست باشد"""
        if not isinstance(value, list):
            raise serializers.ValidationError("Content must be a list.")
        return value

    def validate_publish_at(self, value):
        """بررسی اینکه تاریخ انتشار نباید در گذشته باشد"""
        if value and value < now():
            raise serializers.ValidationError("Publish date cannot be in the past.")
        return value

    def create(self, validated_data):
        """ایجاد پست جدید با مقداردهی خودکار `slug`"""
        title = validated_data["title"]
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while Post.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        validated_data["slug"] = slug

        if "publish_at" in validated_data and validated_data["publish_at"] is not None:
            validated_data["is_published"] = False  # اگر زمان انتشار تعیین شده باشد، در ابتدا منتشر نشود

        return super().create(validated_data)




class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["id", 'title', 'created_at', 'main_image_url', 'summary', 'category']

