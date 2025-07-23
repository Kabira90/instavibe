

from .models import Post, Story, Follow
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from .forms import ProfileForm, PostForm
from .models import Profile
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import StoryForm
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from .models import Message

from .models import models
from .models import Notification

from .models import Highlight

from .forms import HighlightForm



# =============================
# Auth & Signup Views
# =============================

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# =============================
# Profile Views
# =============================

@login_required
def profile_update(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_update')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'insta/profile_update.html', {'form': form})


@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=profile_user).order_by('-created_at')
    highlights = Highlight.objects.filter(user=profile_user)


    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()

    context = {
        'profile_user': profile_user,
        'highlights': highlights,
        'posts': posts,
        'is_following': is_following,
        'followers_count': followers_count,
        'following_count': following_count,
    }
    return render(request, 'insta/user_profile.html', context)


@login_required
def follow_toggle(request, username):
    target_user = get_object_or_404(User, username=username)
    
    if target_user == request.user:
        return redirect('user_profile', username=username)

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=target_user
    )

    if not created:
        follow.delete()

    return redirect('user_profile', username=username)


# =============================
# Post Views
# =============================



@login_required
def home_view(request):
    posts = Post.objects.all().order_by('-created_at')

    # DEBUG: Show who the current user follows
    following_ids = request.user.following.values_list('following_id', flat=True)
    print("User is following IDs:", list(following_ids))

    # Include your own ID
    all_user_ids = list(following_ids) + [request.user.id]
    print("Fetching stories for user IDs:", all_user_ids)

    stories = Story.objects.filter(user_id__in=all_user_ids).order_by('-created_at')

    context = {
        'posts': posts,
        'stories': stories,
    }
    return render(request, 'insta/home.html', context)




@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'insta/create_post.html', {'form': form})


@login_required
def reels_view(request):
    reels = Post.objects.filter(video__isnull=False).order_by('-created_at')
    return render(request, 'insta/reels.html', {'reels': reels})









@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    
    post.delete()
    return redirect('user_profile', request.user.username)


# =============================
# Optional function-Based View
# =============================
@login_required
def post_list_view(request):
    posts = Post.objects.all().order_by('-created_at')  # You can adjust ordering if needed
    return render(request, 'insta/post_list.html', {'posts': posts})



@login_required
def add_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('home')  # Change to your desired redirect
    else:
        form = StoryForm()
    
    return render(request, 'insta/add_story.html', {'form': form})




@login_required
def story_detail_view(request, story_id):
    story = get_object_or_404(Story, id=story_id)

    # Only show if story is fresh (within 24 hours)
    if timezone.now() - story.created_at > timedelta(hours=24):
        return HttpResponseForbidden("This story has expired.")

    return render(request, 'insta/story_detail.html', {'story': story})
    


@login_required
def search_users(request):
    query = request.GET.get('q')
    users = []

    if query:
        users = User.objects.filter(Q(username__icontains=query)).exclude(username=request.user.username)

    return render(request, 'insta/search_results.html', {'users': users, 'query': query})






@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'insta/post_detail.html', {'post': post})







@login_required
def explore(request):
    posts = Post.objects.filter(
        Q(image__isnull=False) | Q(video__isnull=False)
    ).order_by('-created_at')
    return render(request, 'insta/explore.html', {'posts': posts})






@login_required
def inbox(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'insta/inbox.html', {'users': users})

@login_required
def conversation(request, user_id):
    user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        (models.Q(sender=request.user, receiver=user) |
         models.Q(sender=user, receiver=request.user))
    ).order_by('timestamp')
    return render(request, 'insta/conversation.html', {'messages': messages, 'receiver': user})

@login_required
def send_message(request, user_id):
    if request.method == 'POST':
        receiver = get_object_or_404(User, id=user_id)
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
        return redirect('conversation', user_id=user_id)
    





@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    post.likes.add(user)
    
    # Create notification if not self-like
    if post.user != user:
        Notification.objects.create(
            sender=user,
            receiver=post.user,
            type='like',
            post=post
        )
    return redirect('post_detail', post_id=post_id)






@login_required
def notifications(request):
    notes = Notification.objects.filter(receiver=request.user).order_by('-created_at')
    return render(request, 'insta/notifications.html', {'notifications': notes})





@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)  # Unlike
    else:
        post.likes.add(user)  # Like

        # ✅ Add notification (optional)
        if post.user != user:
            Notification.objects.create(
                sender=user,
                receiver=post.user,
                type='like',
                post=post
            )

    return redirect('post_detail', post_id=post_id)





@login_required
def highlight_detail(request, highlight_id):
    highlight = get_object_or_404(Highlight, id=highlight_id)
    stories = highlight.stories.all()  # ✅ Fetch related stories

    return render(request, 'insta/highlight_detail.html', {
        'highlight': highlight,
        'stories': stories
    })




@login_required
def create_highlight(request):
    if request.method == 'POST':
        form = HighlightForm(request.POST, request.FILES)
        if form.is_valid():
            highlight = form.save(commit=False)
            highlight.user = request.user
            highlight.save()
            form.save_m2m()  # for ManyToManyField
            return redirect('user_profile', request.user.username)
    else:
        form = HighlightForm()

    return render(request, 'insta/create_highlight.html', {'form': form})
