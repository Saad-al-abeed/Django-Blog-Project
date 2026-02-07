from django.shortcuts import render, redirect, get_object_or_404
from blogs.models import Category, Blog
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CategoryForm, BlogPostForm, AddUserForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

@login_required(login_url="login")
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
            "category_count" : category_count,
            "blogs_count" : blogs_count
        }
    return render(request, "dashboard/dashboard.html", context)

@login_required(login_url="login")
@permission_required('blogs.view_category', raise_exception=True)
def categories(request):
    return render(request, "dashboard/categories.html")

@login_required(login_url="login")
@permission_required('blogs.add_category', raise_exception=True)
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categories")
    form = CategoryForm()
    context = {
            "form" : form
        }
    return render(request, "dashboard/add_category.html", context)

@login_required(login_url="login")
@permission_required('blogs.change_category', raise_exception=True)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("categories")
    form = CategoryForm(instance=category)
    context = {
            "form" : form,
            "category" : category
        }
    return render(request, "dashboard/edit_category.html", context)

@login_required(login_url="login")
@permission_required('blogs.delete_category', raise_exception=True)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect("categories")

@login_required(login_url="login")
def posts(request):
    is_privileged = request.user.is_superuser or request.user.groups.filter(name__in=['Managers', 'Editors']).exists()
    if is_privileged:
        posts = Blog.objects.all()
    else:
        posts = Blog.objects.filter(author=request.user)
    context = {
            "posts" : posts
        }
    return render(request, "dashboard/posts.html", context)

@login_required(login_url="login")
def add_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) # temporarily saving the form
            post.author = request.user
            post.save() # required to access post.id
            title = form.cleaned_data["title"]
            post.slug = slugify(title) + "-" + str(post.id)
            post.save()
            return redirect("posts")
    form = BlogPostForm()
    context = {
            "form" : form
        }
    return render(request, "dashboard/add_post.html", context)

@login_required(login_url="login")
def edit_post(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    # --- PERMISSION CHECK START ---
    # 1. Define who is a "privileged" user (Superuser, Manager, or Editor)
    is_privileged = request.user.is_superuser or request.user.groups.filter(name__in=['Managers', 'Editors']).exists()

    # 2. Check if the user is the owner (Assuming your model has an 'author' field)
    is_owner = blog.author == request.user

    # 3. If they are NEITHER privileged NOR the owner, block them.
    if not (is_privileged or is_owner):
        raise PermissionDenied  # This returns a 403 Forbidden error
    # --- PERMISSION CHECK END ---

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            post = form.save(commit=False) # temporarily saving the form
            post.save() # required to access post.id
            title = form.cleaned_data["title"]
            post.slug = slugify(title) + "-" + str(post.id)
            post.save()
            return redirect("posts")
    form = BlogPostForm(instance=blog)
    context = {
            "form" : form,
            "blog" : blog
        }
    return render(request, "dashboard/edit_post.html", context)

@login_required(login_url="login")
def delete_post(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    # --- PERMISSION CHECK START ---
    # 1. Define who is a "privileged" user (Superuser, Manager, or Editor)
    is_privileged = request.user.is_superuser or request.user.groups.filter(name__in=['Managers', 'Editors']).exists()

    # 2. Check if the user is the owner (Assuming your model has an 'author' field)
    is_owner = blog.author == request.user

    # 3. If they are NEITHER privileged NOR the owner, block them.
    if not (is_privileged or is_owner):
        raise PermissionDenied  # This returns a 403 Forbidden error
    # --- PERMISSION CHECK END ---

    blog.delete()
    return redirect("posts")

@login_required(login_url="login")
@permission_required('auth.view_user', raise_exception=True)
def users(request):
    users = User.objects.exclude(is_superuser=True)
    context = {
            "users" : users
        }
    return render(request, "dashboard/users.html", context)

@login_required(login_url="login")
@permission_required('auth.add_user', raise_exception=True)
def add_user(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users")
    form = AddUserForm()
    context = {
            "form" : form
        }
    return render(request, "dashboard/add_user.html", context)

@login_required(login_url="login")
@permission_required('auth.change_user', raise_exception=True)
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users")
    form = EditUserForm(instance=user)
    context = {
            "form" : form,
            "user" : user
        }
    return render(request, "dashboard/edit_user.html", context)

@login_required(login_url="login")
@permission_required('auth.delete_user', raise_exception=True)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect("users")
