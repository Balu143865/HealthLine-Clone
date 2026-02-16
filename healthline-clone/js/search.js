/**
 * Healthline Clone - Search Functionality
 * Handles search indexing, autocomplete, and results display
 */

class HealthlineSearch {
  constructor(options = {}) {
    this.searchInput = options.searchInput;
    this.suggestionsContainer = options.suggestionsContainer;
    this.resultsContainer = options.resultsContainer;
    this.dataUrl = options.dataUrl || 'data/articles.json';
    this.minChars = options.minChars || 2;
    this.maxResults = options.maxResults || 10;
    
    this.articles = [];
    this.categories = [];
    this.searchIndex = [];
    
    this.init();
  }

  async init() {
    await this.loadData();
    this.buildIndex();
    this.bindEvents();
  }

  /**
   * Load articles data from JSON
   */
  async loadData() {
    try {
      const response = await fetch(this.dataUrl);
      const data = await response.json();
      this.articles = data.articles || [];
      this.categories = data.categories || [];
    } catch (error) {
      console.error('Error loading search data:', error);
    }
  }

  /**
   * Build search index from articles
   */
  buildIndex() {
    this.searchIndex = this.articles.map(article => ({
      id: article.id,
      title: article.title.toLowerCase(),
      excerpt: article.excerpt.toLowerCase(),
      category: article.category.toLowerCase(),
      tags: article.tags.map(t => t.toLowerCase()),
      author: article.author.toLowerCase(),
      slug: article.slug,
      image: article.image,
      readTime: article.readTime,
      date: article.date,
      originalTitle: article.title,
      originalExcerpt: article.excerpt
    }));
  }

  /**
   * Bind event listeners
   */
  bindEvents() {
    if (this.searchInput) {
      this.searchInput.addEventListener('input', this.debounce(() => {
        this.handleInput();
      }, 300));

      this.searchInput.addEventListener('keydown', (e) => {
        this.handleKeydown(e);
      });

      // Close suggestions on click outside
      document.addEventListener('click', (e) => {
        if (!this.searchInput.contains(e.target) && 
            !this.suggestionsContainer?.contains(e.target)) {
          this.hideSuggestions();
        }
      });
    }
  }

  /**
   * Handle input changes
   */
  handleInput() {
    const query = this.searchInput.value.trim();
    
    if (query.length < this.minChars) {
      this.hideSuggestions();
      return;
    }

    const results = this.search(query);
    this.showSuggestions(results, query);
  }

  /**
   * Handle keyboard navigation
   */
  handleKeydown(e) {
    const suggestions = this.suggestionsContainer?.querySelectorAll('.search-suggestion');
    const activeItem = this.suggestionsContainer?.querySelector('.search-suggestion.active');
    
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        if (!activeItem && suggestions?.length) {
          suggestions[0].classList.add('active');
        } else if (activeItem) {
          const next = activeItem.nextElementSibling;
          if (next?.classList.contains('search-suggestion')) {
            activeItem.classList.remove('active');
            next.classList.add('active');
          }
        }
        break;
        
      case 'ArrowUp':
        e.preventDefault();
        if (activeItem) {
          const prev = activeItem.previousElementSibling;
          if (prev?.classList.contains('search-suggestion')) {
            activeItem.classList.remove('active');
            prev.classList.add('active');
          }
        }
        break;
        
      case 'Enter':
        e.preventDefault();
        if (activeItem) {
          const slug = activeItem.dataset.slug;
          window.location.href = `pages/articles/article.html?slug=${slug}`;
        } else {
          this.performSearch();
        }
        break;
        
      case 'Escape':
        this.hideSuggestions();
        break;
    }
  }

  /**
   * Search articles
   */
  search(query) {
    const queryLower = query.toLowerCase();
    const queryWords = queryLower.split(/\s+/);

    const results = this.searchIndex
      .map(article => {
        let score = 0;
        
        // Title match (highest priority)
        if (article.title.includes(queryLower)) {
          score += 100;
          if (article.title.startsWith(queryLower)) {
            score += 50;
          }
        }
        
        // Exact phrase match in title
        if (article.title.includes(queryLower)) {
          score += 30;
        }
        
        // Category match
        if (article.category.includes(queryLower)) {
          score += 20;
        }
        
        // Tags match
        article.tags.forEach(tag => {
          if (tag.includes(queryLower)) {
            score += 15;
          }
        });
        
        // Excerpt match
        if (article.excerpt.includes(queryLower)) {
          score += 10;
        }
        
        // Author match
        if (article.author.includes(queryLower)) {
          score += 5;
        }
        
        // Word matches
        queryWords.forEach(word => {
          if (article.title.includes(word)) score += 5;
          if (article.excerpt.includes(word)) score += 2;
        });

        return { ...article, score };
      })
      .filter(article => article.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, this.maxResults);

    return results;
  }

  /**
   * Show search suggestions
   */
  showSuggestions(results, query) {
    if (!this.suggestionsContainer) return;

    if (results.length === 0) {
      this.suggestionsContainer.innerHTML = `
        <div class="search-suggestion no-results">
          <span class="search-suggestion-text">No results found for "${query}"</span>
        </div>
      `;
      this.suggestionsContainer.classList.add('active');
      return;
    }

    const html = results.map(result => `
      <div class="search-suggestion" data-slug="${result.slug}">
        <div class="search-suggestion-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
          </svg>
        </div>
        <div class="search-suggestion-text">
          ${this.highlightMatch(result.originalTitle, query)}
        </div>
        <div class="search-suggestion-category">
          ${this.getCategoryName(result.category)}
        </div>
      </div>
    `).join('');

    this.suggestionsContainer.innerHTML = html;
    this.suggestionsContainer.classList.add('active');

    // Add click handlers
    this.suggestionsContainer.querySelectorAll('.search-suggestion').forEach(suggestion => {
      suggestion.addEventListener('click', () => {
        const slug = suggestion.dataset.slug;
        if (slug) {
          window.location.href = `pages/articles/article.html?slug=${slug}`;
        }
      });
    });
  }

  /**
   * Hide search suggestions
   */
  hideSuggestions() {
    if (this.suggestionsContainer) {
      this.suggestionsContainer.classList.remove('active');
    }
  }

  /**
   * Perform full search and navigate to results page
   */
  performSearch() {
    const query = this.searchInput.value.trim();
    if (query) {
      window.location.href = `pages/search-results.html?q=${encodeURIComponent(query)}`;
    }
  }

  /**
   * Highlight matching text
   */
  highlightMatch(text, query) {
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<strong>$1</strong>');
  }

  /**
   * Get category display name
   */
  getCategoryName(categoryId) {
    const category = this.categories.find(c => c.id === categoryId);
    return category ? category.name : categoryId;
  }

  /**
   * Debounce function
   */
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
}

/**
 * Search Results Page Handler
 */
class SearchResultsPage {
  constructor(options = {}) {
    this.resultsContainer = options.resultsContainer;
    this.infoContainer = options.infoContainer;
    this.dataUrl = options.dataUrl || '../data/articles.json';
    this.articles = [];
    this.categories = [];
    
    this.init();
  }

  async init() {
    await this.loadData();
    this.displayResults();
  }

  async loadData() {
    try {
      const response = await fetch(this.dataUrl);
      const data = await response.json();
      this.articles = data.articles || [];
      this.categories = data.categories || [];
    } catch (error) {
      console.error('Error loading data:', error);
    }
  }

  displayResults() {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q') || '';
    
    if (!query) {
      this.showNoQuery();
      return;
    }

    const results = this.searchArticles(query);
    this.renderResults(results, query);
  }

  searchArticles(query) {
    const queryLower = query.toLowerCase();
    
    return this.articles
      .filter(article => {
        const titleMatch = article.title.toLowerCase().includes(queryLower);
        const excerptMatch = article.excerpt.toLowerCase().includes(queryLower);
        const categoryMatch = article.category.toLowerCase().includes(queryLower);
        const tagsMatch = article.tags.some(tag => tag.toLowerCase().includes(queryLower));
        
        return titleMatch || excerptMatch || categoryMatch || tagsMatch;
      })
      .sort((a, b) => {
        // Prioritize title matches
        const aTitleMatch = a.title.toLowerCase().includes(queryLower);
        const bTitleMatch = b.title.toLowerCase().includes(queryLower);
        if (aTitleMatch && !bTitleMatch) return -1;
        if (!aTitleMatch && bTitleMatch) return 1;
        return 0;
      });
  }

  renderResults(results, query) {
    if (this.infoContainer) {
      this.infoContainer.innerHTML = `
        Found <strong>${results.length}</strong> result${results.length !== 1 ? 's' : ''} for "<strong>${query}</strong>"
      `;
    }

    if (!this.resultsContainer) return;

    if (results.length === 0) {
      this.resultsContainer.innerHTML = `
        <div class="no-results">
          <h3>No results found</h3>
          <p>We couldn't find any articles matching "${query}". Try different keywords or browse our categories.</p>
          <a href="../index.html" class="btn btn-primary">Back to Homepage</a>
        </div>
      `;
      return;
    }

    const html = results.map(article => `
      <article class="card">
        <a href="articles/${article.slug}.html">
          <img src="../${article.image}" alt="${article.title}" class="card-image" onerror="this.src='../images/placeholder.jpg'">
        </a>
        <div class="card-content">
          <span class="card-category">${this.getCategoryName(article.category)}</span>
          <h3 class="card-title">
            <a href="articles/${article.slug}.html">${this.highlightMatch(article.title, query)}</a>
          </h3>
          <p class="card-excerpt">${this.highlightMatch(article.excerpt, query)}</p>
          <div class="card-meta">
            <span class="card-meta-item">${article.author}</span>
            <span class="card-meta-item">${article.readTime}</span>
          </div>
        </div>
      </article>
    `).join('');

    this.resultsContainer.innerHTML = `<div class="search-results-grid">${html}</div>`;
  }

  showNoQuery() {
    if (this.infoContainer) {
      this.infoContainer.textContent = 'Enter a search term to find articles.';
    }
    if (this.resultsContainer) {
      this.resultsContainer.innerHTML = '';
    }
  }

  getCategoryName(categoryId) {
    const category = this.categories.find(c => c.id === categoryId);
    return category ? category.name : categoryId;
  }

  highlightMatch(text, query) {
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<mark>$1</mark>');
  }
}

// Initialize search on pages
document.addEventListener('DOMContentLoaded', function() {
  // Header search
  const searchInput = document.querySelector('.header-search-input');
  const suggestionsContainer = document.querySelector('.search-suggestions');
  
  if (searchInput) {
    new HealthlineSearch({
      searchInput,
      suggestionsContainer,
      dataUrl: 'data/articles.json'
    });
  }

  // Search results page
  const resultsContainer = document.querySelector('.search-results-container');
  const infoContainer = document.querySelector('.search-results-info');
  
  if (resultsContainer) {
    new SearchResultsPage({
      resultsContainer,
      infoContainer,
      dataUrl: '../data/articles.json'
    });
  }
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { HealthlineSearch, SearchResultsPage };
}
