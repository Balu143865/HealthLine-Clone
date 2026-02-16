from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


def category_image_path(instance, filename):
    """Path for category images"""
    return f'categories/{instance.slug}/{filename}'


def article_image_path(instance, filename):
    """Path for article images"""
    return f'articles/{instance.slug}/{filename}'


def profile_photo_path(instance, filename):
    """Path for profile photos"""
    return f'profiles/{instance.user.username}/{filename}'


class Category(models.Model):
    """Category model for article classification"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=category_image_path, blank=True, null=True, help_text="Upload category image")
    image_url = models.CharField(max_length=255, blank=True, help_text="Or enter image URL/path (e.g., images/articles/placeholder.svg)")
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', args=[self.slug])
    
    def get_image_url(self):
        """Return the appropriate image URL"""
        # Prioritize image_url over image field for imported articles
        if self.image_url:
            # If it's an external URL (http/https), use it directly
            if self.image_url.startswith('http://') or self.image_url.startswith('https://'):
                return self.image_url
            # If it's already a full path, use it directly
            if self.image_url.startswith('/'):
                return self.image_url
            # If it looks like a static path, prefix with /static/
            elif self.image_url.startswith('images/'):
                return f'/static/{self.image_url}'
            # Otherwise assume it's in the articles folder
            return f'/static/images/articles/{self.image_url}'
        elif self.image and hasattr(self.image, 'url'):
            # Only use ImageField if a file was actually uploaded
            return self.image.url
        return '/static/images/placeholder.svg'


class SubCategory(models.Model):
    """Sub-category for more specific classification"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    
    class Meta:
        verbose_name_plural = "Sub Categories"
        unique_together = ['slug', 'category']
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Article(models.Model):
    """Article model for health content"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    excerpt = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to=article_image_path, blank=True, null=True, help_text="Upload article image")
    image_url = models.CharField(max_length=255, blank=True, help_text="Or enter image URL/path (e.g., images/articles/placeholder.svg)")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')
    
    # Metadata
    author = models.CharField(max_length=100, default="Healthline Team")
    read_time = models.IntegerField(default=5, help_text="Read time in minutes")
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0, help_text="Number of likes")
    
    # Flags
    is_featured = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    
    # Status
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])
    
    def get_image_url(self):
        """Return the appropriate image URL"""
        # Prioritize image_url over image field for imported articles
        if self.image_url:
            # If it's an external URL (http/https), use it directly
            if self.image_url.startswith('http://') or self.image_url.startswith('https://'):
                return self.image_url
            # If it's already a full path, use it directly
            if self.image_url.startswith('/'):
                return self.image_url
            # If it looks like a static path, prefix with /static/
            elif self.image_url.startswith('images/'):
                return f'/static/{self.image_url}'
            # Otherwise assume it's in the articles folder
            return f'/static/images/articles/{self.image_url}'
        elif self.image and hasattr(self.image, 'url'):
            # Only use ImageField if a file was actually uploaded
            return self.image.url
        return '/static/images/placeholder.svg'


class Newsletter(models.Model):
    """Newsletter subscription model"""
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.CharField(max_length=255, blank=True, help_text="Avatar URL or initials")
    profile_photo = models.ImageField(upload_to=profile_photo_path, blank=True, null=True, help_text="Profile photo")
    saved_articles = models.ManyToManyField(Article, blank=True, related_name='saved_by')
    liked_articles = models.ManyToManyField(Article, blank=True, related_name='liked_by')
    
    def __str__(self):
        return self.user.username
    
    @property
    def initials(self):
        name = self.user.get_full_name() or self.user.username
        return name[0].upper() if name else 'U'
    
    def get_avatar_url(self):
        """Return the appropriate avatar URL"""
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url
        elif self.avatar:
            # If avatar is a URL
            if self.avatar.startswith('http://') or self.avatar.startswith('https://'):
                return self.avatar
            # If avatar is a path
            if self.avatar.startswith('/'):
                return self.avatar
            # Otherwise assume it's initials or use default
            return None
        return None
