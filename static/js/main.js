/**
 * Healthline Clone - Main JavaScript
 * Handles navigation, mobile menu, and general functionality
 */

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
  initHeader();
  initMobileMenu();
  initSearch();
  initDropdowns();
  initSmoothScroll();
  initLazyLoading();
  initAuthState();
});

/**
 * Header scroll behavior
 */
function initHeader() {
  const header = document.querySelector('.header');
  if (!header) return;

  let lastScroll = 0;
  const scrollThreshold = 50;

  window.addEventListener('scroll', function() {
    const currentScroll = window.pageYOffset;

    // Add shadow on scroll
    if (currentScroll > scrollThreshold) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }

    lastScroll = currentScroll;
  });
}

/**
 * Mobile menu toggle
 */
function initMobileMenu() {
  const menuToggle = document.querySelector('.mobile-menu-toggle');
  const mobileNav = document.querySelector('.mobile-nav');
  const body = document.body;

  if (!menuToggle || !mobileNav) return;

  menuToggle.addEventListener('click', function() {
    menuToggle.classList.toggle('active');
    mobileNav.classList.toggle('active');
    body.classList.toggle('menu-open');
  });

  // Close menu when clicking outside
  document.addEventListener('click', function(e) {
    if (!menuToggle.contains(e.target) && !mobileNav.contains(e.target)) {
      menuToggle.classList.remove('active');
      mobileNav.classList.remove('active');
      body.classList.remove('menu-open');
    }
  });

  // Mobile submenu toggles
  const submenuToggles = document.querySelectorAll('.mobile-nav-toggle');
  submenuToggles.forEach(toggle => {
    toggle.addEventListener('click', function(e) {
      e.preventDefault();
      const parent = this.closest('.mobile-nav-item');
      parent.classList.toggle('expanded');
    });
  });
}

/**
 * Search functionality
 */
function initSearch() {
  const searchToggle = document.querySelector('.header-search-toggle');
  const searchContainer = document.querySelector('.header-search');
  const searchInput = document.querySelector('.header-search-input');

  if (searchToggle && searchContainer) {
    searchToggle.addEventListener('click', function() {
      searchContainer.classList.toggle('active');
      if (searchContainer.classList.contains('active') && searchInput) {
        searchInput.focus();
      }
    });

    // Close search on escape
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        searchContainer.classList.remove('active');
      }
    });
  }

  // Search form submission - let Django handle the form submission
  // Forms have action attribute pointing to Django URL
}

/**
 * Dropdown menus
 */
function initDropdowns() {
  const dropdownItems = document.querySelectorAll('.nav-item');

  dropdownItems.forEach(item => {
    const dropdown = item.querySelector('.nav-dropdown');
    if (!dropdown) return;

    // Keyboard accessibility
    const links = dropdown.querySelectorAll('.nav-dropdown-link');
    const parentLink = item.querySelector('.nav-link');

    parentLink.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        dropdown.classList.toggle('show');
      }
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        links[0]?.focus();
      }
    });

    links.forEach((link, index) => {
      link.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          links[index + 1]?.focus();
        }
        if (e.key === 'ArrowUp') {
          e.preventDefault();
          if (index === 0) {
            parentLink.focus();
          } else {
            links[index - 1]?.focus();
          }
        }
        if (e.key === 'Escape') {
          dropdown.classList.remove('show');
          parentLink.focus();
        }
      });
    });
  });
}

/**
 * Smooth scroll for anchor links
 */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href === '#') return;

      e.preventDefault();
      const target = document.querySelector(href);
      if (target) {
        const headerHeight = document.querySelector('.header')?.offsetHeight || 0;
        const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - headerHeight;

        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });
}

/**
 * Lazy loading for images
 */
function initLazyLoading() {
  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const image = entry.target;
          if (image.dataset.src) {
            image.src = image.dataset.src;
            image.removeAttribute('data-src');
          }
          if (image.dataset.srcset) {
            image.srcset = image.dataset.srcset;
            image.removeAttribute('data-srcset');
          }
          image.classList.remove('lazy');
          observer.unobserve(image);
        }
      });
    });

    document.querySelectorAll('img.lazy').forEach(img => {
      imageObserver.observe(img);
    });
  } else {
    // Fallback for browsers without IntersectionObserver
    document.querySelectorAll('img.lazy').forEach(img => {
      if (img.dataset.src) img.src = img.dataset.src;
      if (img.dataset.srcset) img.srcset = img.dataset.srcset;
    });
  }
}

/**
 * Newsletter form handling
 */
function handleNewsletterSubmit(form) {
  const email = form.querySelector('input[type="email"]').value;
  const button = form.querySelector('button');
  const originalText = button.textContent;
  const csrfToken = form.querySelector('[name="csrfmiddlewaretoken"]');

  // Show loading state
  button.textContent = 'Subscribing...';
  button.disabled = true;

  // Send AJAX request to subscribe
  fetch('/newsletter/subscribe/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': csrfToken ? csrfToken.value : ''
    },
    body: 'email=' + encodeURIComponent(email)
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Show success message
      const successMessage = document.createElement('div');
      successMessage.className = 'newsletter-success';
      successMessage.innerHTML = `
        <p>Thank you for subscribing! Check your email for confirmation.</p>
      `;
      form.parentNode.replaceChild(successMessage, form);
    } else {
      // Show error message
      alert(data.error || 'An error occurred. Please try again.');
      button.textContent = originalText;
      button.disabled = false;
    }
  })
  .catch(err => {
    console.error('Error:', err);
    alert('An error occurred. Please try again.');
    button.textContent = originalText;
    button.disabled = false;
  });
}

// Attach to window for inline handlers
window.handleNewsletterSubmit = handleNewsletterSubmit;

// Initialize newsletter forms on page load
document.addEventListener('DOMContentLoaded', function() {
  // Handle footer newsletter form
  const footerForm = document.getElementById('footer-newsletter-form');
  if (footerForm) {
    footerForm.addEventListener('submit', function(e) {
      e.preventDefault();
      handleNewsletterSubmit(this);
    });
  }
});

/**
 * Copy link to clipboard
 */
function copyLink(url) {
  navigator.clipboard.writeText(url).then(() => {
    alert('Link copied to clipboard!');
  }).catch(err => {
    console.error('Failed to copy:', err);
  });
}

window.copyLink = copyLink;

/**
 * Format date for display
 */
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('en-US', options);
}

window.formatDate = formatDate;

/**
 * Truncate text
 */
function truncateText(text, maxLength) {
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength).trim() + '...';
}

window.truncateText = truncateText;

/**
 * Auth state management
 * Note: This function is disabled for Django templates as auth is handled server-side
 * The Django templates use {% if user.is_authenticated %} for auth state
 */
function initAuthState() {
  // Django handles auth state server-side via template context
  // This function is kept for compatibility but does not override Django templates
  return;
}

/**
 * Sign out function - Django handles logout via URL
 * This is kept for any client-side cleanup if needed
 */
function signOut(event) {
  // Django handles the actual logout via the signout URL
  // The link in the template points to /signout/ which does the logout
}

window.signOut = signOut;

/**
 * Navigation helpers - Django handles these via URLs
 */
function goToProfile() {
  window.location.href = '/profile/';
}

function goToSaved() {
  window.location.href = '/profile/';
}

function goToSettings() {
  window.location.href = '/profile/';
}

window.goToProfile = goToProfile;
window.goToSaved = goToSaved;
window.goToSettings = goToSettings;
