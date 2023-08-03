from django.urls import include, path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("contact_us/", views.contact_us, name="contact_us"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", views.RegisterFormView.as_view(), name="register"),
    path("accounts/profile/", views.UserProfile.as_view(), name="profile"),
    path("accounts/update_profile/", views.UpdateProfile.as_view(), name="update_profile"),
    path("post_create/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>", views.PostDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path("post_list/", views.PostListView.as_view(), name="post_list"),
    path("my_post_list/", views.MyPostListView.as_view(), name="my_post_list"),
    path("author_list/", views.AuthorListView.as_view(), name="author_list"),
    path("author/<int:pk>", views.AuthorDetailView.as_view(), name="author_detail"),
    path("post/<int:pk>/comment_create/", views.comment_create, name="comment_create"),
]
