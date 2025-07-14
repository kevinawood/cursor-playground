import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../../src/views/Home.vue'

// Mock axios
vi.mock('axios', () => ({
  default: {
    get: vi.fn(),
    put: vi.fn()
  }
}))

describe('Home', () => {
  let router

  beforeEach(() => {
    router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', component: Home }
      ]
    })
  })

  it('renders loading state initially', () => {
    const wrapper = mount(Home, {
      global: {
        plugins: [router]
      }
    })
    
    expect(wrapper.text()).toContain('Loading')
  })

  it('displays articles when loaded', async () => {
    const mockArticles = [
      {
        id: 1,
        title: 'Test Article 1',
        link: 'https://example.com/1',
        description: 'Description 1',
        published_date: '2023-12-01T10:00:00Z',
        author: 'Author 1',
        is_read: false,
        feed: { name: 'Feed 1' }
      },
      {
        id: 2,
        title: 'Test Article 2',
        link: 'https://example.com/2',
        description: 'Description 2',
        published_date: '2023-12-01T11:00:00Z',
        author: 'Author 2',
        is_read: true,
        feed: { name: 'Feed 2' }
      }
    ]

    const wrapper = mount(Home, {
      global: {
        plugins: [router]
      }
    })

    // Mock the data
    await wrapper.setData({
      articles: mockArticles,
      loading: false
    })

    expect(wrapper.text()).toContain('Test Article 1')
    expect(wrapper.text()).toContain('Test Article 2')
  })

  it('shows stats correctly', async () => {
    const wrapper = mount(Home, {
      global: {
        plugins: [router]
      }
    })

    await wrapper.setData({
      stats: {
        total_feeds: 5,
        total_articles: 100,
        unread_articles: 25,
        read_articles: 75
      }
    })

    expect(wrapper.text()).toContain('5')
    expect(wrapper.text()).toContain('100')
    expect(wrapper.text()).toContain('25')
  })

  it('filters articles by search term', async () => {
    const mockArticles = [
      {
        id: 1,
        title: 'JavaScript Article',
        link: 'https://example.com/1',
        description: 'About JavaScript',
        published_date: '2023-12-01T10:00:00Z',
        author: 'Author 1',
        is_read: false,
        feed: { name: 'Feed 1' }
      },
      {
        id: 2,
        title: 'Python Article',
        link: 'https://example.com/2',
        description: 'About Python',
        published_date: '2023-12-01T11:00:00Z',
        author: 'Author 2',
        is_read: true,
        feed: { name: 'Feed 2' }
      }
    ]

    const wrapper = mount(Home, {
      global: {
        plugins: [router]
      }
    })

    await wrapper.setData({
      articles: mockArticles,
      loading: false,
      searchTerm: 'JavaScript'
    })

    expect(wrapper.text()).toContain('JavaScript Article')
    expect(wrapper.text()).not.toContain('Python Article')
  })

  it('filters articles by read status', async () => {
    const mockArticles = [
      {
        id: 1,
        title: 'Unread Article',
        link: 'https://example.com/1',
        description: 'Unread',
        published_date: '2023-12-01T10:00:00Z',
        author: 'Author 1',
        is_read: false,
        feed: { name: 'Feed 1' }
      },
      {
        id: 2,
        title: 'Read Article',
        link: 'https://example.com/2',
        description: 'Read',
        published_date: '2023-12-01T11:00:00Z',
        author: 'Author 2',
        is_read: true,
        feed: { name: 'Feed 2' }
      }
    ]

    const wrapper = mount(Home, {
      global: {
        plugins: [router]
      }
    })

    await wrapper.setData({
      articles: mockArticles,
      loading: false,
      filter: 'unread'
    })

    expect(wrapper.text()).toContain('Unread Article')
    expect(wrapper.text()).not.toContain('Read Article')
  })

  it('handles pagination correctly', async () => {
    const mockArticles = Array.from({ length: 25 }, (_, i) => ({
      id: i + 1,
      title: `Article ${i + 1}`,
      link: `https://example.com/${i + 1}`,
      description: `Description ${i + 1}`,
      published_date: '2023-12-01T10:00:00Z',
      author: 'Author',
      is_read: false,
      feed: { name: 'Feed' }
    }))

    const wrapper = mount(Home, {
      global: {
        plugins: [router]
      }
    })

    await wrapper.setData({
      articles: mockArticles,
      loading: false,
      currentPage: 1,
      itemsPerPage: 10
    })

    // Should show first 10 articles
    expect(wrapper.text()).toContain('Article 1')
    expect(wrapper.text()).toContain('Article 10')
    expect(wrapper.text()).not.toContain('Article 11')
  })

  it('marks article as read when clicked', async () => {
    const mockArticles = [
      {
        id: 1,
        title: 'Test Article',
        link: 'https://example.com/1',
        description: 'Test',
        published_date: '2023-12-01T10:00:00Z',
        author: 'Author',
        is_read: false,
        feed: { name: 'Feed' }
      }
    ]

    const wrapper = mount(Home, {
      global: {
        plugins: [router]
      }
    })

    await wrapper.setData({
      articles: mockArticles,
      loading: false
    })

    // Mock the markAsRead method
    const markAsReadSpy = vi.spyOn(wrapper.vm, 'markAsRead')
    
    await wrapper.find('.article-card').trigger('click')
    
    expect(markAsReadSpy).toHaveBeenCalledWith(mockArticles[0])
  })
}) 