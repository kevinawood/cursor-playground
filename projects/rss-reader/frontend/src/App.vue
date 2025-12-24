<template>
  <div class="min-h-screen transition-colors duration-200" :class="darkMode ? 'bg-[#111111]' : 'bg-white'">
    <!-- Navigation - Minimal Clean Style -->
    <nav class="sticky top-0 z-40 border-b transition-colors duration-200" 
         :class="darkMode ? 'bg-[#111111] border-[#262626]' : 'bg-white border-gray-200'">
      <div class="max-w-5xl mx-auto px-6">
        <div class="flex justify-between h-14">
          <div class="flex items-center">
            <router-link to="/" class="flex items-center space-x-3">
              <div class="w-8 h-8 rounded-lg flex items-center justify-center bg-blue-600">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 5c7.18 0 13 5.82 13 13M6 11a7 7 0 017 7m-6 0a1 1 0 11-2 0 1 1 0 012 0z"></path>
                </svg>
              </div>
              <span class="text-base font-semibold" :class="darkMode ? 'text-white' : 'text-gray-900'">Reader</span>
            </router-link>
          </div>
          
          <div class="hidden sm:flex items-center space-x-1">
            <router-link
              to="/"
              class="px-3 py-1.5 text-sm font-medium rounded-md transition-colors"
              :class="darkMode 
                ? 'text-gray-400 hover:text-white hover:bg-white/5' 
                : 'text-gray-500 hover:text-gray-900 hover:bg-gray-100'"
              active-class="!text-blue-600 !bg-blue-50 dark:!bg-blue-500/10"
            >
              Articles
            </router-link>
            <router-link
              to="/bookmarks"
              class="px-3 py-1.5 text-sm font-medium rounded-md transition-colors"
              :class="darkMode 
                ? 'text-gray-400 hover:text-white hover:bg-white/5' 
                : 'text-gray-500 hover:text-gray-900 hover:bg-gray-100'"
              active-class="!text-blue-600 !bg-blue-50 dark:!bg-blue-500/10"
            >
              Bookmarks
            </router-link>
            <router-link
              to="/feeds"
              class="px-3 py-1.5 text-sm font-medium rounded-md transition-colors"
              :class="darkMode 
                ? 'text-gray-400 hover:text-white hover:bg-white/5' 
                : 'text-gray-500 hover:text-gray-900 hover:bg-gray-100'"
              active-class="!text-blue-600 !bg-blue-50 dark:!bg-blue-500/10"
            >
              Feeds
            </router-link>
          </div>

          <div class="flex items-center space-x-2">
            <button
              @click="toggleDarkMode"
              class="p-2 rounded-md transition-colors"
              :class="darkMode 
                ? 'text-gray-400 hover:text-white hover:bg-white/5' 
                : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'"
            >
              <svg v-if="darkMode" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Mobile Navigation -->
      <div class="sm:hidden border-t" :class="darkMode ? 'border-[#262626]' : 'border-gray-100'">
        <div class="flex justify-around">
          <router-link
            to="/"
            class="flex-1 flex flex-col items-center py-2 text-xs font-medium transition-colors"
            :class="darkMode ? 'text-gray-500' : 'text-gray-400'"
            active-class="!text-blue-600"
          >
            <svg class="w-5 h-5 mb-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path>
            </svg>
            Articles
          </router-link>
          <router-link
            to="/bookmarks"
            class="flex-1 flex flex-col items-center py-2 text-xs font-medium transition-colors"
            :class="darkMode ? 'text-gray-500' : 'text-gray-400'"
            active-class="!text-blue-600"
          >
            <svg class="w-5 h-5 mb-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
            </svg>
            Saved
          </router-link>
          <router-link
            to="/feeds"
            class="flex-1 flex flex-col items-center py-2 text-xs font-medium transition-colors"
            :class="darkMode ? 'text-gray-500' : 'text-gray-400'"
            active-class="!text-blue-600"
          >
            <svg class="w-5 h-5 mb-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 5c7.18 0 13 5.82 13 13M6 11a7 7 0 017 7m-6 0a1 1 0 11-2 0 1 1 0 012 0z"></path>
            </svg>
            Feeds
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Main content -->
    <main class="max-w-5xl mx-auto py-8 px-6">
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
    const savedDarkMode = localStorage.getItem('darkMode')
    if (savedDarkMode !== null) {
      this.darkMode = JSON.parse(savedDarkMode)
    } else {
      this.darkMode = window.matchMedia('(prefers-color-scheme: dark)').matches
    }
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
