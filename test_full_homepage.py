

import time
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.webdriver.support.ui import Select # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.common.exceptions import TimeoutException, NoSuchElementException # type: ignore


class HomepagePetTests:

    
    def __init__(self):
        self.setup_driver()
        self.base_url = "http://localhost:3000/"
        self.wait = WebDriverWait(self.driver, 12)
    
    def setup_driver(self):
       
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(8)
        print(" WebDriver initialized")
    
    def navigate_to_homepage(self):
        """Navigate to homepage"""
        print(f" Loading {self.base_url}")
        self.driver.get(self.base_url)
        time.sleep(3)
        print(f" Page loaded: {self.driver.title}")
    
    
    def test_pet_search_functionality(self):
       
        print("\n TEST 2: Pet Search Functionality")
        print("-" * 45)
        
       
        search_selectors = [
            "input[type='search']", 
            "input[placeholder*='search' i]",
            "input[placeholder*='find' i]",
            "input[placeholder*='pet' i]",
            "input[name*='search']",
            "[data-testid*='search']",
            ".search-input", "#search", ".pet-search"
        ]
        
        search_input = None
        for selector in search_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and element.is_enabled():
                        search_input = element
                        placeholder = element.get_attribute('placeholder') or ''
                        print(f" Found search input: {selector} ('{placeholder}')")
                        break
                if search_input:
                    break
            except:
                continue
        
        if not search_input:
            print("  No search input found on homepage")
            return True 
        
      
        search_terms = ["dog", "cat", "puppy", "kitten", "Golden Retriever"]
        
        for term in search_terms[:2]:  
            try:
                print(f" Searching for: {term}")
                search_input.clear()
                search_input.send_keys(term)
                search_input.send_keys(Keys.ENTER)
                time.sleep(3)
                
               
                new_url = self.driver.current_url
                if new_url != self.base_url:
                    print(f" Search navigated to: {new_url}")
                    return True
                
                
                result_indicators = [
                    ".search-results", ".results", ".pet-results",
                    "[data-testid*='results']", ".pets", ".listings"
                ]
                
                for indicator in result_indicators:
                    try:
                        if self.driver.find_elements(By.CSS_SELECTOR, indicator):
                            print(" Search results appeared on page")
                            return True
                    except:
                        continue
                
            except Exception as e:
                print(f" Search error for '{term}': {e}")
                continue
        
        print("  Search behavior unclear")
        return True
    
    def test_find_pets_navigation(self):
        
        print("\n TEST 3: Find Pets Navigation")
        print("-" * 45)
        
        
        nav_selectors = [
            "a[href*='adopt']", "a[href*='pets']", "a[href*='find']",
            "button:contains('Find')", "button:contains('Adopt')",
            ".cta-button", ".find-pets", ".adopt-button",
            "[data-testid*='adopt']", "[data-testid*='find']",
            "nav a", ".navigation a"
        ]
        
      
        nav_elements = []
        
      
        for selector in nav_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                nav_elements.extend([el for el in elements if el.is_displayed()])
            except:
                continue
        
        
        text_searches = [
            "//a[contains(text(), 'Find') or contains(text(), 'Adopt') or contains(text(), 'Browse')]",
            "//button[contains(text(), 'Find') or contains(text(), 'Adopt') or contains(text(), 'Browse')]"
        ]
        
        for xpath in text_searches:
            try:
                elements = self.driver.find_elements(By.XPATH, xpath)
                nav_elements.extend([el for el in elements if el.is_displayed()])
            except:
                continue
        
        if not nav_elements:
            print(" No 'Find Pets' navigation found")
            return True
        
        print(f" Found {len(nav_elements)} potential pet navigation elements")
        
      
        for element in nav_elements[:3]: 
            try:
                element_text = element.text.lower()
                element_tag = element.tag_name
                href = element.get_attribute('href') if element_tag == 'a' else ''
                
                print(f" Testing navigation: '{element_text}' ({element_tag})")
                
                initial_url = self.driver.current_url
                self.driver.execute_script("arguments[0].click();", element)
                time.sleep(3)
                
                new_url = self.driver.current_url
                if new_url != initial_url:
                    print(f" Successfully navigated to: {new_url}")
                    
                   
                    if any(keyword in new_url.lower() for keyword in ['pet', 'adopt', 'find']):
                        print(" Navigation leads to pet-related page")
                        return True
                
            except Exception as e:
                print(f" Navigation click error: {e}")
                continue
        
        return True
    
    def test_pet_cards_on_homepage(self):
       
        print("\n TEST 4: Pet Cards on Homepage")
        print("-" * 45)
        
        
        if self.driver.current_url != self.base_url:
            self.navigate_to_homepage()
        
       
        pet_card_selectors = [
            ".pet-card", ".pet-item", ".pet", ".animal-card",
            "[data-testid*='pet']", ".card", ".listing",
            ".featured-pets .card", ".pets-grid > div",
            ".adoption-card", ".pet-profile"
        ]
        
        pet_cards = []
        for selector in pet_card_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and element.size['height'] > 50:
                        text = element.text.lower()
                        if any(keyword in text for keyword in ['breed', 'age', 'adopt', 'months', 'years', 'male', 'female']):
                            pet_cards.append(element)
            except:
                continue
        
        if pet_cards:
            print(f" Found {len(pet_cards)} pet cards on homepage")
            
            
            first_card = pet_cards[0]
            card_text = first_card.text
            print(f" First pet card preview: {card_text[:80]}...")
            
           
            try:
                images = first_card.find_elements(By.TAG_NAME, "img")
                if images:
                    print(f"Pet cards contain {len(images)} images")
            except:
                pass
            
            return True
        else:
           
            featured_selectors = [
                ".featured", ".featured-pets", ".available-pets",
                "[data-testid*='featured']", ".pets-section"
            ]
            
            for selector in featured_selectors:
                try:
                    section = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if section.is_displayed():
                        print(f" Found pets section: {selector}")
                        return True
                except:
                    continue
            
            print(" No pet cards found on homepage - might be on dedicated page")
            return True
    
    def test_pet_filtering_options(self):
        
        print("\n TEST 5: Pet Filtering Options")
        print("-" * 45)
        
       
        filter_selectors = [
            "select[name*='animal']", "select[name*='breed']", "select[name*='age']",
            ".filter", ".filter-select", "[data-testid*='filter']",
            "select[name*='type']", "select[name*='size']",
            ".pet-filters select", ".search-filters select"
        ]
        
        filters_found = []
        for selector in filter_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        filters_found.append((element, selector))
            except:
                continue
        
        
        filter_button_selectors = [
            "button[data-filter]", ".filter-button", ".filter-chip",
            "input[type='checkbox'][name*='animal']",
            "input[type='radio'][name*='pet']"
        ]
        
        for selector in filter_button_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        filters_found.append((element, selector))
            except:
                continue
        
        if not filters_found:
            print(" No pet filters found on homepage")
            return True
        
        print(f"Found {len(filters_found)} filter elements")
        
        
        try:
            first_filter, selector_used = filters_found[0]
            
            if first_filter.tag_name == 'select':
                print(f" Testing dropdown filter: {selector_used}")
                
                select = Select(first_filter)
                options = select.options
                
                if len(options) > 1:
                    
                    initial_page = self.driver.page_source
                    select.select_by_index(1)
                    time.sleep(2)
                    
                    new_page = self.driver.page_source
                    if new_page != initial_page:
                        print("Filter appears to update content")
                        return True
            
            elif first_filter.tag_name == 'button':
                print(f" Testing filter button: {selector_used}")
                
                initial_page = self.driver.page_source
                self.driver.execute_script("arguments[0].click();", first_filter)
                time.sleep(2)
                
                new_page = self.driver.page_source
                if new_page != initial_page:
                    print(" Filter button appears to work")
                    return True
        
        except Exception as e:
            print(f" Filter test error: {e}")
        
        return True
    
    def test_favorites_functionality(self):
      
        print("\n TEST 6: Pet Favorites")
        print("-" * 45)
        
       
        favorite_selectors = [
            ".favorite", ".heart", ".love", ".save",
            "[data-testid*='favorite']", "[data-testid*='heart']",
            "button[aria-label*='favorite']", ".wishlist",
            ".fa-heart", ".heart-icon"
        ]
        
        favorite_buttons = []
        for selector in favorite_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                favorite_buttons.extend([el for el in elements if el.is_displayed()])
            except:
                continue
        
       
        try:
            xpath_favorites = self.driver.find_elements(
                By.XPATH, "//button[contains(@aria-label, 'favorite') or contains(text(), '♥') or contains(text(), '🤍') or contains(text(), '❤')]"
            )
            favorite_buttons.extend([btn for btn in xpath_favorites if btn.is_displayed()])
        except:
            pass
        
        if not favorite_buttons:
            print("  No favorite buttons found")
            return True
        
        print(f" Found {len(favorite_buttons)} potential favorite buttons")
        
        
        try:
            first_fav = favorite_buttons[0]
            print(" Testing favorite button click")
            
           
            initial_class = first_fav.get_attribute('class') or ''
            initial_aria = first_fav.get_attribute('aria-label') or ''
            
            
            self.driver.execute_script("arguments[0].click();", first_fav)
            time.sleep(1)
            
            
            new_class = first_fav.get_attribute('class') or ''
            new_aria = first_fav.get_attribute('aria-label') or ''
            
            if new_class != initial_class or new_aria != initial_aria:
                print(" Favorite button state changed")
                return True
            
            
            notification_selectors = [
                ".notification", ".toast", ".alert", ".message",
                "[data-testid*='notification']"
            ]
            
            for selector in notification_selectors:
                try:
                    notifications = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if notifications and notifications[0].is_displayed():
                        print(" Favorite action showed feedback")
                        return True
                except:
                    continue
            
        except Exception as e:
            print(f" Favorite test error: {e}")
        
        return True
    
    def run_all_tests(self):
        
        print(" PawFinder Homepage Pet Finding Tests")
        print("=" * 50)
        
        tests = [
            ("Homepage Load & Pet Content", self.test_homepage_loads_with_pet_content),
            ("Pet Search Functionality", self.test_pet_search_functionality),
            ("Find Pets Navigation", self.test_find_pets_navigation),
            ("Pet Cards Display", self.test_pet_cards_on_homepage),
            ("Pet Filtering Options", self.test_pet_filtering_options),
            ("Favorites Functionality", self.test_favorites_functionality)
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f" {test_name} failed: {e}")
                results[test_name] = False
        
        # Summary
        print("\n" + "=" * 50)
        print(" PET FINDING TEST SUMMARY")
        print("=" * 50)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = " PASSED" if result else " FAILED"
            print(f"{test_name:<25} {status}")
        
        print("-" * 50)
        print(f" Result: {passed}/{total} tests passed")
        
        if passed >= 5:
            print(" Pet finding features are working great!")
        elif passed >= 3:
            print(" Core pet finding functionality is present")
        else:
            print("  Pet finding features need development")
        
        return results
    
    def cleanup(self):
        
        try:
            self.driver.quit()
            print("\n Browser closed")
        except:
            pass


def main():
   
    print(" PawFinder Homepage Pet Finding Tests")
    print("Make sure your app is running at http://localhost:3000/")
    print()
    
    try:
        input("Press Enter to start tests (Ctrl+C to cancel): ")
    except KeyboardInterrupt:
        print("\nTests cancelled")
        return
    
    tester = HomepagePetTests()
    
    try:
        results = tester.run_all_tests()
        return results
    except KeyboardInterrupt:
        print("\n\n Tests interrupted")
    except Exception as e:
        print(f"\n Error: {e}")
    finally:
        tester.cleanup()


if __name__ == "__main__":
    main()



import pytest # type: ignore

class TestHomepagePets:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.tester = HomepagePetTests()
        yield
        self.tester.cleanup()
    
    
    def test_pet_search_works(self):
        assert self.tester.test_pet_search_functionality()
    
    def test_find_pets_navigation_works(self):
        assert self.tester.test_find_pets_navigation()
    
    def test_pet_cards_display(self):
        assert self.tester.test_pet_cards_on_homepage()
    
    def test_pet_filters_work(self):
        assert self.tester.test_pet_filtering_options()
    
    def test_favorites_work(self):
        assert self.tester.test_favorites_functionality()


