from django.db import models

# Create your models here.

from django.core.validators import MinLengthValidator

class Tag(models.Model):
  caption = models.CharField(max_length=20)

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()

class Post(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200)
    image_name = models.CharField(max_length=100) # montagne.png
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True)
    content = models.TextField(validators=[MinLengthValidator(10)]) # validators souleve une erreur si condition non remplie
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, related_name="posts", null=True)
    tags = models.ManyToManyField(Tag)

class Comment(models.Model):
    author_name = models.CharField(max_length=100)
    text = models.TextField(validators=[MinLengthValidator(1)])
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commentaires")
    date = models.DateTimeField(auto_now_add=True)