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
      }
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
    
    async addFeed() {
      this.adding = true
      try {
        await axios.post('/api/feeds', this.newFeed)
        this.showAddModal = false
        this.newFeed = { name: '', url: '', category: 'General' }
        await this.loadFeeds()
      } catch (error) {
        console.error('Error adding feed:', error)
        alert(error.response?.data?.error || 'Error adding feed')
      } finally {
        this.adding = false
      }
    },
    
    async deleteFeed(feed) {
      if (confirm(`Are you sure you want to delete "${feed.name}"?`)) {
        try {
          await axios.delete(`/api/feeds/${feed.id}`)
          await this.loadFeeds()
        } catch (error) {
          console.error('Error deleting feed:', error)
          alert('Error deleting feed')
        }
      }
    },
    
    formatDate(dateString) {
      if (!dateString) return 'Never'
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    }
  }
}
</script> 