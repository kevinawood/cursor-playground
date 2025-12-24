<template>
  <div class="min-h-screen transition-colors duration-200" :class="darkMode ? 'bg-[#111111]' : 'bg-white'">
    <!-- Header -->
    <div class="rounded-xl border p-6 mb-6" :class="darkMode ? 'bg-[#1a1a1a] border-[#262626]' : 'bg-white border-gray-200'">
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
          <h1 class="text-xl font-semibold" :class="darkMode ? 'text-white' : 'text-gray-900'">Bookmarked Articles</h1>
          <span class="px-2 py-0.5 text-xs font-medium rounded-md"
                :class="darkMode ? 'bg-blue-500/10 text-blue-400' : 'bg-blue-50 text-blue-600'">
            {{ stats.bookmarked_articles || 0 }}
          </span>
        </div>
        <router-link
          to="/"
          class="text-sm font-medium transition-colors"
          :class="darkMode ? 'text-gray-400 hover:text-white' : 'text-gray-500 hover:text-gray-900'"
        >
          ← Back to Articles
        </router-link>
      </div>
    </div>

    <!-- Content -->
    <div>
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-2 border-blue-600 border-t-transparent mx-auto"></div>
        <p class="mt-4 text-sm" :class="darkMode ? 'text-gray-500' : 'text-gray-400'">Loading bookmarked articles...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="articles.length === 0" class="text-center py-12">
        <svg class="mx-auto h-10 w-10" :class="darkMode ? 'text-gray-600' : 'text-gray-300'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
        </svg>
        <h3 class="mt-3 text-sm font-medium" :class="darkMode ? 'text-white' : 'text-gray-900'">No bookmarked articles</h3>
        <p class="mt-1 text-sm" :class="darkMode ? 'text-gray-400' : 'text-gray-500'">Start bookmarking articles to see them here.</p>
        <div class="mt-4">
          <router-link
            to="/"
            class="px-4 py-2 text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 transition-colors inline-block"
          >
            Browse Articles
          </router-link>
        </div>
      </div>

      <!-- Articles List -->
      <div v-else class="divide-y" :class="darkMode ? 'divide-[#262626]' : 'divide-gray-100'">
        <article v-for="article in articles" :key="article.id" class="py-5 first:pt-0">
          <div class="space-y-3">
            <!-- Title and Action Buttons -->
            <div class="flex items-start justify-between gap-4">
              <h3 class="flex-1 text-base font-medium leading-snug" :class="darkMode ? 'text-white' : 'text-gray-900'">
                <a 
                  :href="article.link" 
                  target="_blank" 
                  class="hover:text-blue-600 transition-colors cursor-pointer"
                  @click="openArticle(article, $event)"
                >
                  {{ article.title }}
                </a>
              </h3>
              <div class="flex-shrink-0 flex items-center space-x-1">
                <button
                  @click="summarizeArticle(article)"
                  :disabled="article.summarizing"
                  class="p-1.5 rounded-md transition-colors"
                  :class="darkMode ? 'text-gray-500 hover:text-blue-400 hover:bg-blue-500/10' : 'text-gray-400 hover:text-blue-600 hover:bg-blue-50'"
                  :title="article.summary ? 'View Summary' : 'Generate Summary'"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </button>
                <button
                  @click="toggleBookmark(article)"
                  class="p-1.5 rounded-md transition-colors"
                  :class="article.is_bookmarked
                    ? 'text-yellow-500 hover:text-yellow-600'
                    : darkMode ? 'text-gray-500 hover:text-yellow-400' : 'text-gray-400 hover:text-yellow-500'"
                  :title="article.is_bookmarked ? 'Remove from bookmarks' : 'Add to bookmarks'"
                >
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
                  </svg>
                </button>
                <button
                  @click="toggleReadStatus(article)"
                  class="px-2 py-1 text-xs font-medium rounded-md transition-colors"
                  :class="article.is_read
                    ? darkMode ? 'bg-gray-800 text-gray-400' : 'bg-gray-100 text-gray-500'
                    : 'bg-blue-100 text-blue-700'"
                >
                  {{ article.is_read ? 'Read' : 'Unread' }}
                </button>
              </div>
            </div>

            <!-- Description -->
            <p v-if="article.description" class="text-sm leading-relaxed line-clamp-2" :class="darkMode ? 'text-gray-400' : 'text-gray-600'">
              {{ stripHtml(article.description) }}
            </p>

            <!-- AI Summary -->
            <div v-if="article.summary" class="p-3 rounded-lg" :class="darkMode ? 'bg-blue-500/10 border border-blue-500/20' : 'bg-blue-50'">
              <p class="text-sm" :class="darkMode ? 'text-blue-300' : 'text-blue-700'">{{ article.summary }}</p>
            </div>

            <!-- Meta information -->
            <div class="flex flex-wrap items-center gap-2 text-xs" :class="darkMode ? 'text-gray-500' : 'text-gray-400'">
              <span class="font-medium" :class="darkMode ? 'text-gray-400' : 'text-gray-500'">{{ article.feed_name }}</span>
              <span>•</span>
              <span>{{ formatTimeAgo(article.published_date) }}</span>
              <span>•</span>
              <span class="inline-flex items-center">
                <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                {{ calculateReadingTime(article) }}
              </span>
              <span v-if="article.author">•</span>
              <span v-if="article.author">{{ article.author }}</span>
            </div>
          </div>
        </article>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="mt-8 flex items-center justify-between">
        <div class="flex-1 flex justify-between sm:hidden">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-4 py-2 text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
            :class="darkMode ? 'bg-[#1a1a1a] text-gray-300 border border-[#262626]' : 'bg-white text-gray-700 border border-gray-200'"
          >
            Previous
          </button>
          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-4 py-2 text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
            :class="darkMode ? 'bg-[#1a1a1a] text-gray-300 border border-[#262626]' : 'bg-white text-gray-700 border border-gray-200'"
          >
            Next
          </button>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <p class="text-sm" :class="darkMode ? 'text-gray-400' : 'text-gray-500'">
            Page <span class="font-medium" :class="darkMode ? 'text-white' : 'text-gray-900'">{{ currentPage }}</span> of <span class="font-medium" :class="darkMode ? 'text-white' : 'text-gray-900'">{{ totalPages }}</span>
          </p>
          <div class="flex gap-2">
            <button
              @click="changePage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="px-4 py-2 text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
              :class="darkMode ? 'bg-[#1a1a1a] text-gray-300 border border-[#262626] hover:bg-[#222]' : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'"
            >
              Previous
            </button>
            <button
              @click="changePage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="px-4 py-2 text-sm font-medium rounded-lg transition-colors disabled:opacity-50"
              :class="darkMode ? 'bg-[#1a1a1a] text-gray-300 border border-[#262626] hover:bg-[#222]' : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- HN Discussion Modal -->
    <HNDiscussionModal
      :show="showHNModal"
      :modal-content="hnModalContent"
      :dark-mode="darkMode"
      @close="closeHNModal"
      @choice-made="handleHNChoice"
    />
  </div>
</template>

<script>
import api from '../config/axios'
import { isHackerNewsArticle, getHNModalContent } from '../utils/hnUtils'
import HNDiscussionModal from '../components/HNDiscussionModal.vue'

export default {
  name: 'Bookmarks',
  components: {
    HNDiscussionModal
  },
  props: {
    darkMode: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      articles: [],
      stats: {
        bookmarked_articles: 0
      },
      loading: true,
      currentPage: 1,
      totalPages: 1,
      // HN Discussion Modal
      showHNModal: false,
      hnModalContent: {
        title: '',
        originalUrl: '',
        discussionUrl: '',
        searchUrl: '',
        feedName: ''
      },
      // Reading time cache
      readingTimeCache: new Map(),
      // AI Summary cache
      summaryCache: new Map()
    }
  },
  async mounted() {
    await this.loadBookmarkedArticles()
    await this.loadStats()
  },
  methods: {
    async loadBookmarkedArticles() {
      this.loading = true
      try {
        const params = {
          page: this.currentPage,
          per_page: 20
        }
        
        const response = await api.get('/api/articles/bookmarked', { params })
        this.articles = response.data.articles
        this.totalPages = response.data.pages
      } catch (error) {
        console.error('Error loading bookmarked articles:', error)
      } finally {
        this.loading = false
      }
    },
    
    async loadStats() {
      try {
        const response = await api.get('/api/stats')
        this.stats = response.data
      } catch (error) {
        console.error('Error loading stats:', error)
      }
    },
    
    async toggleReadStatus(article) {
      try {
        const endpoint = article.is_read ? 'unread' : 'read'
        await api.put(`/api/articles/${article.id}/${endpoint}`)
        article.is_read = !article.is_read
        await this.loadStats()
      } catch (error) {
        console.error('Error toggling read status:', error)
      }
    },
    
    async toggleBookmark(article) {
      try {
        const response = await api.put(`/api/articles/${article.id}/bookmark`)
        article.is_bookmarked = response.data.is_bookmarked
        
        // Remove from list if unbookmarked
        if (!article.is_bookmarked) {
          this.articles = this.articles.filter(a => a.id !== article.id)
          await this.loadStats()
        }
      } catch (error) {
        console.error('Error toggling bookmark:', error)
      }
    },
    
    async summarizeArticle(article) {
      // If summary already exists, just show/hide it
      if (article.summary) {
        article.summary = null
        return
      }
      
      // Check cache first
      if (this.summaryCache.has(article.id)) {
        article.summary = this.summaryCache.get(article.id);
        return;
      }
      
      // Set loading state
      this.$set(article, 'summarizing', true)
      
      try {
        const response = await api.post(`/api/articles/${article.id}/summarize`)
        this.$set(article, 'summary', response.data.summary)
        
        // Cache the summary
        this.summaryCache.set(article.id, response.data.summary);
      } catch (error) {
        console.error('Error generating summary:', error)
        alert('Failed to generate summary. Please try again.')
      } finally {
        this.$set(article, 'summarizing', false)
      }
    },
    
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        this.loadBookmarkedArticles()
      }
    },
    
    formatTimeAgo(dateString) {
      if (!dateString) return 'Unknown time'
      const date = new Date(dateString)
      const now = new Date()
      const diffInSeconds = Math.floor((now - date) / 1000)
      
      if (diffInSeconds < 60) return 'Just now'
      if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`
      if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`
      if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)}d ago`
      if (diffInSeconds < 31536000) return `${Math.floor(diffInSeconds / 2592000)}mo ago`
      return `${Math.floor(diffInSeconds / 31536000)}y ago`
    },
    
    stripHtml(html) {
      const tmp = document.createElement('div')
      tmp.innerHTML = html
      return tmp.textContent || tmp.innerText || ''
    },
    
    async openArticle(article, event) {
      // Check if this is a Hacker News article
      if (isHackerNewsArticle(article)) {
        // Prevent default for HN articles to show modal
        if (event) {
          event.preventDefault();
        }
        this.hnModalContent = getHNModalContent(article)
        this.showHNModal = true
        return
      }
      
      // For non-HN articles, let the default link behavior happen
      // Just mark as read if not already read
      if (!article.is_read) {
        await this.toggleReadStatus(article)
      }
      
      // Don't prevent default - let the link open naturally
    },
    
    getFeedIcon(feedName) {
      // Simple mapping of feed names to icons
      const iconMap = {
        'Wired Magazine': '🔬',
        'TechCrunch': '📱',
        'Hacker News': '💻',
        'Ars Technica': '⚡',
        'The Verge': '🎯',
        'Engadget': '🔧',
        'Mashable': '📰',
        'Gizmodo': '🤖',
        'VentureBeat': '💰',
        'Recode': '📊'
      }
      return iconMap[feedName] || '📄'
    },
    
    handleImageError(event) {
      // Hide the image if it fails to load
      event.target.style.display = 'none'
    },
    
    closeHNModal() {
      this.showHNModal = false
    },
    
    async handleHNChoice(choice) {
      // Find the article that was clicked
      const article = this.articles.find(a => a.title === this.hnModalContent.title)
      if (article && !article.is_read) {
        await this.toggleReadStatus(article)
      }
    },

    calculateReadingTime(article) {
      // Check cache first
      if (this.readingTimeCache.has(article.id)) {
        return this.readingTimeCache.get(article.id);
      }

      // For now, return a loading state while we fetch the actual reading time
      this.fetchAccurateReadingTime(article);
      return 'Calculating...';
    },

    async fetchAccurateReadingTime(article) {
      try {
        const response = await api.get(`/api/articles/${article.id}/reading-time`);
        const result = response.data;
        
        // Cache the result
        this.readingTimeCache.set(article.id, result.reading_time);
        
        // Force re-render to update the display
        this.$forceUpdate();
        
      } catch (error) {
        console.error('Error fetching reading time:', error);
        // Fallback to estimation
        const fallbackTime = this.calculateFallbackReadingTime(article);
        this.readingTimeCache.set(article.id, fallbackTime);
        this.$forceUpdate();
      }
    },

    calculateFallbackReadingTime(article) {
      // Fallback estimation when API fails
      const title = article.title || '';
      const description = article.description || '';
      
      const titleWords = title.split(/\s+/).filter(word => word.length > 0).length;
      const descWords = description.split(/\s+/).filter(word => word.length > 0).length;
      
      let estimatedWords = 0;
      
      if (descWords > 100) {
        estimatedWords = descWords * 2;
      } else if (titleWords > 10) {
        estimatedWords = titleWords * 20;
      } else {
        const feedName = article.feed_name || '';
        if (feedName.includes('Hacker News') || feedName.includes('TechCrunch')) {
          estimatedWords = 800;
        } else if (feedName.includes('Wired') || feedName.includes('Ars Technica')) {
          estimatedWords = 1500;
        } else {
          estimatedWords = 600;
        }
      }
      
      const readingSpeed = 200;
      const minutes = Math.ceil(estimatedWords / readingSpeed);
      const finalMinutes = Math.max(1, minutes);
      
      if (finalMinutes === 1) {
        return '1 min read (estimated)';
      } else if (finalMinutes < 60) {
        return `${finalMinutes} min read (estimated)`;
      } else {
        const hours = Math.floor(finalMinutes / 60);
        const remainingMinutes = finalMinutes % 60;
        if (remainingMinutes === 0) {
          return `${hours}h read (estimated)`;
        } else {
          return `${hours}h ${remainingMinutes}m read (estimated)`;
        }
      }
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
