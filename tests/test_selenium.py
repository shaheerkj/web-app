from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

BASE_URL = "http://localhost:5000"

class TestStudentRegistrationApp(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)

    # ---------- Test 1: Homepage loads correctly ----------
    def test_01_homepage_loads(self):
        self.driver.get(BASE_URL)
        self.assertIn("Student Registration", self.driver.title)
        heading = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertIn("Student Registration System", heading.text)
        print("✅ Test 1 Passed: Homepage loads correctly")

    # ---------- Test 2: Registration form exists ----------
    def test_02_form_elements_present(self):
        self.driver.get(BASE_URL)
        name_field = self.driver.find_element(By.ID, "name")
        email_field = self.driver.find_element(By.ID, "email")
        course_field = self.driver.find_element(By.ID, "course")
        submit_btn = self.driver.find_element(By.ID, "submit-btn")

        self.assertIsNotNone(name_field)
        self.assertIsNotNone(email_field)
        self.assertIsNotNone(course_field)
        self.assertIsNotNone(submit_btn)
        print("✅ Test 2 Passed: All form elements are present")

    # ---------- Test 3: Register a new student ----------
    def test_03_register_student(self):
        self.driver.get(BASE_URL)

        self.driver.find_element(By.ID, "name").send_keys("Ali Hassan")
        self.driver.find_element(By.ID, "email").send_keys("ali@comsats.edu.pk")

        course_dropdown = Select(self.driver.find_element(By.ID, "course"))
        course_dropdown.select_by_value("DevOps")

        self.driver.find_element(By.ID, "submit-btn").click()
        time.sleep(2)

        # After redirect, check the student appears in the table
        page_source = self.driver.page_source
        self.assertIn("Ali Hassan", page_source)
        print("✅ Test 3 Passed: Student registered and appears in table")

    # ---------- Test 4: Health endpoint works ----------
    def test_04_health_endpoint(self):
        self.driver.get(f"{BASE_URL}/health")
        self.assertIn("ok", self.driver.page_source)
        print("✅ Test 4 Passed: Health endpoint returns ok")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
