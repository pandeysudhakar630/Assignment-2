from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User

@login_required
def chat_view(request):
    users = User.objects.exclude(id=request.user.id)  # Current user ke alawa sabhi users
    messages = Message.objects.filter(receiver=request.user)  # Current user ke received messages
    return render(request, 'messaging/chat.html', {'users': users, 'messages': messages})
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate

# Signup view
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('chat')  # Redirect after login
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('chat')  # Redirect after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials'})
    return render(request, 'login.html')

from django.contrib.auth.models import User

def chat_view(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude current logged-in user
    return render(request, 'chat.html', {'users': users})
def chat_view(request, user_id):
    users = User.objects.exclude(id=request.user.id)
    selected_user = User.objects.get(id=user_id)  # Get selected user
    messages = Chat.objects.filter(
        (Q(sender=request.user) & Q(receiver=selected_user)) |
        (Q(sender=selected_user) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    if request.method == "POST":
        message = request.POST['message']
        Chat.objects.create(sender=request.user, receiver=selected_user, message=message)
    
    return render(request, 'chat.html', {'users': users, 'selected_user': selected_user, 'messages': messages})
