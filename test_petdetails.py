import pytest # type: ignore
from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
import time


class PetDetailPageTests:
    """Selenium test class for the Pet Details Page"""

    def __init__(self):
        self.url = "http://localhost:3000/pets/5"
        self.setup_driver()
        self.wait = WebDriverWait(self.driver, 10)

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Comment this if you want to see the browser
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

    def cleanup(self):
        self.driver.quit()

    def test_page_loads(self):
        """Check if the pet details page loads successfully"""
        self.driver.get(self.url)
        assert "pet" in self.driver.current_url.lower()
        assert self.driver.title != "" 



class TestPetDetailPage:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.tester = PetDetailPageTests()
        yield
        self.tester.cleanup()

    def test_page_loads(self):
        self.tester.test_page_loads()

    

#thik ase
