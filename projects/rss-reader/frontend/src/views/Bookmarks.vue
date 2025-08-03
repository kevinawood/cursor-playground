<template>
  <div class="min-h-screen transition-colors duration-200" :class="darkMode ? 'bg-gray-900' : 'bg-gray-50'">
    <!-- Header -->
    <div class="transition-colors duration-200 px-4 sm:px-6 lg:px-8" :class="darkMode ? 'bg-gray-800 shadow-sm border-gray-700' : 'bg-white shadow-sm border-b'">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center">
          <h1 class="text-xl lg:text-2xl font-bold transition-colors duration-200" :class="darkMode ? 'text-white' : 'text-gray-900'">Bookmarked Articles</h1>
          <span class="ml-3 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium transition-colors duration-200" :class="darkMode ? 'bg-yellow-900 text-yellow-200' : 'bg-yellow-100 text-yellow-800'">
            {{ stats.bookmarked_articles || 0 }}
          </span>
        </div>
        <div class="flex items-center space-x-4">
          <router-link
            to="/"
            class="text-sm font-medium transition-colors duration-200"
            :class="darkMode ? 'text-gray-400 hover:text-gray-300' : 'text-gray-500 hover:text-gray-700'"
          >
            ← Back to Articles
          </router-link>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 sm:px-0">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p class="mt-4 text-base transition-colors duration-200" :class="darkMode ? 'text-gray-400' : 'text-gray-500'">Loading bookmarked articles...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="articles.length === 0" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 transition-colors duration-200" :class="darkMode ? 'text-gray-500' : 'text-gray-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
          </svg>
          <h3 class="mt-2 text-base font-medium transition-colors duration-200" :class="darkMode ? 'text-white' : 'text-gray-900'">No bookmarked articles</h3>
          <p class="mt-1 text-sm transition-colors duration-200" :class="darkMode ? 'text-gray-400' : 'text-gray-500'">Start bookmarking articles to see them here.</p>
          <div class="mt-6">
            <router-link
              to="/"
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              Browse Articles
            </router-link>
          </div>
        </div>

        <!-- Articles List -->
        <div v-else class="transition-colors duration-200 shadow overflow-hidden sm:rounded-md" :class="darkMode ? 'bg-gray-800' : 'bg-white'">
          <ul class="transition-colors duration-200" :class="darkMode ? 'divide-gray-700' : 'divide-gray-200'">
            <li v-for="article in articles" :key="article.id">
              <div class="px-4 py-4 lg:px-6">
                <div class="space-y-3">
                  <!-- Title and Action Buttons -->
                  <div class="flex items-start justify-between">
                    <div class="flex-1 min-w-0 pr-2">
                      <h3 class="text-base font-medium text-gray-900 leading-6">
                        <a 
                          :href="article.link" 
                          target="_blank" 
                          class="hover:underline text-indigo-600 hover:text-indigo-800"
                          @click="openArticle(article)"
                        >
                          {{ article.title }}
                        </a>
                      </h3>
                    </div>
                    <div class="flex-shrink-0 flex items-center space-x-1">
                      <!-- Summarize Button -->
                      <button
                        @click="summarizeArticle(article)"
                        :disabled="article.summarizing"
                        class="p-1.5 rounded-md text-gray-400 hover:text-blue-600 hover:bg-blue-50 disabled:opacity-50"
                        :title="article.summary ? 'View Summary' : 'Generate Summary'"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                      </button>
                      
                      <!-- Bookmark Button -->
                      <button
                        @click="toggleBookmark(article)"
                        :class="[
                          'p-1.5 rounded-md transition-colors',
                          article.is_bookmarked
                            ? 'text-yellow-500 hover:text-yellow-600 hover:bg-yellow-50'
                            : 'text-gray-400 hover:text-yellow-500 hover:bg-yellow-50'
                        ]"
                        :title="article.is_bookmarked ? 'Remove from bookmarks' : 'Add to bookmarks'"
                      >
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
                        </svg>
                      </button>
                      
                      <!-- Read Status Button -->
                      <button
                        @click="toggleReadStatus(article)"
                        :class="[
                          'px-2 py-1 text-xs font-medium rounded-full border',
                          article.is_read
                            ? 'bg-gray-50 text-gray-700 border-gray-200'
                            : 'bg-yellow-50 text-yellow-700 border-yellow-200'
                        ]"
                      >
                        {{ article.is_read ? 'Read' : 'Unread' }}
                      </button>
                    </div>
                  </div>

                  <!-- Description -->
                  <div v-if="article.description" class="text-sm text-gray-600 leading-5 line-clamp-3">
                    {{ stripHtml(article.description) }}
                  </div>

                  <!-- AI Summary -->
                  <div v-if="article.summary" class="bg-blue-50 border-l-4 border-blue-400 p-3 rounded-r-md">
                    <div class="flex items-start">
                      <div class="flex-shrink-0">
                        <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                      </div>
                      <div class="ml-3">
                        <h4 class="text-sm font-medium text-blue-800 mb-1">AI Summary</h4>
                        <p class="text-sm text-blue-700">{{ article.summary }}</p>
                      </div>
                    </div>
                  </div>

                  <!-- Meta information -->
                  <div class="flex flex-wrap items-center gap-2 text-sm text-gray-500">
                    <div class="flex items-center">
                      <img 
                        v-if="article.feed_logo_url" 
                        :src="article.feed_logo_url" 
                        :alt="article.feed_name"
                        class="w-4 h-4 mr-1.5 rounded-sm flex-shrink-0"
                        @error="handleImageError"
                      />
                      <span v-else class="mr-1.5 flex-shrink-0">{{ getFeedIcon(article.feed_name) }}</span>
                      <span class="font-medium">{{ article.feed_name }}</span>
                    </div>
                    <span class="text-gray-400">•</span>
                    <span>{{ formatTimeAgo(article.published_date) }}</span>
                    <span v-if="article.author" class="text-gray-400">•</span>
                    <span v-if="article.author" class="truncate">{{ article.author }}</span>
                  </div>
                </div>
              </div>
            </li>
          </ul>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="mt-6 flex items-center justify-between">
          <div class="flex-1 flex justify-between sm:hidden">
            <button
              @click="changePage(currentPage - 1)"
              :disabled="currentPage === 1"
              class="relative inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <button
              @click="changePage(currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="ml-3 relative inline-flex items-center px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Showing page <span class="font-medium">{{ currentPage }}</span> of <span class="font-medium">{{ totalPages }}</span>
              </p>
            </div>
            <div>
              <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                <button
                  @click="changePage(currentPage - 1)"
                  :disabled="currentPage === 1"
                  class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Previous
                </button>
                <button
                  @click="changePage(currentPage + 1)"
                  :disabled="currentPage === totalPages"
                  class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Next
                </button>
              </nav>
            </div>
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
      loading: true,
      currentPage: 1,
      totalPages: 1,
      stats: {
        bookmarked_articles: 0
      },
      // HN Discussion Modal
      showHNModal: false,
      hnModalContent: {
        title: '',
        originalUrl: '',
        discussionUrl: '',
        searchUrl: '',
        feedName: ''
      }
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
      
      // Set loading state
      this.$set(article, 'summarizing', true)
      
      try {
        const response = await api.post(`/api/articles/${article.id}/summarize`)
        this.$set(article, 'summary', response.data.summary)
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
    
    async openArticle(article) {
      // Mark as read if not already read
      if (!article.is_read) {
        await this.toggleReadStatus(article)
      }
      
      // Check if this is a Hacker News article
      if (isHackerNewsArticle(article)) {
        this.hnModalContent = getHNModalContent(article)
        this.showHNModal = true
        return
      }
      
      // For non-HN articles, open directly
      window.open(article.link, '_blank')
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
    }
  }
}
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 