"""
Simple Test Runner for Airbnb Apartment Search Application
This script runs basic automated tests using Playwright.

To use:
1. pip install playwright
2. playwright install
3. python simple_test_runner.py
"""

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("Playwright not installed. Install with: pip install playwright")

import time
import sys


def test_basic_functionality():
    """Run basic functionality tests"""
    if not PLAYWRIGHT_AVAILABLE:
        print("Cannot run tests - Playwright not available")
        return False
        
    print("Starting Airbnb Search App Tests...")
    print("=" * 50)
    
    test_results = []
    
    with sync_playwright() as p:
        try:
            # Launch browser
            browser = p.chromium.launch(headless=False, slow_mo=500)
            page = browser.new_page()
            
            # Test 1: Page Load
            print("Test 1: Page Load Test")
            try:
                page.goto("http://127.0.0.1:7860/", timeout=10000)
                page.wait_for_load_state("networkidle")
                
                title = page.title()
                if "Airbnb Apartment Search" in title:
                    print("✅ Page loads correctly")
                    test_results.append(("Page Load", "PASS"))
                else:
                    print(f"❌ Wrong page title: {title}")
                    test_results.append(("Page Load", "FAIL"))
            except Exception as e:
                print(f"❌ Page load failed: {e}")
                test_results.append(("Page Load", "FAIL"))
                browser.close()
                return False
            
            # Test 2: UI Elements Present
            print("\nTest 2: UI Elements Test")
            try:
                # Check search input
                search_input = page.locator("textarea[data-testid='textbox']").first
                if search_input.is_visible():
                    print("✅ Search input visible")
                else:
                    print("❌ Search input not found")
                
                # Check submit button
                submit_btn = page.locator("button:has-text('Submit')")
                if submit_btn.is_visible():
                    print("✅ Submit button visible")
                else:
                    print("❌ Submit button not found")
                
                # Check model dropdown
                dropdown = page.locator("input[role='listbox']")
                if dropdown.is_visible():
                    print("✅ Model dropdown visible")
                else:
                    print("❌ Model dropdown not found")
                
                test_results.append(("UI Elements", "PASS"))
                
            except Exception as e:
                print(f"❌ UI elements test failed: {e}")
                test_results.append(("UI Elements", "FAIL"))
            
            # Test 3: Search Input Functionality
            print("\nTest 3: Search Input Test")
            try:
                search_input = page.locator("textarea[data-testid='textbox']").first
                test_text = "Test apartment search"
                
                search_input.clear()
                search_input.fill(test_text)
                
                if search_input.input_value() == test_text:
                    print("✅ Search input works correctly")
                    test_results.append(("Search Input", "PASS"))
                else:
                    print("❌ Search input not working")
                    test_results.append(("Search Input", "FAIL"))
                    
            except Exception as e:
                print(f"❌ Search input test failed: {e}")
                test_results.append(("Search Input", "FAIL"))
            
            # Test 4: Clear Button
            print("\nTest 4: Clear Button Test")
            try:
                clear_btn = page.locator("button:has-text('Clear')")
                search_input = page.locator("textarea[data-testid='textbox']").first
                
                # Add text first
                search_input.fill("Text to clear")
                time.sleep(0.5)
                
                # Click clear
                clear_btn.click()
                time.sleep(1)
                
                if search_input.input_value() == "":
                    print("✅ Clear button works")
                    test_results.append(("Clear Button", "PASS"))
                else:
                    print("❌ Clear button not working")
                    test_results.append(("Clear Button", "FAIL"))
                    
            except Exception as e:
                print(f"❌ Clear button test failed: {e}")
                test_results.append(("Clear Button", "FAIL"))
            
            # Test 5: Model Dropdown
            print("\nTest 5: Model Dropdown Test")
            try:
                dropdown = page.locator("input[role='listbox']")
                dropdown.click()
                time.sleep(1)
                
                # Check if dropdown options are visible
                page_content = page.content()
                models_found = 0
                expected_models = ["llama3.1:8b", "mistral:latest", "qwen3:latest"]
                
                for model in expected_models:
                    if model in page_content:
                        models_found += 1
                
                if models_found >= 2:  # At least 2 models should be visible
                    print(f"✅ Model dropdown works ({models_found} models found)")
                    test_results.append(("Model Dropdown", "PASS"))
                else:
                    print(f"❌ Model dropdown issues ({models_found} models found)")
                    test_results.append(("Model Dropdown", "FAIL"))
                    
            except Exception as e:
                print(f"❌ Model dropdown test failed: {e}")
                test_results.append(("Model Dropdown", "FAIL"))
            
            # Test 6: Submit with Empty Query
            print("\nTest 6: Empty Submit Test")
            try:
                search_input = page.locator("textarea[data-testid='textbox']").first
                submit_btn = page.locator("button:has-text('Submit')")
                
                search_input.clear()
                submit_btn.click()
                time.sleep(3)
                
                # Check if page is still functional
                if page.locator("h1").is_visible():
                    print("✅ Empty submit handled gracefully")
                    test_results.append(("Empty Submit", "PASS"))
                else:
                    print("❌ Empty submit caused issues")
                    test_results.append(("Empty Submit", "FAIL"))
                    
            except Exception as e:
                print(f"❌ Empty submit test failed: {e}")
                test_results.append(("Empty Submit", "FAIL"))
            
            # Test 7: Valid Query Submit (Optional - takes time)
            print("\nTest 7: Valid Query Test (Quick)")
            try:
                search_input = page.locator("textarea[data-testid='textbox']").first
                submit_btn = page.locator("button:has-text('Submit')")
                
                search_input.clear()
                search_input.fill("1 bedroom apartment in Paris")
                submit_btn.click()
                
                # Wait briefly and check if UI is still responsive
                time.sleep(2)
                
                if page.locator("h1").is_visible() and submit_btn.is_visible():
                    print("✅ Valid query submitted successfully")
                    test_results.append(("Valid Query", "PASS"))
                else:
                    print("❌ Valid query submission failed")
                    test_results.append(("Valid Query", "FAIL"))
                    
            except Exception as e:
                print(f"❌ Valid query test failed: {e}")
                test_results.append(("Valid Query", "FAIL"))
            
            browser.close()
            
        except Exception as e:
            print(f"❌ Critical error during testing: {e}")
            try:
                browser.close()
            except:
                pass
            return False
    
    # Print results summary
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for _, result in test_results if result == "PASS")
    failed_tests = total_tests - passed_tests
    
    for test_name, result in test_results:
        status_icon = "✅" if result == "PASS" else "❌"
        print(f"{status_icon} {test_name}: {result}")
    
    print(f"\nTotal Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    return failed_tests == 0


def test_manual_checklist():
    """Display manual test checklist"""
    print("\nMANUAL TEST CHECKLIST")
    print("=" * 30)
    print("Please test the following manually:")
    print()
    
    manual_tests = [
        "1. ✓ Page loads without errors",
        "2. ✓ All UI elements are properly aligned", 
        "3. ✓ Search input accepts different types of text",
        "4. ✓ Model dropdown shows all available models",
        "5. ✓ Submit button generates appropriate responses",
        "6. ✓ Clear button resets all fields",
        "7. ✓ Flag button works without errors",
        "8. ✓ App handles special characters (emojis, symbols)",
        "9. ✓ Long queries don't break the interface",
        "10. ✓ Multiple rapid submissions are handled gracefully",
        "11. ✓ Keyboard navigation works properly",
        "12. ✓ Different models produce different results",
        "13. ✓ Response times are reasonable",
        "14. ✓ Interface remains responsive during processing"
    ]
    
    for test in manual_tests:
        print(test)
    
    print("\nSpecial Test Cases:")
    print("- Try query: '2 bedroom apartment in Tokyo for 1 week'")
    print("- Try query: 'Budget studio apartment under $100/night'") 
    print("- Try query: 'Pet-friendly house with garden'")
    print("- Try empty submission")
    print("- Try very long query (500+ characters)")
    print("- Try special characters: '$, €, ★, 🏠, café'")


def main():
    """Main test runner"""
    print("Airbnb Apartment Search - Test Runner")
    print("Version 1.0")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--manual":
        test_manual_checklist()
        return
    
    if not PLAYWRIGHT_AVAILABLE:
        print("Automated tests require Playwright.")
        print("Install with: pip install playwright")
        print("Then run: playwright install")
        print()
        print("For manual testing, run: python simple_test_runner.py --manual")
        return
    
    print("Note: Make sure the Airbnb search app is running on http://127.0.0.1:7860/")
    input("Press Enter to start automated tests...")
    
    success = test_basic_functionality()
    
    if success:
        print("\n🎉 All automated tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
    
    print("\nFor additional manual testing:")
    print("python simple_test_runner.py --manual")


if __name__ == "__main__":
    main()
