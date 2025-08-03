/**
 * Hacker News utility functions
 */

// Detect if an article is from Hacker News
export function isHackerNewsArticle(article) {
  // Check if the feed name contains "Hacker News" or "HN"
  if (article.feed_name && (
    article.feed_name.toLowerCase().includes('hacker news') ||
    article.feed_name.toLowerCase().includes('hn')
  )) {
    return true
  }
  
  // Check if the article link contains HN patterns
  if (article.link && (
    article.link.includes('news.ycombinator.com') ||
    article.link.includes('ycombinator.com')
  )) {
    return true
  }
  
  return false
}

// Extract HN discussion URL from article link
export function getHNDiscussionUrl(articleLink) {
  // If it's already a discussion link, return as is
  if (articleLink.includes('news.ycombinator.com/item?id=')) {
    return articleLink
  }
  
  // Try to extract the HN item ID from the URL
  // HN discussion URLs are typically: https://news.ycombinator.com/item?id=12345678
  const urlMatch = articleLink.match(/news\.ycombinator\.com\/item\?id=(\d+)/)
  if (urlMatch) {
    return `https://news.ycombinator.com/item?id=${urlMatch[1]}`
  }
  
  // For external articles, we'll use the search approach instead
  // as direct URL matching is unreliable
  return null
}

// Get a more reliable discussion URL by searching HN
export function getHNDiscussionUrlBySearch(articleTitle, articleLink) {
  // Search HN for the article title
  const searchQuery = encodeURIComponent(articleTitle)
  return `https://hn.algolia.com/?q=${searchQuery}`
}

// Get the best discussion URL available
export function getBestDiscussionUrl(articleTitle, articleLink) {
  const directUrl = getHNDiscussionUrl(articleLink)
  if (directUrl) {
    return directUrl
  }
  
  // Fallback to search
  return getHNDiscussionUrlBySearch(articleTitle, articleLink)
}

// Format the HN discussion modal content
export function getHNModalContent(article) {
  const discussionUrl = getBestDiscussionUrl(article.title, article.link)
  
  return {
    title: article.title,
    originalUrl: article.link,
    discussionUrl: discussionUrl,
    searchUrl: discussionUrl, // Use the same URL for both
    feedName: article.feed_name
  }
} 