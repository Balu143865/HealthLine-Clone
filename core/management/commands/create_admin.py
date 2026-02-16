from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Create a superuser admin account'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Admin username')
        parser.add_argument('--email', type=str, help='Admin email')
        parser.add_argument('--password', type=str, help='Admin password')

    def handle(self, *args, **options):
        username = options.get('username') or os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = options.get('email') or os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = options.get('password') or os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123456')

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists.')
            )
            # Update password if user exists
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Password updated for user "{username}".')
            )
        else:
            # Create new superuser
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully!')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nLogin credentials:\n  Username: {username}\n  Password: {password}\n  Email: {email}')
        )
