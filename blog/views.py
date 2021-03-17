from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from django.contrib.auth.models import User
from .forms import IncognitoCommentForm, UserCommentForm


def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # default template name is "<app>/<model>_<viewtype>.html"
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(post=self.get_object()).order_by('-date_posted')
        context['comments'] = comments

        if self.request.user.is_authenticated:
            context['comment_form'] = UserCommentForm(instance=self.request.user)
        else:
            context['comment_form'] = IncognitoCommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            new_comment = Comment(post=self.get_object(),
                                  name=self.request.user,
                                  content=request.POST.get('content'))
        else:
            new_comment = Comment(post=self.get_object(),
                                  name=request.POST.get('name'),
                                  content=request.POST.get('content'))
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    # template name that CreateView is using by default is '<model>_form.html
    model = Post
    fields = ['title', 'content']
    # success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # template name that UpdateView is using by default is '<model>_form.html
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    # template name that DeleteView is using by default is '<model>_confirm_delete.html
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {})


