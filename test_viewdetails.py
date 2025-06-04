from selenium import webdriver # type: ignore 
from selenium.webdriver.common.by import By # type: ignore 
from selenium.webdriver.support.ui import WebDriverWait # type: ignore 
from selenium.webdriver.support import expected_conditions as EC # type: ignore 
import time

def test_view_details_from_homepage():
    driver = webdriver.Chrome()
    driver.get("http://localhost:3000/")

    try:
        view_details_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'View Details')]"))
        )
        view_details_btn.click()

        WebDriverWait(driver, 10).until(
            EC.url_contains("/details")
        )

        detail_header = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        print("✅ View Details works. Detail page loaded with:", detail_header.text)

    except Exception as e:
        print("❌ View Details test failed:", e)
        print(driver.page_source)

    finally:
        time.sleep(2)
        driver.quit()

  #thik ase