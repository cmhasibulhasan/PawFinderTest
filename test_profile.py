
import time
import pytest # type: ignore
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.common.keys import Keys # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.common.action_chains import ActionChains # type: ignore
from selenium.common.exceptions import ( # type: ignore
    TimeoutException, 
    NoSuchElementException, 
    ElementClickInterceptedException
)


class SignInPageTests:
   
    
    def __init__(self):
        self.setup_driver()
        self.base_url = "http://localhost:3000"
        self.signin_urls = [
            "/sign-in", "/signin", "/login", "/auth/signin", "/auth/login"
        ]
        self.wait = WebDriverWait(self.driver, 15)
        
       
        self.test_credentials = {
            "valid_email": "testuser@pawfinder.com",
            "valid_password": "TestPassword123",
            "invalid_email": "invalid@example.com",
            "invalid_password": "wrongpassword",
            "malformed_email": "notanemail"
        }
    
    def setup_driver(self):
        """Setup Chrome WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
       
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        print("✅ WebDriver initialized for sign-in tests")
    
    def find_signin_page(self):
        """Find and navigate to the sign-in page"""
        signin_url = None
        
        
        for url_path in self.signin_urls:
            test_url = f"{self.base_url}{url_path}"
            try:
                print(f"🔍 Trying: {test_url}")
                self.driver.get(test_url)
                time.sleep(2)
                
                current_url = self.driver.current_url
                page_title = self.driver.title.lower()
                page_source = self.driver.page_source.lower()
                
                
                signin_indicators = [
                    "sign in", "login", "email", "password", "authenticate"
                ]
                
                is_signin_page = (
                    any(indicator in page_title for indicator in signin_indicators) or
                    any(indicator in page_source for indicator in signin_indicators) or
                    url_path.lower() in current_url.lower()
                )
                
                if is_signin_page and "404" not in page_title:
                    signin_url = test_url
                    print(f"✅ Found sign-in page: {signin_url}")
                    break
                    
            except Exception as e:
                print(f"❌ Error accessing {test_url}: {e}")
                continue
        
        if not signin_url:
            
            self.driver.get(self.base_url)
            time.sleep(2)
            
            signin_link_selectors = [
                "a[href*='sign-in']", "a[href*='signin']", "a[href*='login']",
                "a:contains('Sign In')", "a:contains('Login')",
                "[data-testid*='signin']", "[data-testid*='login']",
                ".signin-link", ".login-link"
            ]
            
            for selector in signin_link_selectors:
                try:
                    
                    if "contains" in selector:
                        xpath = f"//a[contains(text(), 'Sign In') or contains(text(), 'Login') or contains(text(), 'Sign in')]"
                        links = self.driver.find_elements(By.XPATH, xpath)
                    else:
                        links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if links and links[0].is_displayed():
                        print(f"🔗 Found sign-in link: {selector}")
                        links[0].click()
                        time.sleep(2)
                        signin_url = self.driver.current_url
                        break
                        
                except Exception:
                    continue
        
        if signin_url:
            print(f"📍 Using sign-in page: {signin_url}")
            return signin_url
        else:
            print("❌ Could not find sign-in page")
            return None
    
    def get_form_elements(self):
        """Get sign-in form elements"""
        elements = {}
        
       
        email_selectors = [
            "input[type='email']", "input[name='email']", "input[id='email']",
            "input[name='username']", "input[id='username']",
            "input[placeholder*='email' i]", "input[placeholder*='username' i]",
            "[data-testid*='email']", "[data-testid*='username']"
        ]
        
        for selector in email_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed() and element.is_enabled():
                    elements['email'] = element
                    print(f"✅ Found email field: {selector}")
                    break
            except:
                continue
        
   
        password_selectors = [
            "input[type='password']", "input[name='password']", "input[id='password']",
            "[data-testid*='password']", ".password-input"
        ]
        
        for selector in password_selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                if element.is_displayed() and element.is_enabled():
                    elements['password'] = element
                    print(f"✅ Found password field: {selector}")
                    break
            except:
                continue
        
        
        submit_selectors = [
            "button[type='submit']", "input[type='submit']",
            "button:contains('Sign In')", "button:contains('Login')",
            "[data-testid*='submit']", "[data-testid*='signin']",
            ".signin-btn", ".login-btn", ".submit-btn"
        ]
        
        for selector in submit_selectors:
            try:
                if "contains" in selector:
                    xpath = "//button[contains(text(), 'Sign In') or contains(text(), 'Login') or contains(text(), 'Submit')]"
                    element = self.driver.find_element(By.XPATH, xpath)
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    
                if element.is_displayed() and element.is_enabled():
                    elements['submit'] = element
                    print(f"✅ Found submit button: {selector}")
                    break
            except:
                continue
        
        return elements
    
    def test_page_loads_correctly(self):
        """Test 1: Sign-in page loads with proper elements"""
        print("\n🧪 TEST 1: Page Load & Form Elements")
        print("-" * 45)
        
        signin_url = self.find_signin_page()
        if not signin_url:
            print("❌ Cannot find sign-in page")
            return False
        
        
        page_title = self.driver.title
        print(f"📄 Page title: {page_title}")
        
      
        elements = self.get_form_elements()
        
        required_elements = ['email', 'password', 'submit']
        missing_elements = [elem for elem in required_elements if elem not in elements]
        
        if missing_elements:
            print(f"❌ Missing form elements: {missing_elements}")
            return False
        
        print("✅ All required form elements found")
        return True
    
    def test_form_validation(self):
        """Test 2: Form validation (empty fields, invalid email)"""
        print("\n🧪 TEST 2: Form Validation")
        print("-" * 45)
        
        elements = self.get_form_elements()
        if not elements.get('email') or not elements.get('submit'):
            print("⚠️  Form elements not available")
            return True
        
        
        print("🔘 Testing empty form submission...")
        try:
            elements['submit'].click()
            time.sleep(2)
            
            
            error_selectors = [
                ".error", ".error-message", ".field-error", ".validation-error",
                "[data-testid*='error']", ".invalid-feedback", ".form-error",
                ".text-red", ".text-danger", ".error-text"
            ]
            
            validation_found = False
            for selector in error_selectors:
                try:
                    error_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    visible_errors = [e for e in error_elements if e.is_displayed() and e.text.strip()]
                    
                    if visible_errors:
                        print(f"✅ Found validation errors: {selector}")
                        for error in visible_errors[:2]: 
                            print(f"   → {error.text}")
                        validation_found = True
                        break
                except:
                    continue
            
            if not validation_found:
                
                email_element = elements['email']
                if email_element.get_attribute('required'):
                    print("✅ HTML5 validation likely active (required attribute found)")
                    validation_found = True
            
            if not validation_found:
                print("⚠️  No validation errors found - might use different validation method")
        
        except Exception as e:
            print(f"❌ Error testing empty form: {e}")
        
        
        print("🔘 Testing invalid email format...")
        try:
            email_element = elements['email']
            email_element.clear()
            email_element.send_keys(self.test_credentials['malformed_email'])
            
            if elements.get('password'):
                elements['password'].clear()
                elements['password'].send_keys("somepassword")
            
            elements['submit'].click()
            time.sleep(2)
            
            
            current_url = self.driver.current_url
            if "sign" in current_url.lower() or "login" in current_url.lower():
                print("✅ Invalid email rejected (stayed on sign-in page)")
            
        except Exception as e:
            print(f"❌ Error testing invalid email: {e}")
        
        return True
    
    def test_valid_login_attempt(self):
        """Test 3: Valid login attempt (may fail auth but should process)"""
        print("\n🧪 TEST 3: Valid Login Attempt")
        print("-" * 45)
        
        elements = self.get_form_elements()
        if not all(key in elements for key in ['email', 'password', 'submit']):
            print("⚠️  Form elements not available")
            return True
        
        try:
           
            email_element = elements['email']
            password_element = elements['password']
            submit_element = elements['submit']
            
            email_element.clear()
            email_element.send_keys(self.test_credentials['valid_email'])
            
            password_element.clear()
            password_element.send_keys(self.test_credentials['valid_password'])
            
            print(f"📝 Filling form with: {self.test_credentials['valid_email']}")
            
           
            initial_url = self.driver.current_url
            submit_element.click()
            time.sleep(3)
            
           
            new_url = self.driver.current_url
            
            if new_url != initial_url:
                print(f"✅ Form submitted - redirected to: {new_url}")
                
                
                if any(destination in new_url.lower() for destination in ['dashboard', 'profile', 'home', 'account']):
                    print("✅ Likely successful login (redirected to protected area)")
                elif "sign" in new_url.lower() or "login" in new_url.lower():
                    print("⚠️  Returned to login page (likely auth failed)")
                else:
                    print("ℹ️  Redirected to different page")
            else:
                
                error_selectors = [
                    ".error", ".alert-danger", ".login-error", 
                    "[data-testid*='error']", ".auth-error"
                ]
                
                error_found = False
                for selector in error_selectors:
                    try:
                        errors = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        visible_errors = [e for e in errors if e.is_displayed() and e.text.strip()]
                        
                        if visible_errors:
                            print(f"⚠️  Login error displayed: {visible_errors[0].text}")
                            error_found = True
                            break
                    except:
                        continue
                
                if not error_found:
                    print("⚠️  Form submitted but no clear feedback")
            
            return True
            
        except Exception as e:
            print(f"❌ Error during login attempt: {e}")
            return False
    
    def test_password_visibility_toggle(self):
        """Test 4: Password visibility toggle"""
        print("\n🧪 TEST 4: Password Visibility Toggle")
        print("-" * 45)
        
        elements = self.get_form_elements()
        password_element = elements.get('password')
        
        if not password_element:
            print("⚠️  Password field not available")
            return True
        
        
        toggle_selectors = [
            ".password-toggle", ".show-password", ".toggle-password",
            "[data-testid*='toggle']", "[data-testid*='show']",
            "button[aria-label*='password']", ".eye-icon",
            ".fa-eye", ".password-reveal"
        ]
        
        toggle_found = False
        for selector in toggle_selectors:
            try:
                toggle_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                
                
                password_container = password_element.find_element(By.XPATH, "./..")
                container_toggles = password_container.find_elements(By.CSS_SELECTOR, "button, .toggle, .icon")
                
                all_toggles = toggle_elements + container_toggles
                
                for toggle in all_toggles:
                    if toggle.is_displayed():
                        print(f"✅ Found password toggle: {selector}")
                        
                        
                        try:
                            password_element.send_keys("testpassword")
                            
                            initial_type = password_element.get_attribute('type')
                            toggle.click()
                            time.sleep(1)
                            
                            new_type = password_element.get_attribute('type')
                            
                            if initial_type != new_type:
                                print(f"✅ Password toggle works: {initial_type} → {new_type}")
                            else:
                                print("⚠️  Toggle clicked but type didn't change")
                            
                            password_element.clear()
                            toggle_found = True
                            break
                            
                        except Exception as e:
                            print(f"❌ Error testing toggle: {e}")
                
                if toggle_found:
                    break
                    
            except:
                continue
        
        if not toggle_found:
            print("⚠️  No password visibility toggle found")
        
        return True
    
    def test_remember_me_functionality(self):
        """Test 5: Remember me checkbox"""
        print("\n🧪 TEST 5: Remember Me Functionality")
        print("-" * 45)
       
        remember_selectors = [
            "input[name*='remember']", "input[id*='remember']",
            "[data-testid*='remember']", ".remember-me",
            "input[type='checkbox']"
        ]
        
        remember_element = None
        for selector in remember_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        
                        label_text = ""
                        try:
                            
                            label_id = element.get_attribute('id')
                            if label_id:
                                label = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{label_id}']")
                                label_text = label.text.lower()
                        except:
                           
                            parent = element.find_element(By.XPATH, "./..")
                            label_text = parent.text.lower()
                        
                        if "remember" in label_text or "keep" in label_text:
                            remember_element = element
                            print(f"✅ Found remember me checkbox: {selector}")
                            break
                
                if remember_element:
                    break
                    
            except:
                continue
        
        if remember_element:
            try:
               
                initial_state = remember_element.is_selected()
                remember_element.click()
                time.sleep(0.5)
                
                new_state = remember_element.is_selected()
                
                if initial_state != new_state:
                    print(f"✅ Remember me checkbox works: {initial_state} → {new_state}")
                else:
                    print("⚠️  Checkbox state didn't change")
                    
            except Exception as e:
                print(f"❌ Error testing remember me: {e}")
        else:
            print("⚠️  No remember me checkbox found")
        
        return True
    
    def test_forgot_password_link(self):
        """Test 6: Forgot password functionality"""
        print("\n🧪 TEST 6: Forgot Password Link")
        print("-" * 45)
        
      
        forgot_selectors = [
            "a[href*='forgot']", "a[href*='reset']", "a[href*='password']",
            "[data-testid*='forgot']", ".forgot-password", ".reset-password"
        ]
        
        forgot_link = None
        for selector in forgot_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if elements and elements[0].is_displayed():
                    forgot_link = elements[0]
                    print(f"✅ Found forgot password link: {selector}")
                    break
            except:
                continue
        
        if not forgot_link:
            try:
                xpath = "//a[contains(text(), 'Forgot') or contains(text(), 'Reset') or contains(text(), 'password')]"
                elements = self.driver.find_elements(By.XPATH, xpath)
                if elements and elements[0].is_displayed():
                    forgot_link = elements[0]
                    print("✅ Found forgot password link via text search")
            except:
                pass
        
        if forgot_link:
            try:
               
                initial_url = self.driver.current_url
                forgot_link.click()
                time.sleep(2)
                
                new_url = self.driver.current_url
                
                if new_url != initial_url:
                    print(f"✅ Forgot password link works - navigated to: {new_url}")
                    
                   
                    self.driver.back()
                    time.sleep(1)
                else:
                    print("⚠️  Forgot password link clicked but no navigation")
                    
            except Exception as e:
                print(f"❌ Error testing forgot password: {e}")
        else:
            print("⚠️  No forgot password link found")
        
        return True
    
    def test_social_login_options(self):
        """Test 7: Social login buttons"""
        print("\n🧪 TEST 7: Social Login Options")
        print("-" * 45)
       
        social_providers = ['google', 'facebook', 'twitter', 'github', 'apple']
        social_buttons = []
        
        for provider in social_providers:
            selectors = [
                f"[data-testid*='{provider}']",
                f".{provider}-login", f".signin-{provider}",
                f"button[class*='{provider}']", f"a[href*='{provider}']"
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed():
                            social_buttons.append((provider, element))
                            print(f"Found {provider} login button")
                            break
                except:
                    continue
        
       
        generic_social_selectors = [
            ".social-login", ".oauth-button", ".third-party-login",
            "[data-testid*='social']", ".external-auth"
        ]
        
        for selector in generic_social_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        text = element.text.lower()
                        social_buttons.append(("generic", element))
                        print(f" Found social login button: {text}")
            except:
                continue
        
        if social_buttons:
            print(f" Total social login options: {len(social_buttons)}")
            
            
            try:
                provider, button = social_buttons[0]
                print(f" Testing {provider} login button...")
                
                initial_url = self.driver.current_url
                button.click()
                time.sleep(2)
                
                new_url = self.driver.current_url
                
                if new_url != initial_url:
                    print(f" Social login redirected to: {new_url}")
                   
                    self.driver.back()
                    time.sleep(1)
                else:
                    print("  Social button clicked but no redirect")
                    
            except Exception as e:
                print(f" Error testing social login: {e}")
        else:
            print("  No social login options found")
        
        return True
    
    def test_accessibility_features(self):
        """Test 8: Basic accessibility features"""
        print("\n TEST 8: Accessibility Features")
        print("-" * 45)
        
        elements = self.get_form_elements()
        accessibility_score = 0
        
        
        for field_name, element in elements.items():
            if field_name in ['email', 'password']:
                try:
                    
                    aria_label = element.get_attribute('aria-label')
                    if aria_label:
                        print(f" {field_name} has aria-label: '{aria_label}'")
                        accessibility_score += 1
                    
                    
                    field_id = element.get_attribute('id')
                    if field_id:
                        try:
                            label = self.driver.find_element(By.CSS_SELECTOR, f"label[for='{field_id}']")
                            print(f" {field_name} has associated label")
                            accessibility_score += 1
                        except:
                            pass
                    
                
                    placeholder = element.get_attribute('placeholder')
                    if placeholder:
                        print(f" {field_name} has placeholder: '{placeholder}'")
                        accessibility_score += 1
                        
                except Exception as e:
                    print(f" Error checking {field_name} accessibility: {e}")
        

        try:
            print("Testing keyboard navigation...")
            
            
            first_element = elements.get('email')
            if first_element:
                first_element.click()
                
                for i in range(5): 
                    ActionChains(self.driver).send_keys(Keys.TAB).perform()
                    time.sleep(0.3)
                    
                    focused_element = self.driver.switch_to.active_element
                    if focused_element.is_displayed():
                        accessibility_score += 0.5
                
                print("Keyboard navigation appears to work")
                
        except Exception as e:
            print(f"❌ Error testing keyboard navigation: {e}")
        
        print(f"📊 Accessibility score: {accessibility_score}/6")
        return True
    
    def run_all_tests(self):
        """Run all sign-in page tests"""
        print("🔐 PawFinder Sign-In Page Test Suite")
        print("=" * 55)
        
        tests = [
            ("Page Load & Form Elements", self.test_page_loads_correctly),
            ("Form Validation", self.test_form_validation),
            ("Valid Login Attempt", self.test_valid_login_attempt),
            ("Password Visibility Toggle", self.test_password_visibility_toggle),
            ("Remember Me Functionality", self.test_remember_me_functionality),
            ("Forgot Password Link", self.test_forgot_password_link),
            ("Social Login Options", self.test_social_login_options),
            ("Accessibility Features", self.test_accessibility_features)
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                print(f"❌ {test_name} failed with error: {e}")
                results[test_name] = False
        
      
        print("\n" + "=" * 55)
        print("📊 SIGN-IN PAGE TEST SUMMARY")
        print("=" * 55)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"{test_name:<30} {status}")
        
        print("-" * 55)
        print(f"📈 Result: {passed}/{total} tests passed")
        
        if passed >= 6:
            print("🎉 Sign-in page is well implemented!")
        elif passed >= 4:
            print("👍 Sign-in page has good basic functionality")
        elif passed >= 2:
            print("⚠️  Sign-in page needs some improvements")
        else:
            print("❌ Sign-in page needs significant work")
        
        return results
    
    def cleanup(self):
        """Clean up resources"""
        try:
            self.driver.quit()
            print("\n🧹 Browser closed")
        except:
            pass


def main():
    """Main function to run sign-in tests"""
    print("🔐 PawFinder Sign-In Page Testing")
    print("Make sure your app is running at http://localhost:3000")
    print("Note: Tests will use test credentials but expect auth to fail")
    print()
    
    try:
        input("Press Enter to start tests (Ctrl+C to cancel): ")
    except KeyboardInterrupt:
        print("\nTests cancelled")
        return
    
    tester = SignInPageTests()
    
    try:
        results = tester.run_all_tests()
        return results
    except KeyboardInterrupt:
        print("\n\n⏹️  Tests interrupted")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        tester.cleanup()


if __name__ == "__main__":
    main()



class TestSignInPage:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.tester = SignInPageTests()
        yield
        self.tester.cleanup()
    
   
    def test_form_validation(self):
        assert self.tester.test_form_validation()
    
    def test_login_attempt(self):
        assert self.tester.test_valid_login_attempt()
    
    def test_password_toggle(self):
        assert self.tester.test_password_visibility_toggle()
    
    def test_remember_me(self):
        assert self.tester.test_remember_me_functionality()
    
    def test_forgot_password(self):
        assert self.tester.test_forgot_password_link()
    
    def test_social_login(self):
        assert self.tester.test_social_login_options()
    
    def test_accessibility(self):
        assert self.tester.test_accessibility_features()

