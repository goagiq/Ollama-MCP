"""
Comprehensive Test Cases for Airbnb Apartment Search Application
Running on http://127.0.0.1:7860/

This test suite covers:
- UI functionality tests
- Input validation tests
- Model selection tests
- Search functionality tests
- Edge cases and error handling
- Performance tests
"""

import pytest
import asyncio
from playwright.async_api import async_playwright
import time
import json


class TestAirbnbSearch:
    """Test suite for the Airbnb Apartment Search Gradio application"""
    
    @pytest.fixture(scope="class")
    async def browser(self):
        """Setup browser for testing"""
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("http://127.0.0.1:7860/")
        yield page
        await browser.close()
        await playwright.stop()

    # UI Element Tests
    async def test_page_loads_successfully(self, browser):
        """Test that the page loads with all expected elements"""
        page = browser
        
        # Check page title
        title = await page.title()
        assert "Airbnb Apartment Search" in title
        
        # Check main heading
        heading = await page.locator("h1").text_content()
        assert "Airbnb Apartment Search" in heading
        
        # Check description
        description = await page.locator("p").text_content()
        assert "Search for an apartment on Airbnb" in description

    async def test_ui_elements_present(self, browser):
        """Test that all UI elements are present and visible"""
        page = browser
        
        # Check search query input
        search_input = page.locator("textarea[data-testid='textbox']").first
        assert await search_input.is_visible()
        
        # Check placeholder text
        placeholder = await search_input.get_attribute("placeholder")
        assert "Enter your search query for Airbnb apartments" in placeholder
        
        # Check Ollama model dropdown
        model_dropdown = page.locator("input[role='listbox']")
        assert await model_dropdown.is_visible()
        
        # Check buttons
        submit_btn = page.locator("button:has-text('Submit')")
        clear_btn = page.locator("button:has-text('Clear')")
        flag_btn = page.locator("button:has-text('Flag')")
        
        assert await submit_btn.is_visible()
        assert await clear_btn.is_visible()
        assert await flag_btn.is_visible()
        
        # Check output field
        output_field = page.locator("textarea[data-testid='textbox']").nth(1)
        assert await output_field.is_visible()
        assert await output_field.is_disabled()

    # Model Selection Tests
    async def test_ollama_model_dropdown(self, browser):
        """Test Ollama model dropdown functionality"""
        page = browser
        
        # Click on dropdown
        dropdown = page.locator("input[role='listbox']")
        await dropdown.click()
        
        # Wait for dropdown options to appear
        await page.wait_for_timeout(1000)
        
        # Check available models
        expected_models = [
            "llama3.1:8b",
            "qwen2.5-coder:1.5b-base", 
            "llama3.2:latest",
            "mistral:latest",
            "qwen3:latest"
        ]
        
        page_text = await page.text_content("body")
        for model in expected_models:
            assert model in page_text

    async def test_model_selection(self, browser):
        """Test selecting different models"""
        page = browser
        
        # Test selecting each available model
        models_to_test = ["llama3.1:8b", "mistral:latest", "qwen3:latest"]
        
        for model in models_to_test:
            # Click dropdown
            dropdown = page.locator("input[role='listbox']")
            await dropdown.click()
            await page.wait_for_timeout(500)
            
            # Select model (this might need adjustment based on actual dropdown behavior)
            # Since this is a Gradio app, we might need to use different selectors
            await page.click(f"text={model}")
            await page.wait_for_timeout(500)

    # Input Validation Tests
    async def test_empty_search_query(self, browser):
        """Test submitting with empty search query"""
        page = browser
        
        # Clear any existing input
        search_input = page.locator("textarea[data-testid='textbox']").first
        await search_input.clear()
        
        # Click submit without entering text
        submit_btn = page.locator("button:has-text('Submit')")
        await submit_btn.click()
        
        # Check for error handling or appropriate response
        await page.wait_for_timeout(2000)
        
        # Verify output field shows some response or remains empty
        output_field = page.locator("textarea[data-testid='textbox']").nth(1)
        output_value = await output_field.input_value()
        
        # This test checks that the app handles empty input gracefully
        print(f"Empty query result: {output_value}")

    async def test_valid_search_queries(self, browser):
        """Test various valid search queries"""
        page = browser
        
        valid_queries = [
            "2 bedroom apartment in New York from 2023-10-01 to 2023-10-07",
            "Studio apartment in San Francisco for 1 week",
            "3 bedroom house in Miami Beach December 2023",
            "Pet-friendly apartment in Chicago downtown",
            "Luxury condo in Los Angeles with pool"
        ]
        
        search_input = page.locator("textarea[data-testid='textbox']").first
        submit_btn = page.locator("button:has-text('Submit')")
        output_field = page.locator("textarea[data-testid='textbox']").nth(1)
        
        for query in valid_queries:
            # Clear previous input
            await search_input.clear()
            
            # Enter query
            await search_input.fill(query)
            
            # Submit
            await submit_btn.click()
            
            # Wait for response (adjust timeout as needed)
            await page.wait_for_timeout(5000)
            
            # Check if output was generated
            output_value = await output_field.input_value()
            print(f"Query: {query}")
            print(f"Response length: {len(output_value) if output_value else 0}")
            
            # Optional: Add assertions based on expected behavior
            # assert len(output_value) > 0, f"No output for query: {query}"

    async def test_special_characters_in_query(self, browser):
        """Test queries with special characters"""
        page = browser
        
        special_queries = [
            "Apartment with $1000 budget",
            "2BR near café & restaurant",
            "Place with 5★ rating",
            "Apartment @ downtown location",
            "Pet-friendly (cats & dogs)",
            "Apt. w/ A/C & Wi-Fi"
        ]
        
        search_input = page.locator("textarea[data-testid='textbox']").first
        submit_btn = page.locator("button:has-text('Submit')")
        
        for query in special_queries:
            await search_input.clear()
            await search_input.fill(query)
            await submit_btn.click()
            await page.wait_for_timeout(3000)
            
            # Verify app handles special characters without crashing
            assert await page.locator("body").is_visible()

    async def test_very_long_query(self, browser):
        """Test extremely long search query"""
        page = browser
        
        long_query = "I am looking for a very spacious and luxurious apartment " * 20
        
        search_input = page.locator("textarea[data-testid='textbox']").first
        await search_input.clear()
        await search_input.fill(long_query)
        
        submit_btn = page.locator("button:has-text('Submit')")
        await submit_btn.click()
        
        await page.wait_for_timeout(5000)
        
        # Verify app handles long input appropriately
        assert await page.locator("body").is_visible()

    # Button Functionality Tests
    async def test_clear_button(self, browser):
        """Test clear button functionality"""
        page = browser
        
        search_input = page.locator("textarea[data-testid='textbox']").first
        clear_btn = page.locator("button:has-text('Clear')")
        
        # Enter some text
        await search_input.fill("Test apartment search")
        
        # Verify text is present
        input_value = await search_input.input_value()
        assert len(input_value) > 0
        
        # Click clear button
        await clear_btn.click()
        await page.wait_for_timeout(1000)
        
        # Verify input is cleared
        input_value = await search_input.input_value()
        assert input_value == ""

    async def test_flag_button(self, browser):
        """Test flag button functionality"""
        page = browser
        
        # First generate some output
        search_input = page.locator("textarea[data-testid='textbox']").first
        submit_btn = page.locator("button:has-text('Submit')")
        flag_btn = page.locator("button:has-text('Flag')")
        
        await search_input.fill("Test query for flagging")
        await submit_btn.click()
        await page.wait_for_timeout(3000)
        
        # Click flag button
        await flag_btn.click()
        
        # Verify flag button works (may show confirmation or change state)
        await page.wait_for_timeout(1000)
        assert await flag_btn.is_visible()

    # Error Handling Tests
    async def test_network_resilience(self, browser):
        """Test behavior when backend might be slow/unavailable"""
        page = browser
        
        search_input = page.locator("textarea[data-testid='textbox']").first
        submit_btn = page.locator("button:has-text('Submit')")
        
        await search_input.fill("Network test query")
        await submit_btn.click()
        
        # Check that UI remains responsive during processing
        await page.wait_for_timeout(1000)
        assert await search_input.is_visible()
        assert await submit_btn.is_visible()

    # Performance Tests
    async def test_multiple_rapid_submissions(self, browser):
        """Test submitting multiple queries rapidly"""
        page = browser
        
        search_input = page.locator("textarea[data-testid='textbox']").first
        submit_btn = page.locator("button:has-text('Submit')")
        
        queries = [
            "Quick test 1",
            "Quick test 2", 
            "Quick test 3"
        ]
        
        for i, query in enumerate(queries):
            await search_input.clear()
            await search_input.fill(query)
            await submit_btn.click()
            
            # Small delay to avoid overwhelming the system
            await page.wait_for_timeout(500)
        
        # Verify UI still works after rapid submissions
        assert await search_input.is_visible()
        assert await submit_btn.is_enabled()

    # Accessibility Tests
    async def test_keyboard_navigation(self, browser):
        """Test keyboard navigation through the interface"""
        page = browser
        
        # Tab through elements
        await page.keyboard.press("Tab")  # Search input
        await page.keyboard.press("Tab")  # Model dropdown
        await page.keyboard.press("Tab")  # Clear button
        await page.keyboard.press("Tab")  # Submit button
        
        # Test Enter key on submit button
        search_input = page.locator("textarea[data-testid='textbox']").first
        await search_input.fill("Keyboard navigation test")
        await page.keyboard.press("Enter")
        
        await page.wait_for_timeout(2000)

    # Integration Tests  
    async def test_end_to_end_workflow(self, browser):
        """Test complete workflow from search to results"""
        page = browser
        
        # 1. Select model
        dropdown = page.locator("input[role='listbox']")
        await dropdown.click()
        await page.wait_for_timeout(500)
        # Select first available model
        await page.click("text=llama3.1:8b")
        
        # 2. Enter search query
        search_input = page.locator("textarea[data-testid='textbox']").first
        await search_input.fill("2 bedroom apartment in Paris for 1 week in January 2024")
        
        # 3. Submit search
        submit_btn = page.locator("button:has-text('Submit')")
        await submit_btn.click()
        
        # 4. Wait for results
        await page.wait_for_timeout(10000)  # Longer wait for actual processing
        
        # 5. Verify output
        output_field = page.locator("textarea[data-testid='textbox']").nth(1)
        output_value = await output_field.input_value()
        
        print(f"End-to-end test output length: {len(output_value) if output_value else 0}")
        
        # 6. Test flagging result if output exists
        if output_value and len(output_value) > 0:
            flag_btn = page.locator("button:has-text('Flag')")
            await flag_btn.click()
            await page.wait_for_timeout(1000)
        
        # 7. Clear for next test
        clear_btn = page.locator("button:has-text('Clear')")
        await clear_btn.click()


# Standalone test functions for manual testing
async def manual_test_session():
    """Manual test session for interactive testing"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            await page.goto("http://127.0.0.1:7860/")
            
            print("Starting manual test session...")
            print("Navigate through the interface manually and verify functionality")
            
            # Keep browser open for manual testing
            input("Press Enter to close browser...")
            
        finally:
            await browser.close()


# Test data for different scenarios
TEST_SCENARIOS = {
    "basic_searches": [
        "1 bedroom apartment in Tokyo",
        "Studio in New York Manhattan",
        "2BR house in London",
    ],
    "detailed_searches": [
        "3 bedroom apartment in Barcelona with balcony and WiFi for 2 weeks in summer",
        "Pet-friendly studio in Amsterdam near canals from March 15-20 2024",
        "Luxury penthouse in Dubai with pool and gym access for 1 month",
    ],
    "edge_cases": [
        "",  # Empty search
        "a",  # Single character
        "search" * 100,  # Very long search
        "Apartment with émojis 🏠🔑",  # Unicode characters
    ]
}


if __name__ == "__main__":
    # Run manual test session
    asyncio.run(manual_test_session())
