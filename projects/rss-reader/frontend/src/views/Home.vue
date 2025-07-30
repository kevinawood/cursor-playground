<template>
  <div class="flex min-h-screen bg-gray-50">
    <!-- Sidebar -->
    <div 
      :class="[
        'fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:relative lg:translate-x-0',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
      style="top: 3.5rem; height: calc(100vh - 3.5rem);"
    >
      <!-- Sidebar Header -->
      <div class="flex items-center justify-between h-12 sm:h-16 px-4 border-b border-gray-200">
        <h2 class="text-base sm:text-lg font-semibold text-gray-900">Subscribed Feeds</h2>
        <button
          @click="sidebarOpen = false"
          class="lg:hidden p-1.5 sm:p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100"
        >
          <svg class="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <!-- Sidebar Content -->
      <div class="flex-1 overflow-y-auto">
        <div class="p-3 sm:p-4">
          <!-- All Feeds Option -->
          <button
            @click="selectFeed(null)"
            :class="[
              'w-full flex items-center px-2 sm:px-3 py-2 text-sm font-medium rounded-md mb-2 transition-colors',
              selectedFeedId === null
                ? 'bg-indigo-100 text-indigo-700'
                : 'text-gray-700 hover:bg-gray-100'
            ]"
          >
            <svg class="w-4 h-4 mr-2 sm:mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
            </svg>
            All Feeds
            <span class="ml-auto text-xs text-gray-500">{{ stats.total_articles }}</span>
          </button>

          <!-- Feeds List -->
          <div v-if="feedsLoading" class="text-center py-4">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-600 mx-auto"></div>
          </div>

          <div v-else-if="feeds.length === 0" class="text-center py-4">
            <p class="text-sm text-gray-500">No feeds yet</p>
            <router-link
              to="/feeds"
              class="mt-2 inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200"
            >
              Add Feeds
            </router-link>
          </div>

          <div v-else class="space-y-1">
            <button
              v-for="feed in feeds"
              :key="feed.id"
              @click="selectFeed(feed.id)"
              :class="[
                'w-full flex items-center px-2 sm:px-3 py-2 text-sm font-medium rounded-md transition-colors',
                selectedFeedId === feed.id
                  ? 'bg-indigo-100 text-indigo-700'
                  : 'text-gray-700 hover:bg-gray-100'
              ]"
            >
              <img 
                v-if="feed.logo_url" 
                :src="feed.logo_url" 
                :alt="feed.name"
                class="w-4 h-4 mr-2 sm:mr-3 rounded-sm flex-shrink-0"
                @error="handleImageError"
              />
              <span v-else class="w-4 h-4 mr-2 sm:mr-3 text-center flex-shrink-0">{{ getFeedIcon(feed.name) }}</span>
              <span class="truncate flex-1 text-left">{{ feed.name }}</span>
              <span class="text-xs text-gray-500 flex-shrink-0">{{ feed.article_count }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Sidebar Overlay for Mobile -->
    <div 
      v-if="sidebarOpen" 
      @click="sidebarOpen = false"
      class="fixed inset-0 bg-gray-600 bg-opacity-75 z-40 lg:hidden"
      style="top: 3.5rem;"
    ></div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Top Bar -->
      <div class="bg-white shadow-sm border-b px-3 sm:px-4 lg:px-8">
        <div class="flex items-center justify-between h-12 sm:h-16">
          <!-- Mobile menu button -->
          <button
            @click="sidebarOpen = true"
            class="lg:hidden p-1.5 sm:p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
          </button>

          <!-- Title and Filters -->
          <div class="flex-1 min-w-0 ml-2 lg:ml-0">
            <h1 class="text-lg sm:text-xl lg:text-2xl font-bold text-gray-900 truncate">
              {{ selectedFeedId ? getSelectedFeedName() : 'All Articles' }}
            </h1>
            <!-- Mobile navigation links -->
            <div class="flex sm:hidden mt-1 space-x-4">
              <router-link
                to="/"
                class="text-xs font-medium text-gray-500 hover:text-gray-700"
                active-class="text-indigo-600"
              >
                Articles
              </router-link>
              <router-link
                to="/feeds"
                class="text-xs font-medium text-gray-500 hover:text-gray-700"
                active-class="text-indigo-600"
              >
                Feeds
              </router-link>
            </div>
          </div>

          <!-- Filter and Refresh Controls -->
          <div class="flex items-center space-x-2 sm:space-x-4">
            <button
              @click="toggleUnreadOnly"
              :class="[
                'px-2 sm:px-3 py-1 sm:py-2 text-xs sm:text-sm font-medium rounded-md transition-colors',
                showUnreadOnly
                  ? 'bg-indigo-100 text-indigo-700'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              ]"
            >
              <span class="hidden sm:inline">{{ showUnreadOnly ? 'Unread Only' : 'Show All' }}</span>
              <span class="sm:hidden">{{ showUnreadOnly ? 'Unread' : 'All' }}</span>
            </button>
            <button
              @click="refreshFeeds"
              :disabled="refreshing"
              class="p-1.5 sm:p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100 disabled:opacity-50"
            >
              <svg 
                :class="['w-4 h-4 sm:w-5 sm:h-5', refreshing ? 'animate-spin' : '']" 
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Content Area -->
      <div class="flex-1 overflow-y-auto">
        <div class="px-3 sm:px-4 lg:px-8 py-4 sm:py-6">
        <!-- Stats Cards - Hidden on mobile to save space -->
        <div class="hidden sm:grid sm:grid-cols-1 md:grid-cols-3 gap-4 lg:gap-6 mb-6 lg:mb-8">
          <div class="bg-white overflow-hidden shadow rounded-lg">
            <div class="p-4 lg:p-5">
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
            <div class="p-4 lg:p-5">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <div class="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-5 5v-5zM9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
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
            <div class="p-4 lg:p-5">
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
        <div>
          <div v-if="loading" class="text-center py-8 sm:py-12">
            <div class="animate-spin rounded-full h-8 w-8 sm:h-12 sm:w-12 border-b-2 border-indigo-600 mx-auto"></div>
            <p class="mt-4 text-sm sm:text-base text-gray-500">Loading articles...</p>
          </div>

          <div v-else-if="articles.length === 0" class="text-center py-8 sm:py-12">
            <svg class="mx-auto h-8 w-8 sm:h-12 sm:w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <h3 class="mt-2 text-sm sm:text-base font-medium text-gray-900">No articles</h3>
            <p class="mt-1 text-xs sm:text-sm text-gray-500">Get started by adding some RSS feeds.</p>
            <div class="mt-4 sm:mt-6">
              <router-link
                to="/feeds"
                class="inline-flex items-center px-3 py-2 sm:px-4 sm:py-2 border border-transparent shadow-sm text-xs sm:text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
              >
                Add Feeds
              </router-link>
            </div>
          </div>

          <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
            <ul class="divide-y divide-gray-200">
              <li v-for="article in articles" :key="article.id">
                <div class="px-3 py-3 sm:px-4 sm:py-4 lg:px-6">
                  <div class="space-y-3">
                    <!-- Title and Read Status -->
                    <div class="flex items-start justify-between">
                      <div class="flex-1 min-w-0 pr-2">
                        <h3 class="text-sm sm:text-base font-medium text-gray-900 leading-5 sm:leading-6">
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
                      <div class="flex-shrink-0">
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
                    <div v-if="article.description" class="text-sm text-gray-600 leading-5 line-clamp-3 sm:line-clamp-2">
                      {{ stripHtml(article.description) }}
                    </div>

                    <!-- Meta information -->
                    <div class="flex flex-wrap items-center gap-2 text-xs sm:text-sm text-gray-500">
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
      </div>
    </div>
  </div>
</template>

<script>
import api from '../config/axios'

export default {
  name: 'Home',
  data() {
    return {
      articles: [],
      categories: [],
      feeds: [],
      stats: {
        total_feeds: 0,
        total_articles: 0,
        unread_articles: 0,
        read_articles: 0
      },
      loading: true,
      feedsLoading: true,
      currentPage: 1,
      totalPages: 1,
      selectedCategory: '',
      unreadOnly: false,
      selectedFeedId: null,
      sidebarOpen: false,
      refreshing: false
    }
  },
  async mounted() {
    await this.loadCategories()
    await this.loadStats()
    await this.loadFeeds()
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
        
        if (this.selectedFeedId) {
          params.feed_id = this.selectedFeedId
        }
        
        const response = await api.get('/api/articles', { params })
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
        const response = await api.get('/api/categories')
        this.categories = response.data
      } catch (error) {
        console.error('Error loading categories:', error)
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
    
    async loadFeeds() {
      this.feedsLoading = true
      try {
        const response = await api.get('/api/feeds')
        this.feeds = response.data
      } catch (error) {
        console.error('Error loading feeds:', error)
      } finally {
        this.feedsLoading = false
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
    },
    
    selectFeed(feedId) {
      this.selectedFeedId = feedId
      this.currentPage = 1
      this.loadArticles()
      // Close sidebar on mobile
      if (window.innerWidth < 1024) {
        this.sidebarOpen = false
      }
    },
    
    getSelectedFeedName() {
      if (!this.selectedFeedId) return 'All Articles'
      const feed = this.feeds.find(f => f.id === this.selectedFeedId)
      return feed ? feed.name : 'Unknown Feed'
    },

    async refreshFeeds() {
      this.refreshing = true
      try {
        await api.post('/api/refresh-feeds')
        await this.loadFeeds()
        await this.loadArticles()
        await this.loadStats()
      } catch (error) {
        alert('Failed to refresh feeds!')
        console.error('Error refreshing feeds:', error)
      } finally {
        this.refreshing = false
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