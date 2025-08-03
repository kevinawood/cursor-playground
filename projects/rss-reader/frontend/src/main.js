import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './style.css'

// Components
import Home from './views/Home.vue'
import Feeds from './views/Feeds.vue'
import Bookmarks from './views/Bookmarks.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/feeds', component: Feeds },
  { path: '/bookmarks', component: Bookmarks }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app') 