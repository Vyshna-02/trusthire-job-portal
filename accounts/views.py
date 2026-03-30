from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm

def home(request):
    return HttpResponse("Scam-Free Job Portal Home")

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.role == 'EMPLOYER':
                user.is_verified_employer = False
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


from django.contrib.auth import authenticate, login

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'accounts/login.html')

from django.shortcuts import render

def home(request):
    return render(request, 'accounts/home.html')


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')  # redirect to homepage after logout




from django.contrib.auth.forms import AuthenticationForm # Add this import

def user_login(request):
    if request.method == 'POST':
        # Use the built-in AuthenticationForm to handle the data
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    # CRITICAL: You must pass 'form' to the template
    return render(request, 'accounts/login.html', {'form': form})