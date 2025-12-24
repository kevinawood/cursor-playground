<template>
  <div class="min-h-screen transition-colors duration-300" :class="darkMode ? 'bg-[#0f0f0f]' : 'bg-[#fafafa]'">
    <!-- Navigation - Modern Editorial Style -->
    <nav class="sticky top-0 z-40 backdrop-blur-lg transition-all duration-300" 
         :class="darkMode ? 'bg-[#0f0f0f]/80 border-b border-white/10' : 'bg-white/80 border-b border-black/5'">
      <div class="max-w-6xl mx-auto px-6 lg:px-8">
        <div class="flex justify-between h-16 sm:h-20">
          <div class="flex items-center">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="editorial-title text-xl sm:text-2xl font-bold transition-colors duration-200" 
                  :class="darkMode ? 'text-white' : 'text-gray-900'">
                <span class="bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-transparent">RSS</span>
                <span :class="darkMode ? 'text-white' : 'text-gray-900'"> Reader</span>
              </h1>
            </div>
            <div class="hidden sm:ml-12 sm:flex sm:space-x-2">
              <router-link
                to="/"
                class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
                :class="darkMode 
                  ? 'text-gray-400 hover:text-white hover:bg-white/10' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-black/5'"
                active-class="!bg-indigo-600 !text-white"
              >
                Articles
              </router-link>
              <router-link
                to="/bookmarks"
                class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
                :class="darkMode 
                  ? 'text-gray-400 hover:text-white hover:bg-white/10' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-black/5'"
                active-class="!bg-indigo-600 !text-white"
              >
                Bookmarks
              </router-link>
              <router-link
                to="/feeds"
                class="px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
                :class="darkMode 
                  ? 'text-gray-400 hover:text-white hover:bg-white/10' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-black/5'"
                active-class="!bg-indigo-600 !text-white"
              >
                Feeds
              </router-link>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <!-- Dark mode toggle -->
            <button
              @click="toggleDarkMode"
              class="p-2.5 rounded-xl transition-all duration-200"
              :class="darkMode 
                ? 'text-gray-400 hover:text-white hover:bg-white/10' 
                : 'text-gray-500 hover:text-gray-900 hover:bg-black/5'"
              :title="darkMode ? 'Switch to light mode' : 'Switch to dark mode'"
            >
              <svg v-if="darkMode" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
              </svg>
            </button>
            <div class="hidden sm:flex items-center">
              <span class="text-xs font-medium px-3 py-1.5 rounded-full transition-colors duration-200" 
                    :class="darkMode ? 'text-gray-500 bg-white/5' : 'text-gray-400 bg-black/5'">
                Auto-refresh: 5m
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Mobile Navigation -->
      <div class="sm:hidden border-t" :class="darkMode ? 'border-white/10' : 'border-black/5'">
        <div class="flex justify-around py-2">
          <router-link
            to="/"
            class="flex flex-col items-center px-4 py-2 text-xs font-medium transition-colors"
            :class="darkMode ? 'text-gray-400' : 'text-gray-500'"
            active-class="!text-indigo-600"
          >
            <svg class="w-5 h-5 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path>
            </svg>
            Articles
          </router-link>
          <router-link
            to="/bookmarks"
            class="flex flex-col items-center px-4 py-2 text-xs font-medium transition-colors"
            :class="darkMode ? 'text-gray-400' : 'text-gray-500'"
            active-class="!text-indigo-600"
          >
            <svg class="w-5 h-5 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"></path>
            </svg>
            Bookmarks
          </router-link>
          <router-link
            to="/feeds"
            class="flex flex-col items-center px-4 py-2 text-xs font-medium transition-colors"
            :class="darkMode ? 'text-gray-400' : 'text-gray-500'"
            active-class="!text-indigo-600"
          >
            <svg class="w-5 h-5 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 5c7.18 0 13 5.82 13 13M6 11a7 7 0 017 7m-6 0a1 1 0 11-2 0 1 1 0 012 0z"></path>
            </svg>
            Feeds
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Main content -->
    <main class="max-w-6xl mx-auto py-6 sm:py-10 px-4 sm:px-6 lg:px-8">
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
