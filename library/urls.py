from django.urls import path
from .views import (
     admin_view, 
     publisher_view, 
     UserPostListView, 
     login_view, 
     logout_view, 
     user_registration_form,
     register_view,
     UserCreateChat,
     UserChatList,
     feedback_view,
     AboutUsView,
     # PostDetailView,
     user_detail,
     UserCategoryListView,
     CategoryCreateView,
     user_search,
     publisher_add_post,
     PublisherPostListView,
     publisher_search,
     publisher_detail,
     PublisherChatList,
     PublisherCreateChat,
     PublisherManagePost,
     PublisherDeleteView,
     PublisherDetailView,
)
from django.contrib.auth import views as auth_views


urlpatterns = [
     # path('', login_form, name='home'),
     path('registerform/', user_registration_form, name='registerform'),
     path('register/', register_view, name='register'),
     path('login/', login_view, name='login'),
     path('logout/', logout_view, name='logout'),
     path('about/', AboutUsView.as_view(), name='about'),
     # path('detail/', PostDetailView.as_view(), name='detail'),
     



     # System admin's URLs
     path('systemadmin/', admin_view, name='admin_dashboard'),

     # Publisher's URLs
     path('publisher/', publisher_view, name='publisher_dashboard'),
     path('publisher-list/', PublisherPostListView.as_view(), name='publisher_list'),
     path('publisher-add-post/', publisher_add_post, name='publisher_add_post'),
     path('publisher-search/', publisher_search, name='publisher_search'),
     path('publisher-create-chat/', PublisherCreateChat.as_view(), name='publisher_create_chat'),
     path('publisher-chat-list/', PublisherChatList.as_view(), name='publisher_chat_list'),
     path('publisher-manage-post/', PublisherManagePost.as_view(), name='publisher_manage_posts'),
     path('publisher/<slug:slug>/', publisher_detail, name='publisher_detail'),
     path('publisher-deelete-post/<slug:slug>', PublisherDeleteView.as_view(), name='publisher_delete_post'),
      path('publisher-detail/<slug:slug>', PublisherDetailView.as_view(), name='publisher_detail'),


     # User's URLs
    
     path('user/', UserPostListView.as_view(), name='user_dashboard'),
    
     path('user-create-chat/', UserCreateChat.as_view(), name='user_create_chat'),
     path('user-chat-list/', UserChatList.as_view(), name='user_chat_list'),
     path('category-user/<category>/', UserCategoryListView.as_view(), name='user_category'),
     path('feedback/', feedback_view, name='feedback'),
     path('category-form/', CategoryCreateView.as_view(), name='category_form'),
     path('search-user/', user_search, name='user_search'),
     path('user/<slug:slug>/', user_detail, name='user_detail'),

]
