from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),  # Chat view ke liye URL
]

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
]
