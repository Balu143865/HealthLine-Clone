# Healthline Clone

A static website clone similar to Healthline.com, built with HTML, CSS, and JavaScript.

## Features

- **Homepage** with hero section, trending articles, and category previews
- **6 Category Pages** (Nutrition, Fitness, Mental Health, Wellness, Conditions, Lifestyle)
- **Article Detail Pages** with full content, author info, and related articles
- **Search Functionality** with JSON-based article filtering
- **Responsive Design** for desktop, tablet, and mobile devices
- **Newsletter Signup** forms throughout the site

## Project Structure

```
healthline-clone/
├── index.html                 # Homepage
├── css/
│   ├── styles.css            # Main stylesheet with design system
│   ├── components.css        # Reusable component styles
│   └── responsive.css        # Media queries for all devices
├── js/
│   ├── main.js               # Core JavaScript functionality
│   └── search.js             # Search and filtering logic
├── data/
│   └── articles.json         # Article database (36 articles)
├── images/
│   ├── favicon.svg           # Site favicon
│   └── placeholder.svg       # Placeholder image
├── pages/
│   ├── search-results.html   # Search results page
│   ├── categories/
│   │   ├── nutrition.html
│   │   ├── fitness.html
│   │   ├── mental-health.html
│   │   ├── wellness.html
│   │   ├── conditions.html
│   │   └── lifestyle.html
│   └── articles/
│       ├── benefits-of-green-tea.html
│       ├── hiit-workouts-beginners-guide.html
│       ├── managing-anxiety-strategies.html
│       ├── sleep-hygiene-tips-better-rest.html
│       └── ... (more articles)
└── README.md
```

## Design System

### Colors
- **Primary Green**: #00A86B
- **Secondary Blue**: #1E6B8C
- **Dark Text**: #1F1F1F
- **Light Text**: #666666
- **Background**: #FFFFFF
- **Light Gray**: #F5F5F5

### Typography
- **Headings**: Georgia, serif
- **Body**: Arial, sans-serif

### Breakpoints
- **Desktop**: > 1024px
- **Tablet**: 768px - 1024px
- **Mobile**: < 768px

## Getting Started

1. Clone or download this repository
2. Open `index.html` in a web browser
3. Navigate through the site using the menu links

For the best experience, use a local web server:

```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx serve
```

Then open `http://localhost:8000` in your browser.

## Features Implemented

### Navigation
- Sticky header with scroll shadow effect
- Dropdown menus for category subcategories
- Mobile hamburger menu with slide-out navigation
- Search toggle with autocomplete suggestions

### Homepage
- Hero section with featured article
- Trending articles grid
- Category cards with icons
- Editor's picks section
- Newsletter signup

### Category Pages
- Category header with description
- Subcategory filter tabs
- Article grid with filtering
- Newsletter signup

### Article Pages
- Breadcrumb navigation
- Author information box
- Key takeaways highlight
- Full article content
- Related articles section
- Tags for related topics

### Search
- Real-time search suggestions
- JSON-based article indexing
- Search results page with highlighting
- Category filtering in results

### Responsive Design
- Fluid typography and spacing
- Collapsible navigation
- Adaptive grid layouts
- Touch-friendly interactions

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Notes

- This is a demo/educational project
- Article content is placeholder text
- Images use placeholder SVGs
- No backend functionality (forms don't submit)

## License

This project is for educational purposes only. Not intended for commercial use.

---

Built with ❤️ as a learning exercise in front-end web development.