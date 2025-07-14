# Testing Guide

This document provides comprehensive information about testing the RSS Reader application.

## 🧪 Test Structure

```
projects/rss-reader/
├── backend/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Pytest configuration
│   │   ├── test_models.py       # Database model tests
│   │   └── test_api.py          # API endpoint tests
│   └── requirements-test.txt    # Test dependencies
├── frontend/
│   ├── tests/
│   │   ├── setup.js             # Test setup
│   │   ├── components/          # Component tests
│   │   └── views/               # View tests
│   ├── cypress/
│   │   ├── e2e/                 # E2E tests
│   │   └── support/             # Cypress support
│   ├── vitest.config.js         # Vitest configuration
│   └── cypress.config.js        # Cypress configuration
└── scripts/
    └── test.sh                  # Test runner script
```

## 🚀 Quick Start

### Run All Tests
```bash
./scripts/test.sh
```

### Run Backend Tests Only
```bash
cd backend
source venv/bin/activate
pytest tests/ -v --cov=.
```

### Run Frontend Tests Only
```bash
cd frontend
npm run test
```

### Run E2E Tests
```bash
# Start the application first
./scripts/start.sh

# Then run E2E tests
cd frontend
npm run test:e2e
```

## 🔧 Backend Testing

### Test Types
- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test API endpoints and database interactions
- **Model Tests**: Test database models and relationships

### Test Coverage
- API endpoints (GET, POST, PUT, DELETE)
- Database models (Feed, Article)
- Data validation and error handling
- Background job functionality

### Running Backend Tests
```bash
cd backend

# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest tests/ -v --cov=. --cov-report=html

# Run tests in parallel
pytest tests/ -n auto
```

### Test Database
Tests use SQLite in-memory database to ensure isolation and speed.

## 🎨 Frontend Testing

### Test Types
- **Unit Tests**: Test individual Vue components
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test full user workflows

### Test Coverage
- Vue components (ArticleCard, FeedList, etc.)
- Vuex store actions and mutations
- Router navigation
- API integration
- User interactions

### Running Frontend Tests
```bash
cd frontend

# Install dependencies
npm install

# Run unit tests
npm run test

# Run tests with UI
npm run test:ui

# Run with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

### Test Environment
- **Vitest**: Fast unit testing framework
- **Vue Test Utils**: Vue component testing utilities
- **jsdom**: DOM environment for testing
- **Cypress**: E2E testing framework

## 🌐 E2E Testing

### Test Scenarios
- User registration and login
- Adding and removing RSS feeds
- Reading and marking articles
- Search and filtering
- Navigation and routing

### Running E2E Tests
```bash
# Start the application
./scripts/start.sh

# Run E2E tests
cd frontend
npm run test:e2e

# Open Cypress UI
npm run test:e2e:open
```

### E2E Test Configuration
- Base URL: `http://localhost:3000`
- Timeout: 10 seconds
- Screenshots on failure
- Video recording

## 📊 Coverage Reports

### Backend Coverage
- Location: `backend/htmlcov/index.html`
- Coverage includes:
  - API endpoints
  - Database models
  - Utility functions
  - Background jobs

### Frontend Coverage
- Location: `frontend/coverage/index.html`
- Coverage includes:
  - Vue components
  - JavaScript utilities
  - API integration

## 🔄 Continuous Integration

### GitHub Actions
The project includes a comprehensive CI pipeline that runs on:
- Push to main/develop branches
- Pull requests

### CI Pipeline Steps
1. **Backend Tests**: Unit and integration tests with PostgreSQL
2. **Frontend Tests**: Unit tests with coverage
3. **E2E Tests**: Full application testing
4. **Coverage Upload**: Results sent to Codecov

### Local CI Simulation
```bash
# Run the full test suite locally
./scripts/test.sh
```

## 🐛 Debugging Tests

### Backend Test Debugging
```bash
# Run tests with debug output
pytest tests/ -v -s

# Run specific test with debugger
pytest tests/test_api.py::TestFeedAPI::test_add_feed_success -v -s

# Run tests with print statements
pytest tests/ -v -s --capture=no
```

### Frontend Test Debugging
```bash
# Run tests in watch mode
npm run test -- --watch

# Run specific test file
npm run test -- tests/components/ArticleCard.test.js

# Debug with browser
npm run test:ui
```

### E2E Test Debugging
```bash
# Run tests with browser open
npm run test:e2e -- --headed

# Run specific test
npm run test:e2e -- --spec "cypress/e2e/home.cy.js"

# Debug with Cypress UI
npm run test:e2e:open
```

## 📝 Writing Tests

### Backend Test Guidelines
```python
# Example test structure
def test_function_name():
    """Test description."""
    # Arrange
    # Act
    # Assert
```

### Frontend Test Guidelines
```javascript
// Example test structure
describe('ComponentName', () => {
  it('should do something', () => {
    // Arrange
    // Act
    // Assert
  })
})
```

### E2E Test Guidelines
```javascript
// Example test structure
describe('Feature', () => {
  it('should work end-to-end', () => {
    // Visit page
    // Interact with elements
    // Assert results
  })
})
```

## 🎯 Best Practices

### Test Organization
- Group related tests in describe blocks
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Keep tests independent and isolated

### Test Data
- Use factories for test data
- Clean up after tests
- Use realistic test data
- Mock external dependencies

### Performance
- Run tests in parallel when possible
- Use fast test databases
- Minimize test setup time
- Cache dependencies

## 🚨 Common Issues

### Backend Test Issues
- Database connection problems
- Missing test dependencies
- Import path issues
- Environment variable conflicts

### Frontend Test Issues
- Component mounting problems
- Async test timing
- Mock configuration
- CSS/styling conflicts

### E2E Test Issues
- Application not running
- Element not found
- Timing issues
- Browser compatibility

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Vue Test Utils Guide](https://test-utils.vuejs.org/)
- [Vitest Documentation](https://vitest.dev/)
- [Cypress Documentation](https://docs.cypress.io/)
- [Testing Best Practices](https://testing-library.com/docs/guiding-principles) 