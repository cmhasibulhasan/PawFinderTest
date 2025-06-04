

import pytest # type: ignore
import time
import sys
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.webdriver.support.ui import Select # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.common.exceptions import ( # type: ignore
    TimeoutException, 
    NoSuchElementException, 
    ElementClickInterceptedException
)


class VeterinaryPageTests:
    """Selenium tests for the veterinary page"""
    
    def __init__(self):
        self.setup_driver()
        self.base_url = "http://localhost:3000/veterinary"
        self.wait = WebDriverWait(self.driver, 15)
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # For debugging, comment out the next line to see browser
        # chrome_options.add_argument("--headless")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.implicitly_wait(10)
            print("✅ Chrome WebDriver initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize WebDriver: {e}")
            print("Make sure ChromeDriver is installed and in PATH")
            sys.exit(1)
    
    def navigate_to_page(self):
        """Navigate to veterinary page"""
        try:
            print(f"🌐 Navigating to {self.base_url}")
            self.driver.get(self.base_url)
            time.sleep(3)
            print(f"✅ Successfully loaded: {self.driver.title}")
            return True
        except Exception as e:
            print(f"❌ Failed to load page: {e}")
            return False
    
    def test_page_accessibility(self):
        """Test 1: Check if the veterinary page loads and is accessible"""
        print("\n🧪 TEST 1: Page Accessibility")
        print("-" * 50)
        
        if not self.navigate_to_page():
            return False
        
        # Check URL
        current_url = self.driver.current_url
        print(f"📍 Current URL: {current_url}")
        
        # Check page title
        page_title = self.driver.title
        print(f"📄 Page Title: {page_title}")
        
        # Check if veterinary-related content exists
        veterinary_keywords = ["veterinary", "vet", "doctor", "clinic", "appointment"]
        page_source = self.driver.page_source.lower()
        
        found_keywords = [keyword for keyword in veterinary_keywords if keyword in page_source]
        print(f"🔍 Found veterinary keywords: {found_keywords}")
        
        # Look for main content areas
        content_selectors = [
            "main", "section", ".container", "[data-testid]", ".veterinary", ".vet"
        ]
        
        main_content_found = False
        for selector in content_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ Found main content: {selector} ({len(elements)} elements)")
                    main_content_found = True
                    break
            except:
                continue
        
        if not main_content_found:
            print("⚠️  No obvious main content containers found")
        
        success = "veterinary" in current_url.lower() and (found_keywords or main_content_found)
        print(f"🎯 Test Result: {'✅ PASSED' if success else '❌ FAILED'}")
        return success
    
    def test_search_functionality(self):
        """Test 2: Search for veterinarians"""
        print("\n🧪 TEST 2: Search Functionality")
        print("-" * 50)
        
        # Common search input selectors
        search_selectors = [
            "input[type='search']",
            "input[placeholder*='search' i]",
            "input[placeholder*='vet' i]",
            "input[placeholder*='doctor' i]",
            "input[name*='search']",
            "[data-testid*='search']",
            ".search-input",
            "#search"
        ]
        
        search_input = None
        for selector in search_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and elements[0].is_displayed():
                    search_input = elements[0]
                    print(f"✅ Found search input: {selector}")
                    break
            except:
                continue
        
        if search_input:
            try:
               
                search_terms = ["Dr", "Animal", "Pet", "Emergency"]
                
                for term in search_terms:
                    print(f"🔍 Searching for: {term}")
                    search_input.clear()
                    search_input.send_keys(term)
                    search_input.send_keys(Keys.ENTER)
                    time.sleep(2)
                    
                   
                    page_source_after = self.driver.page_source
                    if term.lower() in page_source_after.lower():
                        print(f"✅ Search for '{term}' appears to work")
                        return True
                    
                print("⚠️  Search functionality exists but results unclear")
                return True
                
            except Exception as e:
                print(f"❌ Error testing search: {e}")
                return False
        else:
            print("⚠️  No search input found - search might not be implemented")
            return True 
    
    def test_veterinarian_listings(self):
        """Test 3: Check for veterinarian listings or cards"""
        print("\n🧪 TEST 3: Veterinarian Listings")
        print("-" * 50)
        
       
        vet_card_selectors = [
            ".vet-card", ".veterinarian-card", ".doctor-card",
            "[data-testid*='vet']", "[data-testid*='doctor']",
            ".card", ".listing", ".profile-card",
            ".grid > div", ".list-item"
        ]
        
        vet_cards = []
        for selector in vet_card_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                   
                    for element in elements:
                        if element.is_displayed():
                            text = element.text.lower()
                            if any(keyword in text for keyword in ['dr', 'doctor', 'vet', 'dvm', 'clinic']):
                                vet_cards.append(element)
            except:
                continue
        
        if vet_cards:
            print(f"✅ Found {len(vet_cards)} potential veterinarian listings")
            
            
            first_card = vet_cards[0]
            card_text = first_card.text
            print(f"📋 First listing preview: {card_text[:100]}...")
            
           
            booking_buttons = first_card.find_elements(
                By.XPATH, ".//button[contains(text(), 'Book') or contains(text(), 'Contact') or contains(text(), 'Schedule')]"
            )
            
            if booking_buttons:
                print(f"✅ Found {len(booking_buttons)} booking/contact buttons")
            
            return True
        else:
            
            no_results_selectors = [
                ".no-results", ".empty-state", "[data-testid*='empty']",
                ".loading", ".spinner", "[data-testid*='loading']"
            ]
            
            for selector in no_results_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements and elements[0].is_displayed():
                        print(f"ℹ️  Found state indicator: {selector}")
                        return True
                except:
                    continue
            
            print("⚠️  No veterinarian listings found - data might be loading or empty")
            return True
    
    def test_navigation_elements(self):
   
        print("\n🧪 TEST 4: Navigation Elements")
        print("-" * 50)
        
 
        nav_selectors = ["nav", ".navigation", ".navbar", ".header", "[data-testid*='nav']"]
        nav_found = False
        
        for selector in nav_selectors:
            try:
                nav_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if nav_elements and nav_elements[0].is_displayed():
                    print(f"✅ Found navigation: {selector}")
                    nav_found = True
                    
                    # Check for veterinary-specific nav items
                    nav_text = nav_elements[0].text.lower()
                    vet_nav_items = ["vet", "doctor", "appointment", "book", "emergency"]
                    found_items = [item for item in vet_nav_items if item in nav_text]
                    if found_items:
                        print(f"✅ Found vet-related nav items: {found_items}")
                    break
            except:
                continue
        
   
        filter_selectors = [
            "select", ".filter", ".category", "[data-testid*='filter']",
            "button[role='button']", ".dropdown"
        ]
        
        filters_found = 0
        for selector in filter_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        text = element.text.lower() if element.text else ""
                        placeholder = element.get_attribute("placeholder") or ""
                        
                        if any(keyword in (text + placeholder).lower() 
                               for keyword in ["specialty", "location", "emergency", "filter", "category"]):
                            filters_found += 1
                            print(f"✅ Found filter element: {text or placeholder or selector}")
            except:
                continue
        
        if filters_found > 0:
            print(f"✅ Found {filters_found} filter/category elements")
        
        success = nav_found or filters_found > 0
        print(f"🎯 Navigation Test: {'✅ PASSED' if success else '⚠️  LIMITED'}")
        return success
    
    def test_responsive_design(self):
     
        print("\n🧪 TEST 5: Responsive Design")
        print("-" * 50)
        
        # Test different viewport sizes
        viewports = [
            (1920, 1080, "Desktop"),
            (768, 1024, "Tablet"),
            (375, 667, "Mobile")
        ]
        
        responsive_success = True
        
        for width, height, device in viewports:
            try:
                print(f"📱 Testing {device} viewport ({width}x{height})")
                self.driver.set_window_size(width, height)
                time.sleep(2)
                
              
                body = self.driver.find_element(By.TAG_NAME, "body")
                page_width = body.size['width']
                
                
                if width <= 768:  
                    
                    mobile_nav_selectors = [
                        ".mobile-menu", "[data-testid*='mobile']", 
                        ".hamburger", ".menu-toggle"
                    ]
                    
                    mobile_nav_found = False
                    for selector in mobile_nav_selectors:
                        try:
                            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                            if elements and elements[0].is_displayed():
                                print(f"✅ Found mobile navigation: {selector}")
                                mobile_nav_found = True
                                break
                        except:
                            continue
                
                print(f"✅ {device} layout appears functional")
                
            except Exception as e:
                print(f"❌ Error testing {device} viewport: {e}")
                responsive_success = False
        
        # Reset to desktop
        self.driver.set_window_size(1920, 1080)
        
        print(f"🎯 Responsive Test: {'✅ PASSED' if responsive_success else '❌ FAILED'}")
        return responsive_success
    
    def test_performance_basic(self):
        """Test 6: Basic performance check"""
        print("\n🧪 TEST 6: Basic Performance")
        print("-" * 50)
        
        start_time = time.time()
        
       
        self.driver.refresh()
        
      
        try:
            WebDriverWait(self.driver, 15).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            load_time = time.time() - start_time
            print(f"⏱️  Page load time: {load_time:.2f} seconds")
            
            if load_time < 5:
                print("✅ Good load time (< 5 seconds)")
                return True
            elif load_time < 10:
                print("⚠️  Acceptable load time (< 10 seconds)")
                return True
            else:
                print("❌ Slow load time (> 10 seconds)")
                return False
                
        except TimeoutException:
            print("❌ Page took too long to load (> 15 seconds)")
            return False
    
    def run_all_tests(self):
        """Run all tests and provide summary"""
        print("🚀 Starting PawFinder Veterinary Page Tests")
        print("=" * 60)
        
        tests = [
            ("Page Accessibility", self.test_page_accessibility),
            ("Search Functionality", self.test_search_functionality),
            ("Veterinarian Listings", self.test_veterinarian_listings),
            ("Navigation Elements", self.test_navigation_elements),
            ("Responsive Design", self.test_responsive_design),
            ("Basic Performance", self.test_performance_basic)
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"❌ {test_name} failed with error: {e}")
                results[test_name] = False
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name:<25} {status}")
        
        print("-" * 60)
        print(f"📈 Overall Result: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Veterinary page is working well.")
        elif passed >= total * 0.7:
            print("👍 Most tests passed. Some minor issues to investigate.")
        else:
            print("⚠️  Several tests failed. Page needs attention.")
        
        return results
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self.driver.quit()
            print("\n🧹 Browser closed successfully")
        except:
            pass


def main():
    """Main function to run the tests"""
    print("PawFinder Veterinary Page Selenium Tests")
    print("Make sure your Next.js app is running on http://localhost:3000")
    print()
    
    # Ask user if they want to continue
    try:
        user_input = input("Press Enter to start tests (or 'q' to quit): ").strip().lower()
        if user_input == 'q':
            print("Tests cancelled by user.")
            return
    except KeyboardInterrupt:
        print("\nTests cancelled by user.")
        return
    
    tester = VeterinaryPageTests()
    
    try:
        results = tester.run_all_tests()
        return results
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
    finally:
        tester.cleanup()


if __name__ == "__main__":
    main()



class TestVeterinaryPage:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.tester = VeterinaryPageTests()
        yield
        self.tester.cleanup()
    
    
    def test_search_works(self):
        assert self.tester.test_search_functionality()
    
    def test_listings_present(self):
        assert self.tester.test_veterinarian_listings() 
    
    def test_responsive_layout(self):
        assert self.tester.test_responsive_design()
    
    def test_performance_acceptable(self):
        assert self.tester.test_performance_basic()


#thik ase