from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
from django import forms
from django.urls import reverse
from .models import Category, Article, Newsletter, UserProfile


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with additional fields"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
        return user


def frontend_login_required(view_func):
    """Decorator that requires frontend login (separate from admin)"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Store the attempted URL
            request.session['frontend_next_url'] = request.get_full_path()
            return redirect(reverse('core:signin'))
        return view_func(request, *args, **kwargs)
    return wrapper


@frontend_login_required
def home(request):
    """Home page view"""
    # Get featured article for hero section
    featured_article = Article.objects.filter(is_featured=True).first()
    
    # Get trending articles (if not enough trending, get most viewed)
    trending_articles = Article.objects.filter(is_trending=True)[:4]
    if trending_articles.count() < 4:
        trending_articles = Article.objects.order_by('-views')[:4]
    
    # Get featured articles for editor's picks
    featured_articles = Article.objects.filter(is_featured=True)[:4]
    if featured_articles.count() < 4:
        featured_articles = Article.objects.all()[:4]
    
    # Get all categories
    categories = Category.objects.all()
    
    context = {
        'featured_article': featured_article,
        'trending_articles': trending_articles,
        'featured_articles': featured_articles,
        'categories': categories,
    }
    return render(request, 'home.html', context)


@frontend_login_required
def category_view(request, slug):
    """Category page view"""
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category)
    
    # Filter by subcategory if provided
    subcategory = request.GET.get('sub')
    if subcategory:
        articles = articles.filter(subcategory__slug=subcategory)
    
    context = {
        'category': category,
        'articles': articles,
        'subcategories': category.subcategories.all(),
    }
    return render(request, 'category.html', context)


@frontend_login_required
def article_detail(request, slug):
    """Article detail page view"""
    article = get_object_or_404(Article, slug=slug)
    
    # Increment view count
    article.views += 1
    article.save(update_fields=['views'])
    
    # Get related articles (4 articles in a row)
    related_articles = Article.objects.filter(
        category=article.category
    ).exclude(id=article.id)[:4]
    
    # Check if article is saved/liked by user
    is_saved = False
    is_liked = False
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            is_saved = article in profile.saved_articles.all()
            is_liked = article in profile.liked_articles.all()
        except:
            pass
    
    context = {
        'article': article,
        'related_articles': related_articles,
        'is_saved': is_saved,
        'is_liked': is_liked,
    }
    return render(request, 'article_detail.html', context)


@frontend_login_required
def search(request):
    """Search results view"""
    query = request.GET.get('q', '')
    articles = []
    categories = Category.objects.all()
    
    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    
    context = {
        'query': query,
        'articles': articles,
        'categories': categories,
        'total_results': articles.count() if query else 0,
    }
    return render(request, 'search_results.html', context)


def signin_view(request):
    """Sign in view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            
            # Redirect to next URL if stored
            next_url = request.session.pop('frontend_next_url', None)
            if next_url:
                return redirect(next_url)
            return redirect('core:home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'signin.html', {'form': form})


def signup_view(request):
    """Sign up view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Healthline!')
            return redirect('core:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})


def signout_view(request):
    """Sign out view"""
    logout(request)
    messages.success(request, 'You have been signed out successfully.')
    return redirect('core:home')


@login_required
def profile_view(request):
    """User profile view"""
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    saved_articles = user_profile.saved_articles.all()
    liked_articles = user_profile.liked_articles.all()
    
    # Handle settings form submission
    if request.method == 'POST':
        # Check if it's a photo upload
        if 'profile_photo' in request.FILES:
            user_profile.profile_photo = request.FILES['profile_photo']
            user_profile.save()
            messages.success(request, 'Profile photo updated successfully!')
            return redirect('core:profile')
        
        # Check if it's a remove photo request
        if request.POST.get('remove_photo') == 'true':
            user_profile.profile_photo.delete()
            user_profile.save()
            messages.success(request, 'Profile photo removed successfully!')
            return redirect('core:profile')
        
        # Regular profile update
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        
        # Update user information
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('core:profile')
    
    context = {
        'profile': user_profile,
        'saved_articles': saved_articles,
        'liked_articles': liked_articles,
    }
    return render(request, 'profile.html', context)


@require_POST
def newsletter_subscribe(request):
    """Newsletter subscription AJAX view"""
    email = request.POST.get('email')
    
    if not email:
        return JsonResponse({'success': False, 'error': 'Email is required'})
    
    # Check if already subscribed
    if Newsletter.objects.filter(email=email, is_active=True).exists():
        return JsonResponse({'success': False, 'error': 'Email already subscribed'})
    
    # Create or reactivate subscription
    newsletter, created = Newsletter.objects.get_or_create(
        email=email,
        defaults={'is_active': True}
    )
    
    if not created:
        newsletter.is_active = True
        newsletter.save()
    
    return JsonResponse({'success': True, 'message': 'Successfully subscribed!'})


@require_POST
@login_required
def save_article(request, article_id):
    """Save/unsave article for user"""
    article = get_object_or_404(Article, id=article_id)
    profile = request.user.profile
    
    if article in profile.saved_articles.all():
        profile.saved_articles.remove(article)
        saved = False
    else:
        profile.saved_articles.add(article)
        saved = True
    
    return JsonResponse({'success': True, 'saved': saved})


@login_required
def remove_saved_article(request, article_id):
    """Remove saved article from user's profile"""
    article = get_object_or_404(Article, id=article_id)
    profile = request.user.profile
    
    if article in profile.saved_articles.all():
        profile.saved_articles.remove(article)
        messages.success(request, 'Article removed from saved list.')
    else:
        messages.error(request, 'Article not found in saved list.')
    
    return redirect('core:profile')


@require_POST
@login_required
def like_article(request, article_id):
    """Like/unlike article for user"""
    article = get_object_or_404(Article, id=article_id)
    profile = request.user.profile
    
    if article in profile.liked_articles.all():
        profile.liked_articles.remove(article)
        article.likes -= 1
        liked = False
    else:
        profile.liked_articles.add(article)
        article.likes += 1
        liked = True
    
    article.save(update_fields=['likes'])
    
    return JsonResponse({'success': True, 'liked': liked, 'likes_count': article.likes})
