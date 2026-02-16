"""
Custom Admin Panel Views
Modern admin interface for managing content
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from core.models import Category, SubCategory, Article, Newsletter, UserProfile


def is_staff_user(user):
    """Check if user is staff"""
    return user.is_authenticated and user.is_staff


def staff_required(login_url=None):
    """Custom decorator that redirects to admin login if not authenticated"""
    def decorator(view_func):
        from functools import wraps
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # Store the attempted URL
                request.session['admin_next_url'] = request.get_full_path()
                return redirect(reverse('admin_panel:login'))
            if not request.user.is_staff:
                messages.error(request, 'You do not have permission to access the admin panel.')
                return redirect(reverse('core:home'))
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# Admin Login View
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def admin_login(request):
    """Custom admin login page"""
    # If already logged in as staff, redirect to dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel:dashboard')
    
    # If logged in but not staff, show error
    if request.user.is_authenticated and not request.user.is_staff:
        messages.error(request, 'You do not have permission to access the admin panel.')
        return redirect('core:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect to next URL if stored
            next_url = request.session.pop('admin_next_url', None)
            if next_url:
                return redirect(next_url)
            return redirect('admin_panel:dashboard')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'admin_panel/login.html')


def admin_logout(request):
    """Admin logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('admin_panel:login')


@staff_required()
def dashboard(request):
    """Admin dashboard with statistics"""
    from django.db.models.functions import TruncMonth
    import json
    
    # Basic stats
    total_articles = Article.objects.count()
    total_categories = Category.objects.count()
    total_subcategories = SubCategory.objects.count()
    total_newsletters = Newsletter.objects.filter(is_active=True).count()
    total_users = User.objects.count()
    featured_articles = Article.objects.filter(is_featured=True).count()
    
    # Articles by category for chart
    articles_by_category = Category.objects.annotate(
        article_count=Count('articles')
    ).order_by('-article_count')[:8]
    
    category_names = json.dumps([cat.name for cat in articles_by_category])
    category_counts = [cat.article_count for cat in articles_by_category]
    
    # Articles over time (last 6 months)
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    six_months_ago = timezone.now() - timedelta(days=180)
    articles_by_month = Article.objects.filter(
        created_at__gte=six_months_ago
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    article_months = json.dumps([
        item['month'].strftime('%b %Y') for item in articles_by_month
    ])
    article_counts_by_month = [item['count'] for item in articles_by_month]
    
    # Article status counts
    published_count = Article.objects.filter(status='published').count()
    draft_count = Article.objects.filter(status='draft').count()
    
    # Top viewed articles
    top_articles = Article.objects.order_by('-views')[:5]
    top_articles_titles = json.dumps([article.title[:30] + '...' if len(article.title) > 30 else article.title for article in top_articles])
    top_articles_views = [article.views for article in top_articles]
    
    context = {
        'total_articles': total_articles,
        'total_categories': total_categories,
        'total_subcategories': total_subcategories,
        'total_newsletters': total_newsletters,
        'total_users': total_users,
        'featured_articles': featured_articles,
        'recent_articles': Article.objects.order_by('-created_at')[:5],
        'recent_newsletters': Newsletter.objects.order_by('-subscribed_at')[:5],
        'articles_by_category': articles_by_category,
        
        # Chart data
        'category_names': category_names,
        'category_counts': category_counts,
        'article_months': article_months,
        'article_counts_by_month': article_counts_by_month,
        'published_count': published_count,
        'draft_count': draft_count,
        'top_articles_titles': top_articles_titles,
        'top_articles_views': top_articles_views,
    }
    return render(request, 'admin_panel/dashboard.html', context)


# Category CRUD
@staff_required()
def category_list(request):
    """List all categories"""
    categories = Category.objects.annotate(article_count=Count('articles')).order_by('order')
    
    paginator = Paginator(categories, 10)
    page = request.GET.get('page')
    categories = paginator.get_page(page)
    
    context = {
        'categories': categories,
        'total_count': Category.objects.count(),
    }
    return render(request, 'admin_panel/category_list.html', context)


@staff_required()
def category_create(request):
    """Create new category"""
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug') or slugify(name)
        description = request.POST.get('description', '')
        image_url = request.POST.get('image_url', '')
        order = request.POST.get('order', 0)
        
        if Category.objects.filter(slug=slug).exists():
            messages.error(request, 'A category with this slug already exists.')
        else:
            category = Category.objects.create(
                name=name,
                slug=slug,
                description=description,
                image_url=image_url,
                order=order
            )
            
            # Handle image upload
            if request.FILES.get('image_upload'):
                category.image = request.FILES['image_upload']
                category.save()
            
            messages.success(request, f'Category "{category.name}" created successfully.')
            return redirect('admin_panel:category_list')
    
    return render(request, 'admin_panel/category_form.html', {'action': 'Create'})


@staff_required()
def category_edit(request, slug):
    """Edit category"""
    category = get_object_or_404(Category, slug=slug)
    
    if request.method == 'POST':
        category.name = request.POST.get('name', category.name)
        new_slug = request.POST.get('slug') or slugify(category.name)
        category.description = request.POST.get('description', '')
        category.image_url = request.POST.get('image_url', '')
        category.order = request.POST.get('order', 0)
        
        # Handle image upload
        if request.FILES.get('image_upload'):
            category.image = request.FILES['image_upload']
        
        if new_slug != category.slug and Category.objects.filter(slug=new_slug).exists():
            messages.error(request, 'A category with this slug already exists.')
        else:
            category.slug = new_slug
            category.save()
            messages.success(request, f'Category "{category.name}" updated successfully.')
            return redirect('admin_panel:category_list')
    
    return render(request, 'admin_panel/category_form.html', {
        'category': category,
        'action': 'Edit'
    })


@staff_required()
def category_delete(request, slug):
    """Delete category"""
    category = get_object_or_404(Category, slug=slug)
    
    if request.method == 'POST':
        article_count = category.article_set.count()
        if article_count > 0:
            messages.error(request, f'Cannot delete category with {article_count} articles. Move or delete articles first.')
        else:
            category.delete()
            messages.success(request, f'Category "{category.name}" deleted successfully.')
        return redirect('admin_panel:category_list')
    
    return render(request, 'admin_panel/category_confirm_delete.html', {'category': category})


# Article CRUD
@staff_required()
def article_list(request):
    """List all articles with filters"""
    articles = Article.objects.select_related('category').all()
    
    # Filters
    category_filter = request.GET.get('category')
    status_filter = request.GET.get('status')
    search = request.GET.get('search')
    
    if category_filter:
        articles = articles.filter(category__slug=category_filter)
    if status_filter:
        articles = articles.filter(status=status_filter)
    if search:
        articles = articles.filter(title__icontains=search)
    
    articles = articles.order_by('-created_at')
    
    paginator = Paginator(articles, 15)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    
    context = {
        'articles': articles,
        'categories': Category.objects.all(),
        'total_count': Article.objects.count(),
    }
    return render(request, 'admin_panel/article_list.html', context)


@staff_required()
def article_create(request):
    """Create new article"""
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug') or slugify(title)
        excerpt = request.POST.get('excerpt', '')
        content = request.POST.get('content', '')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        author = request.POST.get('author', 'Healthline Team')
        image_url = request.POST.get('image_url', '')
        read_time = request.POST.get('read_time', 5)
        is_featured = request.POST.get('is_featured') == 'on'
        is_trending = request.POST.get('is_trending') == 'on'
        status = request.POST.get('status', 'published')
        
        if Article.objects.filter(slug=slug).exists():
            messages.error(request, 'An article with this slug already exists.')
        else:
            category = Category.objects.get(id=category_id) if category_id else None
            subcategory = SubCategory.objects.get(id=subcategory_id) if subcategory_id else None
            
            article = Article.objects.create(
                title=title,
                slug=slug,
                excerpt=excerpt,
                content=content,
                category=category,
                subcategory=subcategory,
                author=author,
                image_url=image_url,
                read_time=read_time,
                is_featured=is_featured,
                is_trending=is_trending,
                status=status
            )
            
            # Handle image upload
            if request.FILES.get('image_upload'):
                article.image = request.FILES['image_upload']
                article.save()
            
            messages.success(request, f'Article "{article.title}" created successfully.')
            return redirect('admin_panel:article_list')
    
    context = {
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        'action': 'Create'
    }
    return render(request, 'admin_panel/article_form.html', context)


@staff_required()
def article_edit(request, slug):
    """Edit article"""
    article = get_object_or_404(Article, slug=slug)
    
    if request.method == 'POST':
        article.title = request.POST.get('title', article.title)
        new_slug = request.POST.get('slug') or slugify(article.title)
        article.excerpt = request.POST.get('excerpt', '')
        article.content = request.POST.get('content', '')
        
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        
        article.category = Category.objects.get(id=category_id) if category_id else None
        article.subcategory = SubCategory.objects.get(id=subcategory_id) if subcategory_id else None
        
        article.author = request.POST.get('author', 'Healthline Team')
        article.image_url = request.POST.get('image_url', '')
        article.read_time = request.POST.get('read_time', 5)
        article.is_featured = request.POST.get('is_featured') == 'on'
        article.is_trending = request.POST.get('is_trending') == 'on'
        article.status = request.POST.get('status', 'published')
        
        # Handle image upload
        if request.FILES.get('image_upload'):
            article.image = request.FILES['image_upload']
        
        if new_slug != article.slug and Article.objects.filter(slug=new_slug).exists():
            messages.error(request, 'An article with this slug already exists.')
        else:
            article.slug = new_slug
            article.save()
            messages.success(request, f'Article "{article.title}" updated successfully.')
            return redirect('admin_panel:article_list')
    
    context = {
        'article': article,
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        'action': 'Edit'
    }
    return render(request, 'admin_panel/article_form.html', context)


@staff_required()
def article_delete(request, slug):
    """Delete article"""
    article = get_object_or_404(Article, slug=slug)
    
    if request.method == 'POST':
        article.delete()
        messages.success(request, f'Article "{article.title}" deleted successfully.')
        return redirect('admin_panel:article_list')
    
    return render(request, 'admin_panel/article_confirm_delete.html', {'article': article})


# Newsletter Management
@staff_required()
def newsletter_list(request):
    """List all newsletter subscriptions"""
    newsletters = Newsletter.objects.all().order_by('-subscribed_at')
    
    # Filter
    status_filter = request.GET.get('status')
    if status_filter:
        newsletters = newsletters.filter(is_active=status_filter == 'active')
    
    paginator = Paginator(newsletters, 20)
    page = request.GET.get('page')
    newsletters = paginator.get_page(page)
    
    context = {
        'newsletters': newsletters,
        'total_count': Newsletter.objects.count(),
        'active_count': Newsletter.objects.filter(is_active=True).count(),
    }
    return render(request, 'admin_panel/newsletter_list.html', context)


@staff_required()
def newsletter_toggle(request, pk):
    """Toggle newsletter active status"""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    newsletter.is_active = not newsletter.is_active
    newsletter.save()
    
    status = 'activated' if newsletter.is_active else 'deactivated'
    messages.success(request, f'Subscription {newsletter.email} {status}.')
    return redirect('admin_panel:newsletter_list')


@staff_required()
def newsletter_delete(request, pk):
    """Delete newsletter subscription"""
    newsletter = get_object_or_404(Newsletter, pk=pk)
    email = newsletter.email
    newsletter.delete()
    messages.success(request, f'Subscription {email} deleted.')
    return redirect('admin_panel:newsletter_list')


# User Management
@staff_required()
def user_list(request):
    """List all users"""
    users = User.objects.all().order_by('-date_joined')
    
    paginator = Paginator(users, 15)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    
    context = {
        'users': users,
        'total_count': User.objects.count(),
        'staff_count': User.objects.filter(is_staff=True).count(),
    }
    return render(request, 'admin_panel/user_list.html', context)


@staff_required()
def user_toggle_staff(request, pk):
    """Toggle user staff status"""
    user = get_object_or_404(User, pk=pk)
    
    if user == request.user:
        messages.error(request, 'You cannot modify your own staff status.')
    else:
        user.is_staff = not user.is_staff
        user.save()
        status = 'granted' if user.is_staff else 'revoked'
        messages.success(request, f'Staff access {status} for {user.username}.')
    
    return redirect('admin_panel:user_list')


# API endpoints for dynamic data
@staff_required()
def get_subcategories(request):
    """Get subcategories for a category (AJAX)"""
    category_id = request.GET.get('category_id')
    subcategories = SubCategory.objects.filter(category_id=category_id).values('id', 'name', 'slug')
    return JsonResponse({'subcategories': list(subcategories)})


@staff_required()
def dashboard_stats(request):
    """Get dashboard statistics (AJAX)"""
    stats = {
        'articles': Article.objects.count(),
        'categories': Category.objects.count(),
        'newsletters': Newsletter.objects.filter(is_active=True).count(),
        'users': User.objects.count(),
    }
    return JsonResponse(stats)
