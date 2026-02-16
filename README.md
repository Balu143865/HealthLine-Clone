# Healthline Clone - Django Web Application

A full-featured health and wellness web application built with Django 4.2, featuring a modern responsive frontend and a comprehensive admin panel with data visualization.

![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technical Implementation](#technical-implementation)
- [Setup Instructions](#setup-instructions)
- [Deployment](#deployment)
- [Changelog](#changelog)
- [Contributing](#contributing)

---

## Project Overview

Healthline Clone is a comprehensive health information platform that allows users to browse health articles across multiple categories, save articles for later reading, like articles, subscribe to newsletters, and manage their profiles. The application includes a custom-built admin panel with dashboard analytics and data visualization.

### Architecture

```
├── healthline/           # Django project settings
├── core/                 # Main frontend application
├── admin_panel/          # Custom admin panel
├── templates/            # HTML templates
├── static/               # CSS, JS, images
├── media/                # User uploaded files
└── manage.py
```

---

## Key Features

### Frontend Features

- **🏠 Home Page**: Featured articles, trending content, category navigation
- **📚 Article Categories**: Nutrition, Fitness, Mental Health, Wellness, Conditions, Lifestyle
- **📖 Article Detail**: Full article view with related articles
- **🔍 Search**: Full-text search across articles
- **👤 User Authentication**: Sign up, Sign in, Sign out
- **📋 User Profile**: View saved and liked articles, upload profile photo
- **❤️ Like Articles**: Like/unlike articles with real-time counter
- **🔖 Save Articles**: Save articles for later reading
- **📧 Newsletter**: Email subscription for updates
- **📱 Responsive Design**: Mobile-first responsive layout

### Admin Panel Features

- **📊 Dashboard Analytics**: 
  - Total articles, categories, users, newsletter subscribers
  - Articles by Category (Doughnut chart)
  - Articles Published Over Time (Line chart)
  - Article Status Distribution (Pie chart)
  - Top Viewed Articles (Line graph with trend analysis)
- **📝 Article Management**: Create, Read, Update, Delete articles
- **📁 Category Management**: Manage article categories
- **📧 Newsletter Management**: View and manage subscribers
- **👥 User Management**: View registered users
- **🔐 Secure Authentication**: Admin-only access with session management
- **📱 Mobile Responsive**: Bottom navigation for mobile devices

---

## Technical Implementation

### Technology Stack

| Component | Technology |
|-----------|------------|
| Backend Framework | Django 4.2 LTS |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | HTML5, CSS3, JavaScript |
| CSS Framework | Custom CSS with CSS Variables |
| Charts | Chart.js |
| WSGI Server | Gunicorn |
| Static Files | WhiteNoise |
| Deployment | Render.com |

### Django Apps

1. **core** - Frontend application
   - Models: Article, Category, SubCategory, Newsletter, UserProfile
   - Views: Home, Category, Article Detail, Search, Auth, Profile
   - Management Commands: `import_articles`, `create_admin`

2. **admin_panel** - Admin panel application
   - Views: Dashboard, Article CRUD, Category CRUD, Newsletter List, User List
   - Custom authentication and authorization

### Models

```python
# Category Model
- name, slug, description, image, image_url, order

# Article Model  
- title, slug, excerpt, content, image, image_url
- category, subcategory, author, read_time
- views, likes, is_featured, is_trending
- status (draft/published), created_at, updated_at

# Newsletter Model
- email, subscribed_at, is_active

# UserProfile Model
- user, avatar, profile_photo
- saved_articles (ManyToMany), liked_articles (ManyToMany)
```

### URL Structure

```
/site/                    # Frontend
/site/article/<slug>/     # Article detail
/site/category/<slug>/    # Category page
/site/search/             # Search results
/site/signin/             # Sign in
/site/signup/             # Sign up
/site/profile/            # User profile

/admin/                   # Admin panel
/admin/dashboard/         # Dashboard
/admin/articles/          # Article management
/admin/categories/        # Category management
/admin/newsletters/       # Newsletter subscribers
```

---

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Balu143865/HealthLine-Clone.git
   cd HealthLine-Clone
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Import articles data**
   ```bash
   python manage.py import_articles
   ```

6. **Create superuser**
   ```bash
   python manage.py create_admin --username admin --password admin123 --email admin@example.com
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Frontend: http://127.0.0.1:8000/site/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - Django Admin: http://127.0.0.1:8000/django-admin/

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=your-password
```

---

## Deployment

### Render.com Deployment

1. **Push code to GitHub**

2. **Create new Web Service on Render**
   - Connect your GitHub repository
   - Set build command: `./build.sh`
   - Set start command: `gunicorn healthline.wsgi`

3. **Set Environment Variables**
   ```
   PYTHON_VERSION=3.11.0
   SECRET_KEY=<generate>
   DEBUG=False
   ALLOWED_HOSTS=.onrender.com
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@example.com
   DJANGO_SUPERUSER_PASSWORD=<generate>
   CSRF_TRUSTED_ORIGINS=https://*.onrender.com
   ```

4. **Deploy**
   - Render will automatically deploy
   - Access at: `https://your-app.onrender.com`

### Creating Admin User on Render

Use the Render Shell:
```bash
python manage.py create_admin --username admin --password YourPassword123!
```

---

## Changelog

### Version 1.0.0 (February 2026)

#### Initial Release
- ✅ Django 4.2 project structure
- ✅ Article and Category models
- ✅ User authentication system
- ✅ Frontend responsive design
- ✅ Custom admin panel

#### Recent Updates

**Dashboard Visualization Improvements**
- 📊 Changed "Top Viewed Articles" from horizontal bar chart to line graph
- 📈 Added trend analysis with smooth curves and filled areas
- 📱 Improved mobile responsiveness for all charts
- 🎨 Added responsive font sizing and label truncation

**Frontend URL Routing Fixes**
- 🔧 Fixed like/save article button URLs to include `/site/` prefix
- 🔧 Corrected AJAX endpoints for proper routing
- ✅ Verified functionality on both local and production environments

**Admin Panel Mobile Improvements**
- 📱 Fixed horizontal overflow issues
- 📱 Added bottom navigation bar for mobile devices
- 📱 Improved touch targets and spacing
- 📱 Responsive chart containers

**Deployment Configuration**
- 🚀 Updated to Django 4.2 for Python 3.11+ compatibility
- 🚀 Updated gunicorn to 23.0.0 for Python 3.12+ support
- 🚀 Added `create_admin` management command
- 🚀 Configured CSRF_TRUSTED_ORIGINS for production
- 🚀 Removed deprecated `USE_L10N` setting

**CSS Compatibility Fixes**
- 🎨 Replaced `-webkit-overflow-scrolling` with `overscroll-behavior-x`
- 🎨 Fixed Microsoft Edge Tools warnings

---

## Project Structure

```
HealthLine-Clone/
├── healthline/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   ├── management/
│   │   └── commands/
│   │       ├── import_articles.py
│   │       └── create_admin.py
│   └── migrations/
├── admin_panel/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── migrations/
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── article_detail.html
│   ├── category.html
│   ├── profile.html
│   ├── search_results.html
│   ├── signin.html
│   ├── signup.html
│   └── admin_panel/
│       ├── base.html
│       ├── dashboard.html
│       ├── article_list.html
│       ├── article_form.html
│       ├── category_list.html
│       ├── category_form.html
│       ├── newsletter_list.html
│       └── user_list.html
├── static/
│   ├── css/
│   │   ├── styles.css
│   │   ├── components.css
│   │   ├── responsive.css
│   │   └── admin.css
│   ├── js/
│   │   ├── main.js
│   │   └── search.js
│   └── images/
│       └── articles/
├── media/
├── requirements.txt
├── runtime.txt
├── Procfile
├── render.yaml
├── build.sh
└── README.md
```

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Design inspired by [Healthline.com](https://www.healthline.com)
- Chart.js for data visualization
- Django framework and community

---

## Contact

- GitHub: [@Balu143865](https://github.com/Balu143865)
- Repository: [HealthLine-Clone](https://github.com/Balu143865/HealthLine-Clone)
