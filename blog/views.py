from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, FormView, ListView, UpdateView
from django.views.generic.list import MultipleObjectMixin

from blog.forms import CommentModelForm, ContactForm, RegisterForm
from blog.models import Comment, CustomUser, Post

User = get_user_model()


def index(request):
    """Start page where User can sign up/sign in"""
    posts = (
        Post.objects.filter(is_published=True).annotate(comment_count=Count("comment__id")).order_by("-comment_count")
    )
    return render(request, "blog/index.html", {"posts": posts})


class RegisterFormView(FormView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("blog:profile")

    def form_valid(self, form):
        user = form.save()
        # user = authenticate(self.request, username=user.username, password=form.cleaned_data.get("password1"))
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UserProfile(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "registration/profile.html"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    fields = ["first_name", "last_name", "email", "about", "avatar"]
    template_name = "registration/update_profile.html"
    success_url = reverse_lazy("blog:profile")
    success_message = "Profile updated"

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    fields = ["title", "description", "body", "image"]
    template_name = "blog/post_create.html"
    success_message = "Post created. Wait for approve by admin"

    def form_valid(self, form):
        post_object = form.save(commit=False)
        post_object.author = self.request.user
        post_object.save()
        post_path = f"http://127.0.0.1:5000/post/{post_object.id}"
        send_mail(
            "New post!",
            loader.render_to_string(
                "blog/new_post_email.html",
                {"author": post_object.author, "title": post_object.title, "post_path": post_path},
            ),
            settings.NOREPLY_EMAIL,
            ["admin@a.com"],
            fail_silently=False,
        )
        return super().form_valid(form)


class PostDetailView(DetailView, MultipleObjectMixin):
    model = Post
    template_name = "blog/post_detail.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        comments_list = Comment.objects.filter(post__id=self.object.id, is_published=True)
        context = super(PostDetailView, self).get_context_data(object_list=comments_list, **kwargs)
        paginator = Paginator(comments_list, 10)
        page = self.request.GET.get("page")
        context["image"] = self.object.image
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
        context["comments"] = comments
        return context


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    fields = ["title", "description", "body", "image"]
    template_name = "blog/post_update.html"
    success_message = "Post updated"


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("blog:my_post_list")
    success_message = "Post deleted"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostListView(ListView):
    """Show all Posts in one Theme with count of Comments for each"""

    model = Post
    context_object_name = "post"
    paginate_by = 10

    def get_queryset(self):
        return (
            Post.objects.filter(is_published=True)
            .annotate(comment_count=Count("comment__id", filter=Q(is_published=True)))
            .order_by("created_on")
        )


class MyPostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "post"
    template_name = "blog/my_post_list.html"
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).annotate(comment_count=Count("comment__id"))


class AuthorListView(ListView):
    model = CustomUser
    context_object_name = "author"
    template_name = "blog/author_list.html"
    paginate_by = 20

    def get_queryset(self):
        return CustomUser.objects.all()


class AuthorDetailView(DetailView):
    model = CustomUser
    context_object_name = "author"
    template_name = "blog/author_detail.html"


def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    post_path = f"http://127.0.0.1:5000/post/{post.id}"
    if request.method == "POST":
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                post_id=pk,
                author=form.cleaned_data["author"],
                comment_text=form.cleaned_data["comment_text"],
            )
            send_mail(
                "New post!",
                loader.render_to_string(
                    "blog/new_comment_email.html",
                    {"author": comment.author, "comment": comment.comment_text, "post_path": post_path},
                ),
                settings.NOREPLY_EMAIL,
                ["admin@a.com", f"{post.author.email}"],
                fail_silently=False,
            )
            return redirect(reverse("blog:post_detail", args=(pk,)))
    else:
        if user.is_authenticated:
            form = CommentModelForm(initial={"author": request.user.username})
        else:
            form = CommentModelForm()
    return render(request, "blog/create_comment.html", {"form": form, "post": post})


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(
                form.cleaned_data.get("subject"),
                form.cleaned_data.get("message"),
                settings.NOREPLY_EMAIL,
                [form.cleaned_data.get("from_email")],
                fail_silently=False,
            )
            return redirect(reverse("blog:index"))
    else:
        form = ContactForm()
    return render(request, "blog/contact_us.html", {"form": form})
