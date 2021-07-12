
from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from django.shortcuts import get_object_or_404
#from .models import User, Book, Chat, DeleteRequest, Feedback
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView, TemplateView
from .forms import ChatForm, CategoryForm, SearchForm, AddPostForm, UpdateForm, UserUpdateForm
from . import models
from .models import Chat, Post, FeedBack, Category
import operator
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from users.models import CustomUser
from users.forms import CustomUserChangeForm
from django.db.models.query_utils import Q


class AboutUsView(TemplateView):
    template_name = 'library/about.html'

# class PostDetailView(TemplateView):
# 	template_name = 'library/user/detail.html'

# def login_form(request):
#     return render(request, 'library/login.html')


### GENERAL ###
def user_registration_form(request):
     return render(request, 'library/register.html')

def register_view(request):
    if request.method =='POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = make_password(request.POST['password'])

        user = CustomUser(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
        user.save()

        messages.success(request, 'Account created successfully')
        return redirect('login')
    else:
        messages.error(request, 'An error occured, please try again!')
        return redirect('register')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            if user.is_admin or user.is_superuser:
                return redirect('admin_dashboard')
            elif user.is_publisher:
                return redirect('publisher_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.info(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'library/login.html')
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')



    


# def user_view(request):
#     return render(request, 'library/user/home.html')


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'library/user/post_list.html'
    context_object_name = 'all_posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(status='p')


class UserCreateChat(LoginRequiredMixin, CreateView):
    form_class = ChatForm
    model = Chat
    template_name = 'library/user/chat_form.html'
    success_url = reverse_lazy('user_chat_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class UserChatList(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'library/user/chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return Chat.objects.filter(posted_at__lte=timezone.now()).order_by('-posted_at')

@login_required
def feedback_view(request):
    if request.method == 'POST':
        feedback = request.POST['feedback']
        current_user = request.user
        username = current_user.username
        feedback = f'Feackback from {username} --->{feedback}'

        a = FeedBack(feedback=feedback)
        a.save()
        messages.success(request, 'Feedback Was Sent. Thank You.')
        return redirect('user_dashboard')
    else:
        return render(request, 'library/user/feedback.html')

def user_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'library/user/detail.html', {'post': post})


class UserCategoryListView(ListView):
    template_name = 'library/user/category.html'
    context_object_name = 'cat_list'
    #paginate_by = 3
    
    def get_queryset(self):
        context = {
            'cat': self.kwargs['category'],
            'posts': Post.objects.filter(category__name=self.kwargs['category'], status='p')
        }
        return context

class CategoryCreateView(LoginRequiredMixin, CreateView):
    form_class = CategoryForm
    model = Post
    template_name = 'library/user/category_form.html'
    success_url = reverse_lazy('logout')

def user_search(request):
    form = SearchForm()
    q = ''
    c = ''
    results = []
    query = Q()
    if 'q' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']

            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__contains=q, status='p')
            results = Post.objects.filter(query)
    return render(request, 'library/user/search.html', {'form': form, 'q': q, 'results': results})

def category_list(request):
    category_list = Category.objects.exclude(name='Default')
    context =  {'category_list': category_list,}
    return context




### FOR PUBLISHER ### 
@login_required
def publisher_view(request):
    form = SearchForm()
    posts = Post.objects.all()
    users = CustomUser.objects.all()
    context = {'posts': posts, 'users': users, 'form': form}
    return render(request, 'library/publisher/home.html', context)

@login_required
def publisher_add_post(request):
    form = AddPostForm()
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']
        file = request.FILES.get('file', '')
        current_user = request.user
        author = current_user

        newpost = Post(title=title, author=author, desc=desc, file=file)
        newpost.save()
        messages.success(request, 'Post was uploaded successfully')
        return redirect('publisher_list')
    else:
        messages.error(request, 'Post was not uploaded successfully')
        return render(request, 'library/publisher/add_post.html', {'form': form})


class PublisherPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'library/publisher/post_list.html'
    context_object_name = 'all_posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(status='p')

def publisher_search(request):
    form = SearchForm()
    q = ''
    c = ''
    results = []
    query = Q()
    if 'q' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']
            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__contains=q, status='p')
            results = Post.objects.filter(query)
    return render(request, 'library/publisher/search.html', {'form': form, 'q': q, 'results': results})


# def publisher_detail(request, slug):
# 	post = get_object_or_404(Post, slug=slug)
# 	return render(request, 'library/publisher/detail.html', {'post': post})


class PublisherCreateChat(LoginRequiredMixin, CreateView):
    form_class = ChatForm
    model = Chat
    template_name = 'library/publisher/chat_form.html'
    success_url = reverse_lazy('publisher_chat_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class PublisherChatList(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'library/publisher/chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return Chat.objects.filter(posted_at__lte=timezone.now()).order_by('-posted_at')

class PublisherManagePost(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'library/publisher/manage_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.order_by('-id')

class PublisherDetailView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Post
    template_name = 'library/publisher/post_detail.html'

class PublisherUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = UpdateForm
    template_name = 'library/publisher/update_post.html'
    success_url = reverse_lazy('publisher_manage_posts')
    success_message = 'Data was updated successfully'


class PublisherDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    template_name = 'library/publisher/confirm_delete.html'
    success_url = reverse_lazy('publisher_manage_posts')
    success_message = 'Data was deleted successfully'


### FOR ADMIN ### 
@login_required
def admin_view(request):
    form = SearchForm()
    posts = Post.objects.all()
    users = CustomUser.objects.all()
    context = {'posts': posts, 'users': users, 'form': form}
    return render(request, 'library/admin/home.html', context)

class AdminCreateChat(LoginRequiredMixin, CreateView):
    form_class = ChatForm
    model = Chat
    template_name = 'library/admin/chat_form.html'
    success_url = reverse_lazy('admin_chat_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class AdminChatList(LoginRequiredMixin, ListView):
    model = Chat
    template_name = 'library/admin/chat_list.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return Chat.objects.filter(posted_at__lte=timezone.now()).order_by('-posted_at')


@login_required
def admin_add_post(request):
    form = AddPostForm()
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']
        file = request.FILES.get('file', '')
        current_user = request.user
        author = current_user

        newpost = Post(title=title, author=author, desc=desc, file=file)
        newpost.save()
        messages.success(request, 'Post was uploaded successfully')
        return redirect('admin_list')
    else:
        messages.error(request, 'Post was not uploaded successfully')
        return render(request, 'library/admin/add_post.html', {'form': form})

class AdminPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'library/admin/post_list.html'
    context_object_name = 'all_posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(status='p')

# def admin_detail(request, slug):
# 	post = get_object_or_404(Post, slug=slug)
# 	return render(request, 'library/admin/detail.html', {'post': post})


class AdminManagePost(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'library/admin/manage_posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.order_by('-id')

class AdminDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'library/admin/post_detail.html'

class AdminUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = UpdateForm
    template_name = 'library/admin/update_post.html'
    success_url = reverse_lazy('admin_manage_posts')
    success_message = 'Data was updated successfully'


class AdminDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Post
    template_name = 'library/admin/confirm_delete.html'
    success_url = reverse_lazy('admin_manage_posts')
    success_message = 'Data was deleted successfully'


def admin_search(request):
    form = SearchForm()
    q = ''
    c = ''
    results = []
    files = 1
    query = Q()
    if 'q' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']

            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__contains=q, status='p')
            results = Post.objects.filter(query)
            page = request.GET.get('page', 1)
            paginator = Paginator(results, 3)
            try:
                files = paginator.page(page)
            except PageNotAnInteger:
                files = paginator.page(1)
            except EmptyPage:
                files = paginator.page(paginator.num_pages)
            if files:
                return render(request, 'library/admin/search.html', {'form': form, 'q': q, 'results': results, 'files':files})
    return render(request, 'library/admin/search.html', {'form': form, 'q': q, 'results': results, 'files':files})


class AdminFeedbackList(LoginRequiredMixin,ListView):
    model = FeedBack
    template_name = 'library/admin/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 3

    def get_queryset(self):
        return FeedBack.objects.order_by('-id')

def admin_create_user(request):
    choice = ['User', 'Publisher', 'Admin']
    choice = {'choice': choice}
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        userType=request.POST['userType']
        email=request.POST['email']
        password=request.POST['password']
        password = make_password(password)
        print("User Type")
        print(userType)
        if userType == "User":
            a = CustomUser(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_user=True)
            a.save()
            messages.success(request, 'User was created successfully!')
            return redirect('admin_list_user')
        elif userType == "Publisher":
            a = CustomUser(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_publisher=True)
            a.save()
            messages.success(request, 'Publisher was created successfully!')
            return redirect('admin_list_user')
        elif userType == "Admin":
            a = CustomUser(first_name=first_name, last_name=last_name, username=username, email=email, password=password, is_admin=True)
            a.save()
            messages.success(request, 'Fellow Admin was created successfully!')
            return redirect('admin_list_user')    
        else:
            messages.success(request, 'Member was not created successfully')
            return redirect('admin_create_user')
    else:
        return render(request, 'library/admin/create_user_form.html', choice)

class ListUserView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'library/admin/admin_list_users.html'
    context_object_name = 'users'
    paginate_by = 4

    def get_queryset(self):
        return CustomUser.objects.all().order_by('-id')


class AdminUserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'library/admin/user_detail.html'

class AdminUserUpdateView(LoginRequiredMixin, SuccessMessageMixin,  UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'library/admin/update_user.html'
    success_url = reverse_lazy('admin_list_user')
    success_message = 'User was updated successfully'


class AdminUserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = CustomUser
    template_name = 'library/admin/confirm_user_delete.html'
    success_url = reverse_lazy('admin_list_user')
    success_message = 'User was deleted successfully'