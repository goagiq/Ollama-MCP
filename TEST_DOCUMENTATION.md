# Test Cases for Airbnb Apartment Search Application

## Overview
This document contains comprehensive test cases for the Airbnb Apartment Search application running on `http://127.0.0.1:7860/`.

## Application Description
- **Type**: Gradio-based web application
- **Purpose**: Search for Airbnb apartments using AI models
- **Main Components**:
  - Search query input field
  - Ollama model selector dropdown
  - Submit and Clear buttons
  - Output display area
  - Flag button for feedback

## Available Models
- llama3.1:8b
- qwen2.5-coder:1.5b-base
- llama3.2:latest
- mistral:latest
- qwen3:latest

## Test Files Created

### 1. `test_cases_airbnb_search.py`
Comprehensive async Playwright test suite with detailed test scenarios.

### 2. `test_airbnb_playwright.py`
Sync Playwright tests for easier execution with pytest.

### 3. `manual_test_cases.py`
Detailed manual test cases with step-by-step instructions.

### 4. `simple_test_runner.py`
Simple automated test runner that doesn't require pytest.

## Test Categories

### Functional Tests
1. **Page Load Tests**
   - Verify page loads correctly
   - Check all UI elements are present
   - Validate page title and content

2. **Input Validation Tests**
   - Empty query submission
   - Valid search queries
   - Special characters handling
   - Very long queries
   - Unicode and emoji support

3. **Model Selection Tests**
   - Dropdown functionality
   - Model switching
   - Response variation between models

4. **Button Functionality Tests**
   - Submit button behavior
   - Clear button functionality
   - Flag button operation

### User Interface Tests
1. **Element Visibility**
   - All components visible
   - Proper layout and alignment
   - Responsive design

2. **Accessibility Tests**
   - Keyboard navigation
   - Screen reader compatibility
   - Focus management

### Performance Tests
1. **Response Time**
   - Query processing time
   - UI responsiveness
   - Model switching speed

2. **Stress Tests**
   - Multiple rapid submissions
   - Concurrent requests
   - Long-running queries

### Error Handling Tests
1. **Network Issues**
   - Connection timeouts
   - Server unavailability
   - Model errors

2. **Invalid Input**
   - Malformed queries
   - Unsupported characters
   - Extremely long input

## Sample Test Queries

### Basic Queries
- "1 bedroom apartment in New York"
- "Studio in Paris"
- "2 bedroom house in London"

### Detailed Queries
- "2 bedroom apartment in New York from 2023-10-01 to 2023-10-07"
- "Pet-friendly studio in San Francisco with WiFi for 1 week"
- "Luxury penthouse in Miami Beach with pool access"

### Edge Case Queries
- "" (empty)
- "a" (single character)
- Very long query (500+ characters)
- "🏠 House with garden 🌳" (emojis)
- "Apartment with $1000 budget" (special characters)

## How to Run Tests

### Prerequisites
```bash
pip install playwright pytest
playwright install
```

### Automated Tests
```bash
# Run simple test runner
python simple_test_runner.py

# Run pytest suite
pytest test_airbnb_playwright.py -v

# Run comprehensive async tests
pytest test_cases_airbnb_search.py -v
```

### Manual Testing
```bash
# Display manual test checklist
python simple_test_runner.py --manual

# View detailed test cases
python manual_test_cases.py
```

## Expected Results

### Successful Test Criteria
- ✅ Page loads without errors
- ✅ All UI elements function correctly
- ✅ Search queries generate appropriate responses
- ✅ Model selection works properly
- ✅ Error handling is graceful
- ✅ Performance is acceptable

### Key Performance Metrics
- Page load time: < 5 seconds
- Query response time: < 30 seconds
- UI interaction response: < 100ms

## Bug Reporting

When bugs are found, document:
1. Test case that revealed the bug
2. Steps to reproduce
3. Expected vs actual behavior
4. Environment details (browser, OS)
5. Screenshots/recordings if applicable

## Test Environment Requirements

### System Requirements
- Modern web browser (Chrome, Firefox, Edge)
- Stable internet connection
- Python 3.7+ (for automated tests)

### Application Requirements
- Airbnb search app running on localhost:7860
- Ollama models available and functional
- Backend services operational

## Maintenance Notes

### Regular Testing Schedule
- **Daily**: Basic functionality tests
- **Weekly**: Comprehensive test suite
- **Monthly**: Performance and stress tests
- **Release**: Full regression testing

### Test Data Updates
- Update test queries based on real user patterns
- Add new edge cases as discovered
- Update model list when new models are added

## Future Enhancements

### Potential Test Additions
1. Cross-browser compatibility tests
2. Mobile responsiveness tests
3. Load testing with multiple users
4. API endpoint testing
5. Security vulnerability testing
6. Internationalization testing

### Automation Improvements
1. CI/CD integration
2. Automated screenshot comparison
3. Performance regression detection
4. Test result reporting dashboard

## Contact Information
For questions about these test cases or to report issues, please contact the development team.

---
*Last Updated: July 22, 2025*
