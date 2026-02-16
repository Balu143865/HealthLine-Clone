# Healthline Clone - Django Project

A Django-based health and wellness website with a custom admin panel.

## Features

- **Admin Panel**: Custom admin dashboard for managing articles, categories, newsletters, and users
- **Frontend Website**: Public-facing health and wellness content
- **User Authentication**: Sign up, sign in, and profile management
- **Article Management**: Create, edit, and publish health articles
- **Newsletter Subscription**: Email subscription functionality
- **Responsive Design**: Mobile-friendly interface

## Deployment on Render

### Prerequisites

1. A [Render](https://render.com) account
2. A GitHub repository with this code

### Deployment Steps

1. **Push to GitHub**: Push this code to a GitHub repository

2. **Create a new Web Service on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Select the repository containing this project

3. **Configure the Web Service**:
   - **Name**: healthline-clone (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn healthline.wsgi`
   - **Instance Type**: Free (or paid for better performance)

4. **Set Environment Variables**:
   - `SECRET_KEY`: Generate a secure secret key
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: `.onrender.com`
   - `DJANGO_SUPERUSER_USERNAME`: admin
   - `DJANGO_SUPERUSER_EMAIL`: your-email@example.com
   - `DJANGO_SUPERUSER_PASSWORD`: A secure password

5. **Deploy**: Click "Create Web Service"

### Accessing Your Deployed Site

After deployment, your site will be available at:
- **Admin Panel**: `https://your-app-name.onrender.com/admin/`
- **Frontend Website**: `https://your-app-name.onrender.com/site/`

### Default Admin Credentials

The superuser account will be created automatically during deployment using the environment variables you set.

## Local Development

### Prerequisites

- Python 3.9+
- pip

### Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd Clone-Django
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Import articles:
   ```bash
   python manage.py import_articles
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the site:
   - Admin Panel: http://127.0.0.1:8000/admin/
   - Frontend: http://127.0.0.1:8000/site/

## Project Structure

```
Clone-Django/
├── admin_panel/          # Custom admin panel app
├── core/                 # Main frontend app
├── healthline/           # Django project settings
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── media/                # User-uploaded files
├── requirements.txt      # Python dependencies
├── Procfile              # For production deployment
├── render.yaml           # Render deployment config
└── build.sh              # Build script for deployment
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode (True/False) | No (default: True) |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | No (default: *) |
| `DATABASE_URL` | PostgreSQL database URL | No (uses SQLite) |
| `DJANGO_SUPERUSER_USERNAME` | Admin username | For deployment |
| `DJANGO_SUPERUSER_EMAIL` | Admin email | For deployment |
| `DJANGO_SUPERUSER_PASSWORD` | Admin password | For deployment |

## License

This project is for educational purposes.
