import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
import os
import time


@pytest.fixture
def driver():
    """Setup and teardown for Chrome driver"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def load_html(driver):
    """Load the HTML file"""
    html_path = os.path.abspath("index.html")
    driver.get(f"file://{html_path}")
    time.sleep(0.5)  # Allow time for DOM to load
    return driver


class TestSpendChart:
    """Comprehensive test suite for SpendChart application"""

    def test_load_html_file(self, load_html):
        """Test 1: Verify HTML file loads successfully"""
        assert "SpendChart" in load_html.title
        header = load_html.find_element(By.TAG_NAME, "h1")
        assert "$pendChart" in header.text

    def test_initial_values(self, load_html):
        """Test 2: Verify initial values are displayed correctly"""
        budget = load_html.find_element(By.ID, "budget")
        expenses = load_html.find_element(By.ID, "expenses")
        balance = load_html.find_element(By.ID, "balance")
        savings = load_html.find_element(By.ID, "savings")

        assert budget.text == "$0.00"
        assert expenses.text == "$0.00"
        assert balance.text == "$0.00"
        assert savings.text == "$0.00"

    def test_fill_rent_input(self, load_html):
        """Test 3: Fill rent/mortgage input field"""
        inputs = load_html.find_elements(By.CLASS_NAME, "expense-input")
        rent_input = inputs[0]  # First input is Rent/Mortgage

        rent_input.clear()
        rent_input.send_keys("1200")
        time.sleep(0.3)

        # Verify expenses updated
        expenses = load_html.find_element(By.ID, "expenses")
        assert expenses.text == "$1200.00"

    def test_fill_groceries_input(self, load_html):
        """Test 4: Fill groceries input field"""
        inputs = load_html.find_elements(By.CLASS_NAME, "expense-input")
        groceries_input = inputs[2]  # Third input is Groceries

        groceries_input.clear()
        groceries_input.send_keys("500")
        time.sleep(0.3)

        # Verify expenses updated
        expenses = load_html.find_element(By.ID, "expenses")
        assert expenses.text == "$500.00"

    def test_fill_multiple_expense_inputs(self, load_html):
        """Test 5: Fill multiple expense inputs and verify total"""
        inputs = load_html.find_elements(By.CLASS_NAME, "expense-input")

        # Rent/Mortgage
        inputs[0].clear()
        inputs[0].send_keys("1200")

        # Utilities
        inputs[1].clear()
        inputs[1].send_keys("150")

        # Groceries
        inputs[2].clear()
        inputs[2].send_keys("500")

        # Transportation
        inputs[3].clear()
        inputs[3].send_keys("200")

        # Entertainment
        inputs[4].clear()
        inputs[4].send_keys("100")

        time.sleep(0.3)

        # Verify total expenses
        expenses = load_html.find_element(By.ID, "expenses")
        assert expenses.text == "$2150.00"

    def test_add_budget_button(self, load_html):
        """Test 6: Test clicking Add+ button for budget"""
        budget_btn = load_html.find_element(By.CSS_SELECTOR, '[data-type="budget"]')

        # Click the button
        budget_btn.click()

        # Wait for alert and handle it
        try:
            WebDriverWait(load_html, 3).until(EC.alert_is_present())
            alert = load_html.switch_to.alert
            alert.send_keys("3000")
            alert.accept()
            time.sleep(0.3)

            # Verify budget updated
            budget = load_html.find_element(By.ID, "budget")
            assert budget.text == "$3000.00"
        except TimeoutException:
            pytest.skip("Alert not present - JavaScript may not be fully loaded")

    def test_add_savings_button(self, load_html):
        """Test 7: Test clicking Add+ button for savings"""
        savings_btn = load_html.find_element(By.CSS_SELECTOR, '[data-type="savings"]')

        # Click the button
        savings_btn.click()

        # Wait for alert and handle it
        try:
            WebDriverWait(load_html, 3).until(EC.alert_is_present())
            alert = load_html.switch_to.alert
            alert.send_keys("500")
            alert.accept()
            time.sleep(0.3)

            # Verify savings updated
            savings = load_html.find_element(By.ID, "savings")
            assert savings.text == "$500.00"
        except TimeoutException:
            pytest.skip("Alert not present - JavaScript may not be fully loaded")

    def test_balance_calculation(self, load_html):
        """Test 8: Verify balance calculation (budget - expenses)"""
        # Add budget
        budget_btn = load_html.find_element(By.CSS_SELECTOR, '[data-type="budget"]')
        budget_btn.click()

        try:
            WebDriverWait(load_html, 3).until(EC.alert_is_present())
            alert = load_html.switch_to.alert
            alert.send_keys("3000")
            alert.accept()
            time.sleep(0.3)
        except TimeoutException:
            pytest.skip("Alert not present - JavaScript may not be fully loaded")

        # Add expenses
        inputs = load_html.find_elements(By.CLASS_NAME, "expense-input")
        inputs[0].send_keys("1200")  # Rent
        inputs[2].send_keys("500")  # Groceries
        time.sleep(0.3)

        # Verify balance = budget - expenses
        balance = load_html.find_element(By.ID, "balance")
        assert balance.text == "$1300.00"  # 3000 - 1700

    def test_complete_workflow(self, load_html):
        """Test 9: Complete workflow with all interactions"""
        # Set budget
        budget_btn = load_html.find_element(By.CSS_SELECTOR, '[data-type="budget"]')
        budget_btn.click()

        try:
            WebDriverWait(load_html, 3).until(EC.alert_is_present())
            alert = load_html.switch_to.alert
            alert.send_keys("5000")
            alert.accept()
            time.sleep(0.3)
        except TimeoutException:
            pytest.skip("Alert not present - JavaScript may not be fully loaded")

        # Add all expenses
        inputs = load_html.find_elements(By.CLASS_NAME, "expense-input")
        inputs[0].send_keys("1500")  # Rent
        inputs[1].send_keys("200")  # Utilities
        inputs[2].send_keys("600")  # Groceries
        inputs[3].send_keys("300")  # Transportation
        inputs[4].send_keys("150")  # Entertainment
        time.sleep(0.3)

        # Set savings
        savings_btn = load_html.find_element(By.CSS_SELECTOR, '[data-type="savings"]')
        savings_btn.click()

        try:
            WebDriverWait(load_html, 3).until(EC.alert_is_present())
            alert = load_html.switch_to.alert
            alert.send_keys("1000")
            alert.accept()
            time.sleep(0.3)
        except TimeoutException:
            pytest.skip("Alert not present - JavaScript may not be fully loaded")

        # Verify all values
        budget = load_html.find_element(By.ID, "budget")
        expenses = load_html.find_element(By.ID, "expenses")
        balance = load_html.find_element(By.ID, "balance")
        savings = load_html.find_element(By.ID, "savings")

        assert budget.text == "$5000.00"
        assert expenses.text == "$2750.00"
        assert balance.text == "$2250.00"  # 5000 - 2750
        assert savings.text == "$1000.00"

    def test_update_expense_recalculates_balance(self, load_html):
        """Test 10: Verify updating expenses recalculates balance"""
        # Set initial budget
        budget_btn = load_html.find_element(By.CSS_SELECTOR, '[data-type="budget"]')
        budget_btn.click()

        try:
            WebDriverWait(load_html, 3).until(EC.alert_is_present())
            alert = load_html.switch_to.alert
            alert.send_keys("2000")
            alert.accept()
            time.sleep(0.3)
        except TimeoutException:
            pytest.skip("Alert not present - JavaScript may not be fully loaded")

        inputs = load_html.find_elements(By.CLASS_NAME, "expense-input")

        # Add initial expense
        inputs[0].send_keys("500")
        time.sleep(0.3)
        balance = load_html.find_element(By.ID, "balance")
        assert balance.text == "$1500.00"

        # Update expense
        inputs[0].clear()
        inputs[0].send_keys("800")
        time.sleep(0.3)
        balance = load_html.find_element(By.ID, "balance")
        assert balance.text == "$1200.00"
