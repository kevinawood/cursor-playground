<template>
  <div class="min-h-screen transition-colors duration-200" :class="darkMode ? 'bg-gray-900' : 'bg-gray-50'">
    <!-- Navigation -->
    <nav class="transition-colors duration-200 sticky top-0 z-40" :class="darkMode ? 'bg-gray-800 shadow-lg border-gray-700' : 'bg-white shadow-sm border-b'">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-14 sm:h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-lg sm:text-xl font-bold transition-colors duration-200" :class="darkMode ? 'text-white' : 'text-gray-900'">
                RSS Reader
              </h1>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link
                to="/"
                class="transition-colors duration-200 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="darkMode 
                  ? 'border-transparent text-gray-300 hover:border-gray-600 hover:text-white' 
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
                active-class="border-indigo-500 text-indigo-600"
              >
                Articles
              </router-link>
              <router-link
                to="/bookmarks"
                class="transition-colors duration-200 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="darkMode 
                  ? 'border-transparent text-gray-300 hover:border-gray-600 hover:text-white' 
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
                active-class="border-indigo-500 text-indigo-600"
              >
                Bookmarks
              </router-link>
              <router-link
                to="/feeds"
                class="transition-colors duration-200 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="darkMode 
                  ? 'border-transparent text-gray-300 hover:border-gray-600 hover:text-white' 
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
                active-class="border-indigo-500 text-indigo-600"
              >
                Feeds
              </router-link>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <!-- Dark mode toggle -->
            <button
              @click="toggleDarkMode"
              class="p-2 rounded-lg transition-colors duration-200"
              :class="darkMode 
                ? 'text-gray-300 hover:text-white hover:bg-gray-700' 
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'"
              :title="darkMode ? 'Switch to light mode' : 'Switch to dark mode'"
            >
              <svg v-if="darkMode" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
              </svg>
            </button>
            <div class="flex-shrink-0 hidden sm:block">
              <span class="text-xs sm:text-sm transition-colors duration-200" :class="darkMode ? 'text-gray-400' : 'text-gray-500'">
                Auto-refresh every 5 minutes
              </span>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Main content -->
    <main class="max-w-7xl mx-auto py-4 sm:py-6 sm:px-6 lg:px-8">
      <router-view :darkMode="darkMode" />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      darkMode: false
    }
  },
  mounted() {
    // Load dark mode preference from localStorage
    const savedDarkMode = localStorage.getItem('darkMode')
    if (savedDarkMode !== null) {
      this.darkMode = JSON.parse(savedDarkMode)
    } else {
      // Check system preference
      this.darkMode = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
    
    // Apply dark mode to document
    this.applyDarkMode()
  },
  methods: {
    toggleDarkMode() {
      this.darkMode = !this.darkMode
      localStorage.setItem('darkMode', JSON.stringify(this.darkMode))
      this.applyDarkMode()
    },
    applyDarkMode() {
      if (this.darkMode) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }
  }
}
</script> 