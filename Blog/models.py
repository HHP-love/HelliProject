from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from django.utils import timezone 

# from django.contrib.postgres.fields import JSONField  

class Post(models.Model):
    title = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(5)],
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    main_image_url = models.CharField(
        max_length=1024,  # حداکثر طول URL
        blank=True,
        null=True,
        help_text="URL تصویر اصلی پست"
    )
    summary = models.TextField(default="")
    category = models.CharField(max_length=40, default="")
    content = models.JSONField(
        default=list,
        help_text="لیستی از محتوای پست شامل متن، تصاویر، ویدیوها و غیره"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    publish_at = models.DateTimeField(blank=True, null=True, help_text="تاریخ و زمان انتشار پست")

    def save(self, *args, **kwargs):
        if self.publish_at and self.publish_at > timezone.now():
            self.is_published = False
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']



from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"
