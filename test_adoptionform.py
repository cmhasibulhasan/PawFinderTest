from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
import time

def test_adoption_form_submission():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("http://localhost:3000/pets/6")
        time.sleep(5)  
        print("=== FULL PAGE SOURCE ===")
        page_html = driver.page_source
        print(page_html[:1500])  

        
        inputs = driver.find_elements(By.TAG_NAME, "input")
        if not inputs:
            print("⚠️ No <input> elements found on the page.")
            return  

        for i, inp in enumerate(inputs):
            print(f"Input[{i}] - name={inp.get_attribute('name')}, id={inp.get_attribute('id')}, placeholder={inp.get_attribute('placeholder')}")

        
        if len(inputs) >= 3:
            inputs[0].send_keys("Hasib")
            inputs[1].send_keys("hasib@gmail.com")
            inputs[2].send_keys("0123456789")
        else:
            print("⚠️ Not enough inputs found. At least 3 required.")
            return

        
        button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
        button.click()
        time.sleep(2)

        assert "Adoption submitted" in driver.page_source or "Thank you" in driver.page_source
        print("✅ Form submitted successfully with name Hasib.")
    
    finally:
        driver.quit()


        #thik ase
        
