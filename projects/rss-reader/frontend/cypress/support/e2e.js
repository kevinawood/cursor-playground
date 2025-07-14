// Import commands.js using ES2015 syntax:
import './commands'

// Alternatively you can use CommonJS syntax:
// require('./commands')

// Add custom commands here
Cypress.Commands.add('login', () => {
  // Add login logic if needed
})

Cypress.Commands.add('addFeed', (name, url, category = 'Technology') => {
  cy.request('POST', 'http://localhost:5001/api/feeds', {
    name,
    url,
    category
  })
})

Cypress.Commands.add('markArticleAsRead', (articleId) => {
  cy.request('PUT', `http://localhost:5001/api/articles/${articleId}/read`)
}) 