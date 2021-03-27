
from django.urls import path
from . import views

urlpatterns = [
    path('',views.wallIndex),
    path('post_message', views.postMessage),
    path('post_comment', views.postComment),
    path('delete_message',views.delMessage),
    path('delete_comment',views.delComment),
    path('get_created_at',views.getMsgComCreatedAt),
]