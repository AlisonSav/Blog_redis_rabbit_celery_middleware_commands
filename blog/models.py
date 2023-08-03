from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class CustomUser(AbstractUser):  # noqa DJ10, DJ11
    email = models.EmailField(unique=True)
    about = models.CharField(max_length=200)
    avatar = models.ImageField("avatar", upload_to="images", blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.username}, {self.email}, {self.about}"

    def get_absolute_url(self):
        return reverse("blog:author_detail", kwargs={"pk": self.pk})


class Post(models.Model):  # noqa DJ10, DJ11
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    body = models.TextField()
    image = models.ImageField(upload_to="images", blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}. by {self.author}. Created on: {self.created_on:'%d.%m.%Y, %H:%m'}. "

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.pk})


class Comment(models.Model):  # noqa DJ10, DJ11
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, blank=True, null=True)
    author = models.CharField(max_length=50)
    comment_text = models.TextField()
    is_published = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment: {self.comment_text}. Author: {self.author}. {self.created_on:'%d.%m.%Y, %H:%m'}"
