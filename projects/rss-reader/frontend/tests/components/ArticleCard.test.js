import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import ArticleCard from '../../src/components/ArticleCard.vue'

describe('ArticleCard', () => {
  const mockArticle = {
    id: 1,
    title: 'Test Article Title',
    link: 'https://example.com/article',
    description: 'This is a test article description',
    published_date: '2023-12-01T10:00:00Z',
    author: 'Test Author',
    is_read: false,
    feed: {
      name: 'Test Feed',
      logo_url: 'https://example.com/logo.png'
    }
  }

  it('renders article title correctly', () => {
    const wrapper = mount(ArticleCard, {
      props: { article: mockArticle }
    })
    
    expect(wrapper.text()).toContain('Test Article Title')
  })

  it('renders feed name correctly', () => {
    const wrapper = mount(ArticleCard, {
      props: { article: mockArticle }
    })
    
    expect(wrapper.text()).toContain('Test Feed')
  })

  it('shows unread indicator when article is unread', () => {
    const wrapper = mount(ArticleCard, {
      props: { article: mockArticle }
    })
    
    expect(wrapper.find('.unread-indicator').exists()).toBe(true)
  })

  it('hides unread indicator when article is read', () => {
    const readArticle = { ...mockArticle, is_read: true }
    const wrapper = mount(ArticleCard, {
      props: { article: readArticle }
    })
    
    expect(wrapper.find('.unread-indicator').exists()).toBe(false)
  })

  it('emits click event when article is clicked', async () => {
    const wrapper = mount(ArticleCard, {
      props: { article: mockArticle }
    })
    
    await wrapper.find('.article-card').trigger('click')
    
    expect(wrapper.emitted('click')).toBeTruthy()
    expect(wrapper.emitted('click')[0]).toEqual([mockArticle])
  })

  it('opens article link in new tab when external link is clicked', async () => {
    const wrapper = mount(ArticleCard, {
      props: { article: mockArticle }
    })
    
    // Mock window.open
    const mockOpen = vi.fn()
    global.open = mockOpen
    
    await wrapper.find('.external-link').trigger('click')
    
    expect(mockOpen).toHaveBeenCalledWith('https://example.com/article', '_blank')
  })

  it('formats date correctly', () => {
    const wrapper = mount(ArticleCard, {
      props: { article: mockArticle }
    })
    
    // Check that the date is formatted (should show relative time)
    expect(wrapper.text()).toContain('ago')
  })

  it('shows author when available', () => {
    const wrapper = mount(ArticleCard, {
      props: { article: mockArticle }
    })
    
    expect(wrapper.text()).toContain('Test Author')
  })

  it('handles missing author gracefully', () => {
    const articleWithoutAuthor = { ...mockArticle, author: null }
    const wrapper = mount(ArticleCard, {
      props: { article: articleWithoutAuthor }
    })
    
    expect(wrapper.text()).not.toContain('Test Author')
  })
}) 