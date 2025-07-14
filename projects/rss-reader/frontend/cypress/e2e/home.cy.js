describe('Home Page', () => {
  beforeEach(() => {
    cy.visit('/')
  })

  it('should display the RSS reader title', () => {
    cy.get('h1').should('contain', 'RSS Reader')
  })

  it('should show loading state initially', () => {
    cy.get('[data-testid="loading"]').should('be.visible')
  })

  it('should display articles after loading', () => {
    // Wait for articles to load
    cy.get('[data-testid="article-card"]', { timeout: 10000 }).should('exist')
  })

  it('should display stats information', () => {
    cy.get('[data-testid="stats"]').should('exist')
    cy.get('[data-testid="total-feeds"]').should('exist')
    cy.get('[data-testid="total-articles"]').should('exist')
    cy.get('[data-testid="unread-articles"]').should('exist')
  })

  it('should filter articles by search term', () => {
    cy.get('[data-testid="search-input"]').type('test')
    cy.get('[data-testid="article-card"]').should('contain', 'test')
  })

  it('should filter articles by read status', () => {
    cy.get('[data-testid="filter-unread"]').click()
    cy.get('[data-testid="article-card"]').should('not.have.class', 'read')
  })

  it('should mark article as read when clicked', () => {
    cy.get('[data-testid="article-card"]').first().click()
    cy.get('[data-testid="article-card"]').first().should('have.class', 'read')
  })

  it('should open article in new tab when external link is clicked', () => {
    cy.get('[data-testid="external-link"]').first().click()
    // Note: Cypress can't test opening in new tab, but we can verify the link exists
    cy.get('[data-testid="external-link"]').first().should('have.attr', 'target', '_blank')
  })

  it('should navigate through pages', () => {
    // Assuming there are multiple pages
    cy.get('[data-testid="pagination"]').should('exist')
    cy.get('[data-testid="next-page"]').click()
    cy.url().should('include', 'page=2')
  })

  it('should display sidebar with feeds', () => {
    cy.get('[data-testid="sidebar"]').should('exist')
    cy.get('[data-testid="feed-item"]').should('exist')
  })

  it('should filter articles by selected feed', () => {
    cy.get('[data-testid="feed-item"]').first().click()
    cy.get('[data-testid="selected-feed"]').should('contain', 'Feed')
  })
}) 