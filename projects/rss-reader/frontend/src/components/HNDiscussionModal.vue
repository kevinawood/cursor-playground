<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto" @click="closeModal">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 transition-opacity" :class="darkMode ? 'bg-gray-900 bg-opacity-75' : 'bg-gray-500 bg-opacity-75'"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom transition-all transform rounded-lg text-left overflow-hidden shadow-xl sm:my-8 sm:align-middle sm:max-w-lg sm:w-full transition-colors duration-200" :class="darkMode ? 'bg-gray-800' : 'bg-white'" @click.stop>
        <div class="px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-orange-100 sm:mx-0 sm:h-10 sm:w-10">
              <svg class="h-6 w-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
              </svg>
            </div>
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
              <h3 class="text-lg leading-6 font-medium transition-colors duration-200" :class="darkMode ? 'text-white' : 'text-gray-900'">
                Hacker News Article
              </h3>
              <div class="mt-2">
                <p class="text-sm transition-colors duration-200" :class="darkMode ? 'text-gray-300' : 'text-gray-500'">
                  This article is from Hacker News. Would you like to:
                </p>
                <p class="mt-2 text-sm font-medium transition-colors duration-200" :class="darkMode ? 'text-white' : 'text-gray-900'">
                  {{ modalContent.title }}
                </p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <!-- View Discussion Button -->
          <button
            type="button"
            @click="openDiscussion"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-orange-600 text-base font-medium text-white hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 sm:ml-3 sm:w-auto sm:text-sm transition-colors duration-200"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
            View Discussion
          </button>
          
          <!-- Read Article Button -->
          <button
            type="button"
            @click="openArticle"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm transition-colors duration-200"
            :class="darkMode ? 'border-gray-600 bg-gray-700 text-gray-300 hover:bg-gray-600' : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'"
          >
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
            </svg>
            Read Article
          </button>
          
          <!-- Cancel Button -->
          <button
            type="button"
            @click="closeModal"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm transition-colors duration-200"
            :class="darkMode ? 'border-gray-600 text-gray-300 hover:bg-gray-600' : 'border-gray-300 text-gray-700 hover:bg-gray-50'"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HNDiscussionModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    modalContent: {
      type: Object,
      default: () => ({
        title: '',
        originalUrl: '',
        discussionUrl: '',
        searchUrl: '',
        feedName: ''
      })
    },
    darkMode: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    closeModal() {
      this.$emit('close')
    },
    
    openDiscussion() {
      // Open the discussion URL
      const url = this.modalContent.discussionUrl
      if (url) {
        window.open(url, '_blank')
      }
      this.$emit('choice-made', 'discussion')
      this.closeModal()
    },
    
    openArticle() {
      window.open(this.modalContent.originalUrl, '_blank')
      this.$emit('choice-made', 'article')
      this.closeModal()
    }
  }
}
</script> 