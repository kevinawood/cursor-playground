<template>
  <div>
    <!-- Header -->
    <div class="sm:flex sm:items-center mb-8">
      <div class="sm:flex-auto">
        <h1 class="text-2xl font-semibold" :class="darkMode ? 'text-white' : 'text-gray-900'">Feeds</h1>
        <p class="mt-1 text-sm" :class="darkMode ? 'text-gray-400' : 'text-gray-500'">
          Manage your RSS subscriptions
        </p>
      </div>
      <div class="mt-4 sm:mt-0">
        <button
          @click="showAddModal = true"
          class="inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 transition-colors"
        >
          Add Feed
        </button>
      </div>
    </div>

    <!-- Feed Search Section -->
    <div class="rounded-xl border p-6 mb-8" :class="darkMode ? 'bg-[#1a1a1a] border-[#262626]' : 'bg-white border-gray-200'">
      <h3 class="text-sm font-medium mb-4" :class="darkMode ? 'text-white' : 'text-gray-900'">Search for RSS Feeds</h3>
      <div class="flex gap-3">
        <input
          v-model="searchQuery"
          @keyup.enter="searchFeeds"
          type="text"
          placeholder="Search for a website, magazine, or RSS feed..."
          class="flex-1 px-4 py-2 text-sm rounded-lg border transition-colors"
          :class="darkMode 
            ? 'bg-[#111111] border-[#262626] text-white placeholder-gray-500 focus:border-blue-500' 
            : 'bg-white border-gray-200 text-gray-900 placeholder-gray-400 focus:border-blue-500'"
        />
        <button
          @click="searchFeeds"
          :disabled="searching"
          class="px-4 py-2 text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          {{ searching ? 'Searching...' : 'Search' }}
        </button>
      </div>

      <!-- Search Results -->
      <div v-if="searchResults.length > 0" class="mt-6 space-y-2">
        <h4 class="text-xs font-medium uppercase tracking-wide mb-3" :class="darkMode ? 'text-gray-500' : 'text-gray-400'">Results</h4>
        <div
          v-for="feed in searchResults"
          :key="feed.url"
          class="flex items-center justify-between p-4 rounded-lg border transition-colors"
          :class="darkMode ? 'border-[#262626] hover:bg-[#222]' : 'border-gray-100 hover:bg-gray-50'"
        >
          <div class="flex items-center space-x-3">
            <img
              v-if="feed.favicon"
              :src="feed.favicon"
              :alt="feed.title"
              class="w-6 h-6 rounded"
              @error="$event.target.style.display='none'"
            />
            <div>
              <h5 class="text-sm font-medium" :class="darkMode ? 'text-white' : 'text-gray-900'">{{ feed.title }}</h5>
              <p v-if="feed.website" class="text-xs" :class="darkMode ? 'text-gray-500' : 'text-gray-400'">{{ feed.website }}</p>
            </div>
          </div>
          <button
            @click="addFeedFromSearch(feed)"
            :disabled="addingFeed === feed.url"
            class="px-3 py-1 text-xs font-medium rounded-md transition-colors disabled:opacity-50"
            :class="darkMode ? 'text-blue-400 bg-blue-500/10 hover:bg-blue-500/20' : 'text-blue-600 bg-blue-50 hover:bg-blue-100'"
          >
            {{ addingFeed === feed.url ? 'Adding...' : 'Add' }}
          </button>
        </div>
      </div>

      <!-- No Results -->
      <div v-else-if="searched && searchResults.length === 0" class="mt-6 text-center py-4">
        <p class="text-sm" :class="darkMode ? 'text-gray-500' : 'text-gray-400'">No RSS feeds found for "{{ searchQuery }}"</p>
      </div>
    </div>

    <!-- Feeds list -->
    <div>
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-2 border-blue-600 border-t-transparent mx-auto"></div>
        <p class="mt-4 text-sm" :class="darkMode ? 'text-gray-500' : 'text-gray-400'">Loading feeds...</p>
      </div>

      <div v-else-if="loadError" class="text-center py-12">
        <svg class="mx-auto h-10 w-10" :class="darkMode ? 'text-red-400' : 'text-red-500'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
        </svg>
        <h3 class="mt-3 text-sm font-medium" :class="darkMode ? 'text-white' : 'text-gray-900'">Error loading feeds</h3>
        <p class="mt-1 text-sm" :class="darkMode ? 'text-gray-400' : 'text-gray-500'">There was a problem loading your feeds.</p>
        <div class="mt-4">
          <button
            @click="retryLoadFeeds"
            class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            Retry
          </button>
        </div>
      </div>

      <div v-else-if="feeds.length === 0" class="text-center py-12">
        <svg class="mx-auto h-10 w-10" :class="darkMode ? 'text-gray-600' : 'text-gray-300'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 5c7.18 0 13 5.82 13 13M6 11a7 7 0 017 7m-6 0a1 1 0 11-2 0 1 1 0 012 0z"></path>
        </svg>
        <h3 class="mt-3 text-sm font-medium" :class="darkMode ? 'text-white' : 'text-gray-900'">No feeds yet</h3>
        <p class="mt-1 text-sm" :class="darkMode ? 'text-gray-400' : 'text-gray-500'">Get started by adding your first RSS feed.</p>
        <div class="mt-4">
          <button
            @click="showAddModal = true"
            class="px-4 py-2 text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 transition-colors"
          >
            Add Feed
          </button>
        </div>
      </div>

      <div v-else class="space-y-2">
        <div v-for="feed in feeds" :key="feed.id" 
             class="flex items-center justify-between p-4 rounded-xl border transition-colors"
             :class="darkMode ? 'bg-[#1a1a1a] border-[#262626] hover:bg-[#222]' : 'bg-white border-gray-200 hover:border-gray-300'">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-3">
              <h3 class="text-sm font-medium truncate" :class="darkMode ? 'text-white' : 'text-gray-900'">
                {{ feed.name }}
              </h3>
              <span class="px-2 py-0.5 text-xs font-medium rounded-md"
                    :class="darkMode ? 'bg-blue-500/10 text-blue-400' : 'bg-blue-50 text-blue-600'">
                {{ feed.category }}
              </span>
            </div>
            <div class="mt-1.5 flex items-center gap-2 text-xs" :class="darkMode ? 'text-gray-500' : 'text-gray-400'">
              <span class="truncate max-w-xs">{{ feed.url }}</span>
              <span>•</span>
              <span>{{ feed.article_count }} articles</span>
              <span v-if="feed.last_fetched">•</span>
              <span v-if="feed.last_fetched">{{ formatDate(feed.last_fetched) }}</span>
            </div>
          </div>
          <button
            @click="deleteFeed(feed)"
            class="ml-4 px-3 py-1.5 text-xs font-medium rounded-md transition-colors"
            :class="darkMode ? 'text-red-400 hover:bg-red-500/10' : 'text-red-600 hover:bg-red-50'"
          >
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- Add Feed Modal -->
    <div v-if="showAddModal" class="fixed inset-0 flex items-center justify-center p-4 z-50" :class="darkMode ? 'bg-black/80' : 'bg-black/50'">
      <div class="rounded-xl max-w-md w-full p-6" :class="darkMode ? 'bg-[#1a1a1a] border border-[#262626]' : 'bg-white'">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg font-semibold" :class="darkMode ? 'text-white' : 'text-gray-900'">Add RSS Feed</h3>
          <button
            @click="showAddModal = false"
            class="p-1 rounded-md transition-colors"
            :class="darkMode ? 'text-gray-400 hover:text-white hover:bg-white/10' : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="addFeed">
          <div class="space-y-4">
            <div>
              <label for="feed-name" class="block text-sm font-medium text-gray-700">Feed Name</label>
              <input
                id="feed-name"
                v-model="newFeed.name"
                type="text"
                required
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="e.g., TechCrunch"
              />
            </div>
            
            <div>
              <label for="feed-url" class="block text-sm font-medium text-gray-700">RSS URL</label>
              <input
                id="feed-url"
                v-model="newFeed.url"
                type="url"
                required
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="https://example.com/feed.xml"
              />
            </div>
            
            <div>
              <label for="feed-category" class="block text-sm font-medium text-gray-700">Category</label>
              <select
                id="feed-category"
                v-model="newFeed.category"
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value="General">General</option>
                <option value="Technology">Technology</option>
                <option value="News">News</option>
                <option value="Sports">Sports</option>
                <option value="Entertainment">Entertainment</option>
                <option value="Science">Science</option>
                <option value="Business">Business</option>
                <option value="Politics">Politics</option>
              </select>
            </div>
          </div>
          
          <div class="mt-6 flex justify-end space-x-3">
            <button
              type="button"
              @click="showAddModal = false"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="adding"
              class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 disabled:opacity-50"
            >
              {{ adding ? 'Adding...' : 'Add Feed' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../config/axios'

export default {
  name: 'Feeds',
  props: {
    darkMode: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      feeds: [],
      loading: true,
      loadError: false,
      retryCount: 0,
      maxRetries: 3,
      showAddModal: false,
      adding: false,
      newFeed: {
        name: '',
        url: '',
        category: 'General'
      },
      // Search functionality
      searchQuery: '',
      searchResults: [],
      searching: false,
      searched: false,
      addingFeed: null
    }
  },
  async mounted() {
    await this.loadFeeds()
  },
  methods: {
    async loadFeeds(isRetry = false) {
      if (!isRetry) {
        this.loading = true
        this.loadError = false
        this.retryCount = 0
      }
      
      try {
        const response = await api.get('/api/feeds')
        this.feeds = response.data
        this.loadError = false
        this.retryCount = 0
      } catch (error) {
        console.error('Error loading feeds:', error)
        
        // Auto-retry on failure (handles race conditions with backend scheduler)
        if (this.retryCount < this.maxRetries) {
          this.retryCount++
          console.log(`Retrying feed load (attempt ${this.retryCount}/${this.maxRetries})...`)
          // Exponential backoff: 500ms, 1000ms, 2000ms
          await new Promise(resolve => setTimeout(resolve, 500 * Math.pow(2, this.retryCount - 1)))
          return this.loadFeeds(true)
        }
        
        this.loadError = true
      } finally {
        this.loading = false
      }
    },
    
    async retryLoadFeeds() {
      this.retryCount = 0
      await this.loadFeeds()
    },

    async searchFeeds() {
      if (!this.searchQuery.trim()) return
      
      console.log('Searching for:', this.searchQuery)
      this.searching = true
      this.searched = true
      try {
        const response = await api.get(`/api/feed-search?q=${encodeURIComponent(this.searchQuery)}`)
        this.searchResults = response.data.feeds || []
      } catch (error) {
        console.error('Error searching feeds:', error)
        this.searchResults = []
      } finally {
        this.searching = false
      }
    },

    async addFeedFromSearch(feed) {
      this.addingFeed = feed.url
      try {
        // Determine category based on feed title/description
        let category = 'General'
        const title = feed.title.toLowerCase()
        const description = (feed.description || '').toLowerCase()
        
        if (title.includes('tech') || description.includes('tech')) category = 'Technology'
        else if (title.includes('news') || description.includes('news')) category = 'News'
        else if (title.includes('sport') || description.includes('sport')) category = 'Sports'
        else if (title.includes('entertainment') || description.includes('entertainment')) category = 'Entertainment'
        else if (title.includes('science') || description.includes('science')) category = 'Science'
        else if (title.includes('business') || description.includes('business')) category = 'Business'
        else if (title.includes('politic') || description.includes('politic')) category = 'Politics'

        const response = await api.post('/api/feeds', {
          name: feed.title,
          url: feed.url,
          category: category
        })
        
        // Add to feeds list
        this.feeds.push({
          id: response.data.id,
          name: response.data.name,
          url: response.data.url,
          category: response.data.category,
          last_fetched: response.data.last_fetched,
          article_count: 0,
          logo_url: feed.favicon
        })
        
        // Remove from search results
        this.searchResults = this.searchResults.filter(f => f.url !== feed.url)
        
        // Clear search if no more results
        if (this.searchResults.length === 0) {
          this.searchQuery = ''
          this.searched = false
        }
      } catch (error) {
        console.error('Error adding feed:', error)
        alert('Failed to add feed. It might already exist or be invalid.')
      } finally {
        this.addingFeed = null
      }
    },

    async addFeed() {
      this.adding = true
      try {
        const response = await api.post('/api/feeds', this.newFeed)
        this.feeds.push({
          id: response.data.id,
          name: response.data.name,
          url: response.data.url,
          category: response.data.category,
          last_fetched: response.data.last_fetched,
          article_count: 0
        })
        this.showAddModal = false
        this.newFeed = { name: '', url: '', category: 'General' }
      } catch (error) {
        console.error('Error adding feed:', error)
        alert('Failed to add feed. It might already exist or be invalid.')
      } finally {
        this.adding = false
      }
    },

    async deleteFeed(feed) {
      if (!confirm(`Are you sure you want to delete "${feed.name}"?`)) return
      
      try {
        await api.delete(`/api/feeds/${feed.id}`)
        this.feeds = this.feeds.filter(f => f.id !== feed.id)
      } catch (error) {
        console.error('Error deleting feed:', error)
        alert('Failed to delete feed.')
      }
    },

    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      const now = new Date()
      const diffInMinutes = Math.floor((now - date) / (1000 * 60))
      
      if (diffInMinutes < 60) return `${diffInMinutes}m ago`
      if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`
      return `${Math.floor(diffInMinutes / 1440)}d ago`
    }
  }
}
</script>