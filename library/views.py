from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
#from .models import User, Book, Chat, DeleteRequest, Feedback
from django.contrib import messages
from django.db.models import Sum
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
#from .forms import ChatForm, BookForm, UserForm
from . import models
from .models import Post
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


# def login_form(request):
#     return render(request, 'library/login.html')
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

def logout_view(request):
    logout(request)
    return redirect('login')



def admin_view(request):
    return render(request, 'library/admin/home.html')

def publisher_view(request):
    return render(request, 'library/publisher/home.html')

# def user_view(request):
#     return render(request, 'library/user/home.html')


class UserPostListView(ListView):
	model = Post
	template_name = 'library/user/post_list.html'
	context_object_name = 'all_posts'
	#paginate_by = 5

	def get_queryset(self):
		return Post.objects.filter(status='p').order_by('-id')


