from django.db import models
from autoslug import AutoSlugField
from django.utils.text import slugify
from django.contrib.auth.models import User
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.models import CloudinaryField 

# Category Model
class Category(models.Model):  
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)  

    def __str__(self):
        return self.name

# Blog Post Model
class Post(models.Model):
    STATUS_CHOICES = [
        ('0', 'Draft'),
        ('1', 'Publish')
    ]

    SECTION_CHOICES = [
        ('recent', 'Recent'),
        ('popular', 'Popular'),
        ('trending', 'Trending'),
    ]

    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = CloudinaryField('image', null=True, blank=True)
    content = models.TextField()
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE) 
    blog_slug = AutoSlugField(populate_from="title", unique=True, always_update=True) 
    date = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, default='0')  
    main_post = models.BooleanField(default=False)
    section = models.CharField(choices=SECTION_CHOICES, max_length=10, default='recent')

    class Meta:
        ordering = ['-date'] 

    def __str__(self):
        return self.title



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('image', null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")  # Parent for replies
    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"