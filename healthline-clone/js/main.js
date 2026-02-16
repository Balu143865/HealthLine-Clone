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

  // Search form submission
  const searchForms = document.querySelectorAll('.search-form');
  searchForms.forEach(form => {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      const query = this.querySelector('input[type="search"], input[type="text"]').value.trim();
      if (query) {
        window.location.href = `pages/search-results.html?q=${encodeURIComponent(query)}`;
      }
    });
  });
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

  // Show loading state
  button.textContent = 'Subscribing...';
  button.disabled = true;

  // Simulate API call
  setTimeout(() => {
    // Show success message
    const successMessage = document.createElement('div');
    successMessage.className = 'newsletter-success';
    successMessage.innerHTML = `
      <p>Thank you for subscribing! Check your email for confirmation.</p>
    `;
    form.parentNode.replaceChild(successMessage, form);
  }, 1500);
}

// Attach to window for inline handlers
window.handleNewsletterSubmit = handleNewsletterSubmit;

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
 */
function initAuthState() {
  const headerAuth = document.getElementById('header-auth');
  const mobileNavAuth = document.getElementById('mobile-nav-auth');

  // Determine the correct path based on current location
  const isInSubdirectory = window.location.pathname.includes('/pages/');
  const basePath = isInSubdirectory ? '' : 'pages/';
  
  // Check if user is logged in
  const userData = localStorage.getItem('healthline_user');
  
  console.log('Auth state check - userData:', userData); // Debug log
  
  if (userData) {
    try {
      const user = JSON.parse(userData);
      console.log('Parsed user:', user); // Debug log
      
      if (user && user.loggedIn) {
        // User is logged in - show user dropdown
        const initials = user.name ? user.name.charAt(0).toUpperCase() : user.email.charAt(0).toUpperCase();
        const displayName = user.name || user.email.split('@')[0];
        
        console.log('User is logged in:', displayName); // Debug log
        
        // Update desktop header
        if (headerAuth) {
          headerAuth.innerHTML = `
            <div class="header-auth-user">
              <div class="header-auth-avatar">${initials}</div>
              <span class="header-auth-name">${displayName}</span>
              <div class="header-auth-dropdown">
                <a href="#" onclick="goToProfile(); return false;">My Profile</a>
                <a href="#" onclick="goToSaved(); return false;">Saved Articles</a>
                <a href="#" onclick="goToSettings(); return false;">Settings</a>
                <div class="divider"></div>
                <a href="#" onclick="signOut(event); return false;">Sign Out</a>
              </div>
            </div>
          `;
        }
        
        // Update mobile nav
        if (mobileNavAuth) {
          mobileNavAuth.innerHTML = `
            <div class="mobile-nav-user">
              <div class="mobile-nav-avatar">${initials}</div>
              <div class="mobile-nav-user-info">
                <div class="mobile-nav-user-name">${displayName}</div>
                <div class="mobile-nav-user-email">${user.email}</div>
              </div>
            </div>
            <div class="mobile-nav-user-actions">
              <a href="#" onclick="goToProfile(); return false;">My Profile</a>
              <a href="#" onclick="goToSaved(); return false;">Saved Articles</a>
              <a href="#" onclick="goToSettings(); return false;">Settings</a>
              <a href="#" onclick="signOut(event); return false;">Sign Out</a>
            </div>
          `;
        }
        return; // User is logged in, no need to show sign up/sign in buttons
      }
    } catch (e) {
      console.error('Error parsing user data:', e);
    }
  }
  
  // User is not logged in - show sign up/sign in buttons
  console.log('User is not logged in, showing sign in/up buttons'); // Debug log
  
  if (headerAuth) {
    headerAuth.innerHTML = `
      <a href="${basePath}signin.html" class="btn btn-text">Sign In</a>
      <a href="${basePath}signup.html" class="btn btn-primary">Sign Up</a>
    `;
  }
  
  // Update mobile nav for logged out state
  if (mobileNavAuth) {
    mobileNavAuth.innerHTML = `
      <a href="${basePath}signin.html" class="mobile-nav-link">Sign In</a>
      <a href="${basePath}signup.html" class="mobile-nav-link">Sign Up</a>
    `;
  }
}

/**
 * Sign out function
 */
function signOut(event) {
  event.preventDefault();
  localStorage.removeItem('healthline_user');
  // Redirect to home page after logout
  const isInSubdirectory = window.location.pathname.includes('/pages/');
  const homePath = isInSubdirectory ? '../index.html' : 'index.html';
  window.location.href = homePath;
}

window.signOut = signOut;

/**
 * Navigation helpers for dropdown
 */
function goToProfile() {
  alert('Profile page coming soon!');
}

function goToSaved() {
  alert('Saved articles page coming soon!');
}

function goToSettings() {
  alert('Settings page coming soon!');
}

window.goToProfile = goToProfile;
window.goToSaved = goToSaved;
window.goToSettings = goToSettings;
