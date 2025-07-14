<template>
  <div class="px-4 sm:px-6 lg:px-8">
    <!-- Header -->
    <div class="sm:flex sm:items-center">
      <div class="sm:flex-auto">
        <h1 class="text-2xl font-semibold text-gray-900">RSS Feeds</h1>
        <p class="mt-2 text-sm text-gray-700">
          Manage your RSS feed subscriptions
        </p>
      </div>
      <div class="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
        <button
          @click="showAddModal = true"
          class="inline-flex items-center justify-center rounded-md border border-transparent bg-indigo-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 sm:w-auto"
        >
          Add Feed
        </button>
      </div>
    </div>

    <!-- Feed Search Section -->
    <div class="mt-8 bg-white shadow sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg font-medium leading-6 text-gray-900 mb-4">Search for RSS Feeds</h3>
        <div class="flex gap-3">
          <div class="flex-1">
            <input
              v-model="searchQuery"
              @keyup.enter="searchFeeds"
              type="text"
              placeholder="Search for a website, magazine, or RSS feed..."
              class="block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
          <button
            @click="searchFeeds"
            :disabled="searching"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            {{ searching ? 'Searching...' : 'Search' }}
          </button>
        </div>

        <!-- Search Results -->
        <div v-if="searchResults.length > 0" class="mt-6">
          <h4 class="text-sm font-medium text-gray-900 mb-3">Search Results</h4>
          <div class="space-y-3">
            <div
              v-for="feed in searchResults"
              :key="feed.url"
              class="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
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
                  <h5 class="text-sm font-medium text-gray-900">{{ feed.title }}</h5>
                  <p v-if="feed.website" class="text-xs text-gray-500">{{ feed.website }}</p>
                  <p v-if="feed.description" class="text-xs text-gray-600 mt-1">{{ feed.description }}</p>
                </div>
              </div>
              <button
                @click="addFeedFromSearch(feed)"
                :disabled="addingFeed === feed.url"
                class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {{ addingFeed === feed.url ? 'Adding...' : 'Add' }}
              </button>
            </div>
          </div>
        </div>

        <!-- No Results -->
        <div v-else-if="searched && searchResults.length === 0" class="mt-6 text-center py-4">
          <p class="text-sm text-gray-500">No RSS feeds found for "{{ searchQuery }}"</p>
        </div>
      </div>
    </div>

    <!-- Feeds list -->
    <div class="mt-8">
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
        <p class="mt-4 text-gray-500">Loading feeds...</p>
      </div>

      <div v-else-if="feeds.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 5c7.18 0 13 5.82 13 13M6 11a7 7 0 017 7m-6 0a1 1 0 11-2 0 1 1 0 012 0z"></path>
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No feeds</h3>
        <p class="mt-1 text-sm text-gray-500">Get started by adding your first RSS feed.</p>
        <div class="mt-6">
          <button
            @click="showAddModal = true"
            class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            Add Feed
          </button>
        </div>
      </div>

      <div v-else class="bg-white shadow overflow-hidden sm:rounded-md">
        <ul class="divide-y divide-gray-200">
          <li v-for="feed in feeds" :key="feed.id">
            <div class="px-4 py-4 sm:px-6">
              <div class="flex items-center justify-between">
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between">
                    <p class="text-sm font-medium text-indigo-600 truncate">
                      {{ feed.name }}
                    </p>
                    <div class="ml-2 flex-shrink-0 flex">
                      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        {{ feed.category }}
                      </span>
                    </div>
                  </div>
                  <div class="mt-2 flex">
                    <div class="flex items-center text-sm text-gray-500">
                      <span class="truncate">{{ feed.url }}</span>
                      <span class="mx-1">•</span>
                      <span>{{ feed.article_count }} articles</span>
                      <span v-if="feed.last_fetched" class="mx-1">•</span>
                      <span v-if="feed.last_fetched" class="truncate">
                        Last updated: {{ formatDate(feed.last_fetched) }}
                      </span>
                    </div>
                  </div>
                </div>
                <div class="ml-4 flex-shrink-0">
                  <button
                    @click="deleteFeed(feed)"
                    class="text-red-600 hover:text-red-900 text-sm font-medium"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Add Feed Modal -->
    <div v-if="showAddModal" class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg max-w-md w-full p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-medium text-gray-900">Add RSS Feed</h3>
          <button
            @click="showAddModal = false"
            class="text-gray-400 hover:text-gray-600"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
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
import axios from 'axios'

export default {
  name: 'Feeds',
  data() {
    return {
      feeds: [],
      loading: true,
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
    async loadFeeds() {
      this.loading = true
      try {
        const response = await axios.get('/api/feeds')
        this.feeds = response.data
      } catch (error) {
        console.error('Error loading feeds:', error)
      } finally {
        this.loading = false
      }
    },

    async searchFeeds() {
      if (!this.searchQuery.trim()) return
      
      this.searching = true
      this.searched = true
      try {
        const response = await axios.get(`/api/feed-search?q=${encodeURIComponent(this.searchQuery)}`)
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

        const response = await axios.post('/api/feeds', {
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
        const response = await axios.post('/api/feeds', this.newFeed)
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
        await axios.delete(`/api/feeds/${feed.id}`)
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