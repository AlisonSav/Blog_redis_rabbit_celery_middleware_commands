from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.mail import send_mail

from blog.models import Comment, CustomUser, Post

admin.site.register(CustomUser, UserAdmin)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "description", "body", "is_published", "image")
    search_fields = ["author", "title"]
    list_editable = ["is_published"]
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if form.cleaned_data["is_published"]:
            send_mail(
                "Post has been published",
                "Your post has been published",
                settings.NOREPLY_EMAIL,
                [f"{obj.author.email}"],
                fail_silently=False,
            )
        return obj.save()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "comment_text", "is_published")
    search_fields = ["post", "author"]
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if form.cleaned_data["is_published"]:
            send_mail(
                "Comment has been published",
                "Your comment has been published",
                settings.NOREPLY_EMAIL,
                [f"{obj.author.email}"],
                fail_silently=False,
            )
        return obj.save()
