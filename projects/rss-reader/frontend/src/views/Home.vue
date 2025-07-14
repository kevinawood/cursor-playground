<template>
  <div class="px-4 sm:px-6 lg:px-8">
    <!-- Header -->
    <div class="sm:flex sm:items-center">
      <div class="sm:flex-auto">
        <h1 class="text-2xl font-semibold text-gray-900">Articles</h1>
        <p class="mt-2 text-sm text-gray-700">
          Latest articles from your RSS feeds
        </p>
      </div>
      <div class="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
        <div class="flex space-x-4">
          <!-- Category filter -->
          <select
            v-model="selectedCategory"
            @change="loadArticles"
            class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
          >
            <option value="">All Categories</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
          
          <!-- Unread filter -->
          <button
            @click="toggleUnreadOnly"
            :class="[
              'px-4 py-2 text-sm font-medium rounded-md',
              unreadOnly
                ? 'bg-indigo-600 text-white hover:bg-indigo-700'
                : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
            ]"
          >
            {{ unreadOnly ? 'Show All' : 'Unread Only' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Stats -->
    <div class="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-4">
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-indigo-500 rounded-md flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 5c7.18 0 13 5.82 13 13M6 11a7 7 0 017 7m-6 0a1 1 0 11-2 0 1 1 0 012 0z"></path>
                </svg>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Total Feeds</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats.total_feeds }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Total Articles</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats.total_articles }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Unread</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats.unread_articles }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">Read</dt>
                <dd class="text-lg font-medium text-gray-900">{{ stats.read_articles }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Articles list -->
    <div class="mt-8">
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
        <p class="mt-4 text-gray-500">Loading articles...</p>
      </div>

      <div v-else-if="articles.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No articles</h3>
        <p class="mt-1 text-sm text-gray-500">Get started by adding some RSS feeds.</p>
        <div class="mt-6">
          <router-link
            to="/feeds"
            class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            Add Feeds
          </router-link>
        </div>
      </div>

      <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
        <ul class="divide-y divide-gray-200">
          <li v-for="article in articles" :key="article.id">
            <div class="px-4 py-4 sm:px-6">
              <div class="flex items-center justify-between">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between">
                    <p class="text-sm font-medium text-indigo-600 truncate">
                      <a 
                        :href="article.link" 
                        target="_blank" 
                        class="hover:underline"
                        @click="openArticle(article)"
                      >
                        {{ article.title }}
                      </a>
                    </p>
                    <div class="ml-2 flex-shrink-0 flex">
                      <button
                        @click="toggleReadStatus(article)"
                        :class="[
                          'px-2 py-1 text-xs font-medium rounded-full',
                          article.is_read
                            ? 'bg-gray-100 text-gray-800'
                            : 'bg-yellow-100 text-yellow-800'
                        ]"
                      >
                        {{ article.is_read ? 'Read' : 'Unread' }}
                      </button>
                    </div>
                  </div>
                  <div class="mt-2 flex">
                    <div class="flex items-center text-sm text-gray-500">
                      <img 
                        v-if="article.feed_logo_url" 
                        :src="article.feed_logo_url" 
                        :alt="article.feed_name"
                        class="w-4 h-4 mr-1 rounded-sm"
                        @error="handleImageError"
                      />
                      <span v-else class="mr-1">{{ getFeedIcon(article.feed_name) }}</span>
                      <span class="truncate">{{ article.feed_name }}</span>
                      <span class="mx-1">•</span>
                      <span>{{ formatTimeAgo(article.published_date) }}</span>
                      <span v-if="article.author" class="mx-1">•</span>
                      <span v-if="article.author" class="truncate">{{ article.author }}</span>
                    </div>
                  </div>
                  <div v-if="article.description" class="mt-2 text-sm text-gray-600 line-clamp-2">
                    {{ stripHtml(article.description) }}
                  </div>
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
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
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
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  data() {
    return {
      articles: [],
      categories: [],
      stats: {
        total_feeds: 0,
        total_articles: 0,
        unread_articles: 0,
        read_articles: 0
      },
      loading: true,
      currentPage: 1,
      totalPages: 1,
      selectedCategory: '',
      unreadOnly: false
    }
  },
  async mounted() {
    await this.loadCategories()
    await this.loadStats()
    await this.loadArticles()
  },
  methods: {
    async loadArticles() {
      this.loading = true
      try {
        const params = {
          page: this.currentPage,
          per_page: 20
        }
        
        if (this.selectedCategory) {
          params.category = this.selectedCategory
        }
        
        if (this.unreadOnly) {
          params.unread_only = true
        }
        
        const response = await axios.get('/api/articles', { params })
        this.articles = response.data.articles
        this.totalPages = response.data.pages
      } catch (error) {
        console.error('Error loading articles:', error)
      } finally {
        this.loading = false
      }
    },
    
    async loadCategories() {
      try {
        const response = await axios.get('/api/categories')
        this.categories = response.data
      } catch (error) {
        console.error('Error loading categories:', error)
      }
    },
    
    async loadStats() {
      try {
        const response = await axios.get('/api/stats')
        this.stats = response.data
      } catch (error) {
        console.error('Error loading stats:', error)
      }
    },
    
    async toggleReadStatus(article) {
      try {
        const endpoint = article.is_read ? 'unread' : 'read'
        await axios.put(`/api/articles/${article.id}/${endpoint}`)
        article.is_read = !article.is_read
        await this.loadStats()
      } catch (error) {
        console.error('Error toggling read status:', error)
      }
    },
    
    toggleUnreadOnly() {
      this.unreadOnly = !this.unreadOnly
      this.currentPage = 1
      this.loadArticles()
    },
    
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.currentPage = page
        this.loadArticles()
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return 'Unknown date'
      const date = new Date(dateString)
      return date.toLocaleDateString()
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