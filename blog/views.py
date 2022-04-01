from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from . models import Post


# Create your views here.



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

# Class Based Views will look for template <app>/<model>_<viewtype>.html ie blog/post_list/html
class PostListView(ListView):
    model  = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts' # Post.objects.all() Function based view
    ordering = ['-date_posted'] # To order the posts ie. latest at top
    paginate_by = 5

# To see the post of logged in user only not of other users.
class UserPostListView(ListView):
    model  = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'  
    paginate_by = 5


    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']

    #If we try to post now it will not work because 
    # author is not mentioned and will show integrity error.
    # To override this we need to create another function.

    def form_valid(self, form):
        form.instance.author = self.request.user # Before submit take author as instance and submit to user
        return super().form_valid(form)

        #If we submit now it will create post but 
        # doesn't find absolute path to redirect it.

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # To test the author is trying to update their own post or others.
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# UserPassesTestMixin is used to update own post ie 
# users can only update their own post not others.


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html',{'title':'About'})