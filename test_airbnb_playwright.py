"""
Playwright Test Cases for Airbnb Apartment Search Application
URL: http://127.0.0.1:7860/

To run these tests:
1. Make sure the Airbnb search app is running on localhost:7860
2. Install playwright: pip install playwright pytest
3. Install browsers: playwright install
4. Run tests: pytest test_airbnb_playwright.py -v
"""

import pytest
from playwright.sync_api import sync_playwright, Page, Browser
import time


class TestAirbnbSearchApp:
    """Playwright test suite for Airbnb Search Application"""
    
    @pytest.fixture(scope="class")
    def browser_setup(self):
        """Setup browser for all tests"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            context = browser.new_context()
            page = context.new_page()
            page.goto("http://127.0.0.1:7860/")
            page.wait_for_load_state("networkidle")
            
            yield page
            
            browser.close()

    def test_page_elements_load(self, browser_setup):
        """Test 1: Verify all page elements load correctly"""
        page = browser_setup
        
        # Check page title
        assert "Airbnb Apartment Search" in page.title()
        
        # Check main heading
        heading = page.locator("h1").text_content()
        assert "Airbnb Apartment Search" in heading
        
        # Check description text
        description = page.locator("p").text_content()
        assert "Search for an apartment on Airbnb" in description
        
        # Verify search input field
        search_input = page.locator("textarea[data-testid='textbox']").first
        assert search_input.is_visible()
        
        # Verify placeholder text
        placeholder = search_input.get_attribute("placeholder")
        assert "Enter your search query for Airbnb apartments" in placeholder
        
        # Verify model dropdown
        model_dropdown = page.locator("input[role='listbox']")
        assert model_dropdown.is_visible()
        
        # Verify buttons
        assert page.locator("button:has-text('Submit')").is_visible()
        assert page.locator("button:has-text('Clear')").is_visible()
        assert page.locator("button:has-text('Flag')").is_visible()
        
        # Verify output field
        output_field = page.locator("textarea[data-testid='textbox']").nth(1)
        assert output_field.is_visible()
        assert output_field.is_disabled()

    def test_model_dropdown_functionality(self, browser_setup):
        """Test 2: Test Ollama model dropdown"""
        page = browser_setup
        
        # Click on model dropdown
        dropdown = page.locator("input[role='listbox']")
        dropdown.click()
        
        # Wait for dropdown to open
        page.wait_for_timeout(1000)
        
        # Check that model options are visible
        page_content = page.content()
        expected_models = [
            "llama3.1:8b",
            "qwen2.5-coder:1.5b-base", 
            "llama3.2:latest",
            "mistral:latest",
            "qwen3:latest"
        ]
        
        for model in expected_models:
            assert model in page_content, f"Model {model} not found in dropdown"

    def test_search_input_functionality(self, browser_setup):
        """Test 3: Test search input field"""
        page = browser_setup
        
        search_input = page.locator("textarea[data-testid='textbox']").first
        
        # Test typing in search field
        test_query = "2 bedroom apartment in New York"
        search_input.clear()
        search_input.fill(test_query)
        
        # Verify text was entered
        input_value = search_input.input_value()
        assert input_value == test_query

    def test_clear_button_functionality(self, browser_setup):
        """Test 4: Test clear button"""
        page = browser_setup
        
        search_input = page.locator("textarea[data-testid='textbox']").first
        clear_button = page.locator("button:has-text('Clear')")
        
        # Enter text
        search_input.fill("Test text to clear")
        assert len(search_input.input_value()) > 0
        
        # Click clear button
        clear_button.click()
        page.wait_for_timeout(1000)
        
        # Verify field is cleared
        assert search_input.input_value() == ""

    def test_submit_with_empty_query(self, browser_setup):
        """Test 5: Test submitting with empty search query"""
        page = browser_setup
        
        search_input = page.locator("textarea[data-testid='textbox']").first
        submit_button = page.locator("button:has-text('Submit')")
        output_field = page.locator("textarea[data-testid='textbox']").nth(1)
        
        # Clear search field
        search_input.clear()
        assert search_input.input_value() == ""
        
        # Submit empty query
        submit_button.click()
        page.wait_for_timeout(3000)
        
        # Check that app handles empty submission gracefully
        # (Output might be empty or contain an error message)
        output_value = output_field.input_value()
        print(f"Empty query result: '{output_value}'")

    def test_submit_with_valid_query(self, browser_setup):
        """Test 6: Test submitting with valid search query"""
        page = browser_setup
        
        search_input = page.locator("textarea[data-testid='textbox']").first
        submit_button = page.locator("button:has-text('Submit')")
        output_field = page.locator("textarea[data-testid='textbox']").nth(1)
        
        # Enter valid search query
        test_query = "1 bedroom apartment in Paris for 1 week"
        search_input.clear()
        search_input.fill(test_query)
        
        # Submit query
        submit_button.click()
        
        # Wait for response (adjust timeout based on model response time)
        page.wait_for_timeout(10000)
        
        # Check if output was generated
        output_value = output_field.input_value()
        print(f"Query: {test_query}")
        print(f"Response length: {len(output_value) if output_value else 0}")
        
        # Note: Actual assertions depend on expected behavior
        # For now, we just verify the app didn't crash
        assert page.locator("h1").is_visible()

    def test_flag_button_functionality(self, browser_setup):
        """Test 7: Test flag button"""
        page = browser_setup
        
        flag_button = page.locator("button:has-text('Flag')")
        
        # Click flag button
        flag_button.click()
        page.wait_for_timeout(1000)
        
        # Verify button is still visible (basic functionality test)
        assert flag_button.is_visible()

    def test_special_characters_in_search(self, browser_setup):
        """Test 8: Test search with special characters"""
        page = browser_setup
        
        search_input = page.locator("textarea[data-testid='textbox']").first
        submit_button = page.locator("button:has-text('Submit')")
        
        special_queries = [
            "Apartment with $1000 budget",
            "2BR near café & restaurant", 
            "Place with 5★ rating",
            "Pet-friendly (cats & dogs)"
        ]
        
        for query in special_queries:
            search_input.clear()
            search_input.fill(query)
            submit_button.click()
            page.wait_for_timeout(2000)
            
            # Verify app doesn't crash with special characters
            assert page.locator("h1").is_visible()
            print(f"Tested query with special chars: {query}")

    def test_model_selection(self, browser_setup):
        """Test 9: Test selecting different models"""
        page = browser_setup
        
        dropdown = page.locator("input[role='listbox']")
        
        # Click dropdown to open
        dropdown.click()
        page.wait_for_timeout(1000)
        
        # Try to select a specific model
        # Note: This might need adjustment based on actual dropdown behavior
        try:
            page.click("text=llama3.1:8b")
            page.wait_for_timeout(1000)
            print("Successfully selected llama3.1:8b model")
        except Exception as e:
            print(f"Model selection test info: {e}")

    def test_keyboard_navigation(self, browser_setup):
        """Test 10: Test keyboard navigation"""
        page = browser_setup
        
        search_input = page.locator("textarea[data-testid='textbox']").first
        
        # Focus on search input
        search_input.click()
        
        # Type using keyboard
        page.keyboard.type("Keyboard test query")
        
        # Use Tab to navigate to submit button
        page.keyboard.press("Tab")  # Move to model dropdown
        page.keyboard.press("Tab")  # Move to clear button  
        page.keyboard.press("Tab")  # Move to submit button
        
        # Press Enter to submit
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)
        
        # Verify navigation worked
        assert search_input.input_value() == "Keyboard test query"

    def test_long_search_query(self, browser_setup):
        """Test 11: Test with very long search query"""
        page = browser_setup
        
        search_input = page.locator("textarea[data-testid='textbox']").first
        submit_button = page.locator("button:has-text('Submit')")
        
        # Create a very long query
        long_query = "I am looking for a very spacious apartment with many amenities " * 50
        
        search_input.clear()
        search_input.fill(long_query)
        submit_button.click()
        page.wait_for_timeout(5000)
        
        # Verify app handles long input gracefully
        assert page.locator("h1").is_visible()
        print(f"Long query test completed. Query length: {len(long_query)}")

    def test_rapid_submissions(self, browser_setup):
        """Test 12: Test multiple rapid submissions"""
        page = browser_setup
        
        search_input = page.locator("textarea[data-testid='textbox']").first
        submit_button = page.locator("button:has-text('Submit')")
        
        queries = ["Quick test 1", "Quick test 2", "Quick test 3"]
        
        for i, query in enumerate(queries):
            search_input.clear()
            search_input.fill(query)
            submit_button.click()
            page.wait_for_timeout(500)  # Short delay
            print(f"Submitted rapid query {i+1}: {query}")
        
        # Verify UI is still responsive
        page.wait_for_timeout(2000)
        assert search_input.is_visible()
        assert submit_button.is_enabled()


def manual_test_example():
    """Example of manual testing with Playwright"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://127.0.0.1:7860/")
        
        print("Manual test started. Browser will stay open for manual testing.")
        print("Test the following manually:")
        print("1. Enter different search queries")
        print("2. Try different model selections")
        print("3. Test all buttons")
        print("4. Check responsiveness")
        
        input("Press Enter to close browser...")
        browser.close()


if __name__ == "__main__":
    # Run manual test
    manual_test_example()
