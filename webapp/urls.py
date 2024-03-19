from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('my-login/', views.my_login, name='my-login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('record/', views.add_record, name='record'),
    path('update-record/<int:pk>/', views.update_record, name='update-record'),
    path('singular-record/<int:pk>/', views.singular_record, name='singular-record'),
    path('delete-record/<int:pk>/', views.delete_record, name='delete-record'),
    path('view-contact/', views.view_contact, name='view-contact'),
    path('add-contact/', views.add_contact, name='add-contact'),
    path('view-friend-request/', views.view_friend_requests, name='view-friend-request'),
    path('single-contact/<int:pk>/', views.singular_contact, name='single-contact'),
    path('delete-contact/<int:pk>/', views.delete_contact, name='delete-contact'),
    path('logout/', views.user_logout, name='logout'),
    path('accept-friend-request/<int:request_id>/', views.accept_friend_request, name='accept-friend-request'),
    path('reject-friend-request/<int:request_id>/', views.reject_friend_request, name='reject-friend-request'),
    path('upload-image/', views.upload_image, name= 'upload-image'),
    path('delete-image/<int:pk>/', views.delete_image, name='delete-image'),
    path('like-image/<int:image_id>/', views.like_image, name='like-image'),
    path('dislike-image/<int:image_id>/', views.dislike_image, name='dislike-image'),
]
