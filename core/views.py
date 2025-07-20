from django.shortcuts import get_object_or_404, render,redirect
from .models import Post ,Category,UserProfile
from .forms import *
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages

def index(request):
    posts = Post.objects.order_by('-id')  
    main_post = Post.objects.filter(main_post=True).order_by('-id')[:1] 
    recent = Post.objects.filter(section='recent').order_by('-id')[:5]  
    pop = Post.objects.filter(section='popular').order_by('-id')[:5]  
    trending = Post.objects.filter(section='trending').order_by('-id')[:5]  
    categories = Category.objects.all()
    return render(request, 'pages/index.html', {
        'posts': posts,
        'main_post': main_post,
        'recent': recent,
        'categories':categories,
        'pop':pop,
        'trending':trending,
    })

@login_required
def detail(request, blog_slug):
    categories = Category.objects.all() 
    post = get_object_or_404(Post, blog_slug=blog_slug)
    comments = post.comments.filter(parent__isnull=True)  # Only top-level comments
    comment_form = CommentForm()
    recent = Post.objects.filter(section='recent').order_by('-id')[:5]  
    pop = Post.objects.filter(section='popular').order_by('-id')[:5]  
    trending = Post.objects.filter(section='trending').order_by('-id')[:5]  
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            parent_id = request.POST.get("parent_id")
            if parent_id:
                parent_comment = Comment.objects.get(id=parent_id)
                new_comment.parent = parent_comment

            new_comment.save()
            return redirect('detail', blog_slug=post.blog_slug) 
    return render(request, 'pages/detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'categories': categories,
        'recent': recent,
        'pop':pop,
        'trending':trending,
    })


@login_required
def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category).order_by('-date')[:4]  
    categories = Category.objects.all()
    context = {
        'category': category,
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'pages/category.html', context)

def login(request):
    form = Loginform()
    if request.method == 'POST':
        form = Loginform(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            if user: 
                auth_login(request, user)
                messages.success(request, "Login successful!")
                return redirect('/')
        messages.error(request, "Invalid email or password.")

    return render(request, "pages/login.html", {'form': form})




def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES) 
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            image = form.cleaned_data.get('image') 

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken!")
                return redirect('register')
            user = User.objects.create_user(username=username, email=email, password=password)
            profile = user.userprofile
            profile.image = image
            profile.save()
            email_message = EmailMessage(

                subject=f'You have registered successfully {username}',
                body=f'You can now log in using the link below.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
                reply_to=[email]
            )
            email_message.send()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "pages/register.html", {'form': form})
@login_required
def user_logout(request):
    logout(request)
    messages.success(request,"You have been Logged out successfully!")
    return redirect('login')
@login_required
def user_profile(request):
    categories = Category.objects.all() 
    return render(request,'pages/profile.html',{'categories': categories})
@login_required

def mypost(request):
    categories = Category.objects.all() 
    user_posts = Post.objects.filter(author=request.user) 
    return render(request, 'pages/post.html', {'user_posts': user_posts,'categories': categories})




@login_required
def createpost(request):
    categories = Category.objects.all() 
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) 
            post.author = request.user 
            post.save()  
            return redirect('mypost') 
    else:
        form = PostForm()

    return render(request, 'pages/create.html', {'form': form,'categories': categories})



@login_required
def edit(request, edit_id):
    blog = get_object_or_404(Post, id=edit_id, author=request.user)  
    categories = Category.objects.all() 
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=blog)  
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  
            blog.save()
            return redirect('mypost')  
    else:
        form = PostForm(instance=blog)

    context = {'form': form,'categories': categories}
    return render(request, 'pages/edit.html', context)

@login_required
def deletepost(request, task_id):
    task = get_object_or_404(Post, pk=task_id)
    task.delete()
    return redirect('mypost') 

@login_required
def edit_profile(request):
    user = request.user
    categories = Category.objects.all() 
  
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
      
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.save()

     
        profile.dob = request.POST.get("dob")
        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")

        if "image" in request.FILES:
            profile.image = request.FILES["image"]

        profile.save()

        messages.success(request, "Your profile has been updated successfully!")
        return redirect("profile")  

    return render(request, "pages/profileedit.html", {"user": user,'categories': categories})

@login_required
def aboutus(request):
    categories = Category.objects.all() 
    return render(request,'pages/about.html', {'categories': categories})

@login_required
def contactus(request):
    categories = Category.objects.all()
    success = None  
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Compose the email
            admin_email_message = EmailMessage(
                subject=f'Contact Form Submission from {name}',
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['harishadithyan17@gmail.com'],  
                reply_to=[email]  
            )
            email_message = EmailMessage(
                subject=f'Contact Form Submission from {name}',
                body=f'your message has recieved succeassfully.Your message: {message}',
                from_email=settings.DEFAULT_FROM_EMAIL,  
                to=[email], 
                reply_to=[email]  
            )
            try:
                admin_email_message.send()
                email_message.send()
                success = "Your message has been sent successfully!"
                form = ContactForm()  
            except Exception as e:
                success = f"Failed to send your message. Please try again later. Error: {e}"
        else:
            success = None  
    else:
        form = ContactForm()

    return render(request, 'pages/contactus.html', {'form': form, 'success': success,'categories': categories})