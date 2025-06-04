from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
import time

def test_homepage_loads_and_signin_button():
    driver = webdriver.Chrome()
    driver.get("http://localhost:3000/")

    try:
       
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1")) 
        )

        print(" Homepage loaded")

        
        signin_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sign In"))  
        )
        signin_button.click()

      
        WebDriverWait(driver, 10).until(
            EC.url_contains("/sign-in")
        )

        print(" Sign In link works and redirected correctly.")

    except Exception as e:
        print(" Homepage test failed:", e)
        print(driver.page_source)  

    finally:
        time.sleep(2)
        driver.quit()

#thik ase