from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect,HttpResponseBadRequest
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .forms import PostForm
from .models import User,Newpost,Like
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


@login_required
def index(request):
    newpost = Newpost.objects.all().order_by('-date')
    liked_posts = Like.objects.filter(user=request.user).values_list('post', flat=True)
    paginator= Paginator(newpost,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()  
            return redirect('index')
    else:
        form = PostForm()

    context = {
        'page_obj':page_obj,
        'form': form,
        'newpost':newpost,
        'liked_posts':liked_posts
        }
    return render(request, 'network/index.html', context)

@login_required
@require_POST
def update_post(request, post_id):
    if request.is_ajax():
        try:
            post = Newpost.objects.get(id=post_id, user=request.user)
            new_text = request.POST.get('text')
            post.text = new_text
            post.save()

            return JsonResponse({'status': 'success'})
        except Newpost.DoesNotExist:
            return JsonResponse({'status': 'error'})

    # Return an error response if the request is not AJAX
    return HttpResponseBadRequest("Bad Request: This view requires an AJAX request.")


@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile=profile_user.profile
    posts = Newpost.objects.filter(user=profile_user).order_by('-date')
    print(f'username: {username}')
    context = {
        'profile_user': profile_user,
        'user_profile':profile,
        'posts': posts,
    }
    return render(request, 'network/userprofile.html', context)



@login_required
def follow_toggle(request):
    if request.method == 'POST' and request.user.is_authenticated:
        username = request.POST.get('username')
        user_to_follow = get_object_or_404(User, username=username)
        user_profile = request.user.profile

        if user_to_follow in user_profile.followers.all():
            user_profile.followers.remove(user_to_follow)
        else:
            user_profile.followers.add(user_to_follow)
        
        return redirect('user_profile', username=username)


@login_required
def following_posts(request):
    followed_users = request.user.profile.followers.all()
    posts = Newpost.objects.filter(user__profile__user__in=followed_users)
    
    context = {'posts': posts}
    return render(request, 'network/following_posts.html', context)

@login_required
def like_toggle(request):
    if request.method == 'POST' and request.user.is_authenticated:
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Newpost, id=post_id)
        user = request.user

        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            action = 'unliked'
        except Like.DoesNotExist:
            Like.objects.create(user=user, post=post)
            action = 'liked'

        response = {'action': action, 'like_count': post.like_count()}
        print(response)
        return JsonResponse(response)

@login_required
def update_post(request, post_id):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        new_text = request.POST.get('new_text')
        try:
            post = Newpost.objects.get(id=post_id, user=request.user)
            post.text = new_text
            post.save()
            return JsonResponse({'success': True})
        except Newpost.DoesNotExist:
            return JsonResponse({'success': False})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
