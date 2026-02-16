"""
Management command to import articles from articles.json
"""
import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import Category, SubCategory, Article


class Command(BaseCommand):
    help = 'Import articles from articles.json into the database'

    def handle(self, *args, **options):
        # Path to articles.json
        json_path = os.path.join(settings.BASE_DIR, 'healthline-clone', 'data', 'articles.json')
        
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'File not found: {json_path}'))
            return
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        articles = data.get('articles', [])
        
        # Track created items
        categories_created = 0
        subcategories_created = 0
        articles_created = 0
        articles_updated = 0
        
        for article_data in articles:
            # Create or get category
            category_slug = article_data.get('category', 'uncategorized')
            category_name = category_slug.replace('-', ' ').title()
            
            category, created = Category.objects.get_or_create(
                slug=category_slug,
                defaults={'name': category_name}
            )
            if created:
                categories_created += 1
            
            # Create or get subcategory
            subcategory_slug = article_data.get('subcategory', '')
            if subcategory_slug:
                subcategory_name = subcategory_slug.replace('-', ' ').title()
                subcategory, created = SubCategory.objects.get_or_create(
                    slug=subcategory_slug,
                    category=category,
                    defaults={'name': subcategory_name}
                )
                if created:
                    subcategories_created += 1
            else:
                subcategory = None
            
            # Get image URL directly from articles.json (Unsplash URLs)
            image_url = article_data.get('image', '')
            slug = article_data.get('slug', '')
            
            # Parse read time
            read_time_str = article_data.get('readTime', '5 min read')
            read_time = int(''.join(filter(str.isdigit, read_time_str)) or 5)
            
            # Create or update article
            article, created = Article.objects.update_or_create(
                slug=slug,
                defaults={
                    'title': article_data.get('title', 'Untitled'),
                    'excerpt': article_data.get('excerpt', ''),
                    'content': article_data.get('content', ''),
                    'category': category,
                    'subcategory': subcategory,
                    'author': article_data.get('author', 'Healthline Team'),
                    'image_url': image_url,  # Use Unsplash URL from JSON
                    'read_time': read_time,
                    'is_featured': article_data.get('featured', False),
                    'is_trending': False,
                }
            )
            
            if created:
                articles_created += 1
            else:
                articles_updated += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Import complete!\n'
            f'  Categories created: {categories_created}\n'
            f'  Subcategories created: {subcategories_created}\n'
            f'  Articles created: {articles_created}\n'
            f'  Articles updated: {articles_updated}'
        ))
