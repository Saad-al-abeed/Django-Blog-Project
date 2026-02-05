#from django.http import HttpResponse
from django.shortcuts import render, redirect
from blogs.models import Blog
from assignments.models import About
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib import messages

def home(request):
    featured_posts = Blog.objects.filter(is_featured=True, status="Published").order_by('updated_at')
    posts = Blog.objects.filter(is_featured=False, status="Published")

    try:
        about = About.objects.get()
    except:
        about = None

    context = {
        "featured_posts" : featured_posts,
        "posts" : posts,
        "about" : about
        }
    return render(request, "home.html", context)

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("register")
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    context = {
            "form" : form
        }
    return render(request, "register.html", context)

def login(request):
    if request.method == "POST":
        # FIX 1: Pass 'request' first, then data=request.POST
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = AuthenticationForm()

    context = {
        "form": form
    }
    return render(request, "login.html", context)

def logout(request):
    auth.logout(request)
    return redirect("Home")
