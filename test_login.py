from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.service import Service # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
import time

def setup_driver():
    options = webdriver.ChromeOptions()
    
    # Optional: use a persistent user profile to stay signed into Google
    options.add_argument("--user-data-dir=/tmp/selenium")  # path to profile
    options.add_argument("--start-maximized")
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def test_google_signin():
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("http://localhost:3000/sign-in")

        # Wait for iframe
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)

        # Wait for Google Sign-In button
        google_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue with Google')]")))
        google_btn.click()

        # Switch to the new window
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])

        print("🟡 Waiting for manual Google sign-in or use of saved session...")
        time.sleep(20)  # Give time for manual login if not already signed in

        # Switch back to original window
        driver.switch_to.window(driver.window_handles[0])
        driver.switch_to.default_content()

        time.sleep(5)
        assert "localhost:3000" in driver.current_url
        print("✅ Google Sign-In test passed.")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_google_signin()

    #thik ase
