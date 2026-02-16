from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('search/', views.search, name='search'),
    path('signin/', views.signin_view, name='signin'),
    path('signup/', views.signup_view, name='signup'),
    path('signout/', views.signout_view, name='signout'),
    path('profile/', views.profile_view, name='profile'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('save-article/<int:article_id>/', views.save_article, name='save_article'),
    path('remove-saved-article/<int:article_id>/', views.remove_saved_article, name='remove_saved_article'),
    path('like-article/<int:article_id>/', views.like_article, name='like_article'),
]
