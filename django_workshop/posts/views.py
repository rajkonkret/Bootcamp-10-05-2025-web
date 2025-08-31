from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post

def home(request):
    return HttpResponse("Hello Django!")

class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = "posts/post_list.html"

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "body"]
    success_url = reverse_lazy("post-list")
    template_name = "posts/post_form.html"

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["title", "body"]
    success_url = reverse_lazy("post-list")
    template_name = "posts/post_form.html"

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("post-list")
    template_name = "posts/post_confirm_delete.html"
