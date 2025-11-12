"""
Test file for SpendChart HTML application.
Tests loading HTML, filling inputs, clicking buttons, and verifying calculations.
"""

import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException


class TestSpendChart:
    """Test suite for SpendChart application."""

    @pytest.fixture(scope="class")
    def driver(self):
        """Setup Chrome WebDriver in headless mode."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()

    @pytest.fixture(autouse=True)
    def load_page(self, driver):
        """Load the HTML page before each test."""
        html_path = os.path.abspath("index.html")
        driver.get(f"file://{html_path}")
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "budget"))
        )

    def test_page_loads(self, driver):
        """Test that the HTML page loads successfully."""
        assert "SpendChart" in driver.title
        assert driver.find_element(By.ID, "budget") is not None
        assert driver.find_element(By.ID, "expenses") is not None
        assert driver.find_element(By.ID, "balance") is not None
        assert driver.find_element(By.ID, "savings") is not None

    def test_expense_inputs_exist(self, driver):
        """Test that all expense input fields exist."""
        expense_inputs = driver.find_elements(By.CLASS_NAME, "expense-input")
        assert (
            len(expense_inputs) == 5
        )  # Rent, Utilities, Groceries, Transportation, Entertainment

    def test_fill_rent_input(self, driver):
        """Test filling the Rent/Mortgage input field."""
        expense_inputs = driver.find_elements(By.CLASS_NAME, "expense-input")
        rent_input = expense_inputs[0]  # First input is Rent/Mortgage

        rent_input.clear()
        rent_input.send_keys("1200")

        assert rent_input.get_attribute("value") == "1200"

    def test_fill_groceries_input(self, driver):
        """Test filling the Groceries input field."""
        expense_inputs = driver.find_elements(By.CLASS_NAME, "expense-input")
        groceries_input = expense_inputs[2]  # Third input is Groceries

        groceries_input.clear()
        groceries_input.send_keys("500")

        assert groceries_input.get_attribute("value") == "500"

    def test_total_expenses_calculation(self, driver):
        """Test that total expenses are calculated correctly when inputs are filled."""
        expense_inputs = driver.find_elements(By.CLASS_NAME, "expense-input")

        # Fill multiple expense inputs
        expense_inputs[0].send_keys("1200")  # Rent
        expense_inputs[2].send_keys("500")  # Groceries
        expense_inputs[3].send_keys("200")  # Transportation

        # Wait for expenses to update
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "expenses").text != "$0.00"
        )

        expenses_text = driver.find_element(By.ID, "expenses").text
        assert expenses_text == "$1900.00"

    def test_add_budget_button(self, driver):
        """Test clicking the Add+ button for budget."""
        budget_button = driver.find_element(By.CSS_SELECTOR, '[data-type="budget"]')

        # Click the budget Add+ button
        budget_button.click()

        # Wait for alert to appear and handle it
        try:
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.send_keys("3000")
            alert.accept()

            # Wait for budget to update
            WebDriverWait(driver, 10).until(
                lambda d: d.find_element(By.ID, "budget").text == "$3000.00"
            )

            budget_text = driver.find_element(By.ID, "budget").text
            assert budget_text == "$3000.00"
        except UnexpectedAlertPresentException:
            pytest.fail("Alert handling failed")

    def test_add_savings_button(self, driver):
        """Test clicking the Add+ button for savings."""
        savings_button = driver.find_element(By.CSS_SELECTOR, '[data-type="savings"]')

        # Click the savings Add+ button
        savings_button.click()

        # Wait for alert to appear and handle it
        try:
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.send_keys("1000")
            alert.accept()

            # Wait for savings to update
            WebDriverWait(driver, 10).until(
                lambda d: d.find_element(By.ID, "savings").text == "$1000.00"
            )

            savings_text = driver.find_element(By.ID, "savings").text
            assert savings_text == "$1000.00"
        except UnexpectedAlertPresentException:
            pytest.fail("Alert handling failed")

    def test_balance_calculation(self, driver):
        """Test that remaining balance is calculated correctly (Budget - Expenses)."""
        # Set budget first
        budget_button = driver.find_element(By.CSS_SELECTOR, '[data-type="budget"]')
        budget_button.click()

        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.send_keys("3000")
        alert.accept()

        # Wait for budget to update
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "budget").text == "$3000.00"
        )

        # Add expenses
        expense_inputs = driver.find_elements(By.CLASS_NAME, "expense-input")
        expense_inputs[0].send_keys("1200")  # Rent
        expense_inputs[2].send_keys("500")  # Groceries

        # Wait for balance to update
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "balance").text == "$1300.00"
        )

        balance_text = driver.find_element(By.ID, "balance").text
        assert balance_text == "$1300.00"  # 3000 - 1200 - 500 = 1300

    def test_complete_workflow(self, driver):
        """Test complete workflow: set budget, add expenses, verify all totals and balance."""
        # Step 1: Set budget
        budget_button = driver.find_element(By.CSS_SELECTOR, '[data-type="budget"]')
        budget_button.click()

        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.send_keys("5000")
        alert.accept()

        # Wait for budget to update
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "budget").text == "$5000.00"
        )

        # Step 2: Set savings
        savings_button = driver.find_element(By.CSS_SELECTOR, '[data-type="savings"]')
        savings_button.click()

        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.send_keys("1500")
        alert.accept()

        # Wait for savings to update
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "savings").text == "$1500.00"
        )

        # Step 3: Fill expense inputs
        expense_inputs = driver.find_elements(By.CLASS_NAME, "expense-input")
        expense_inputs[0].send_keys("1500")  # Rent
        expense_inputs[1].send_keys("200")  # Utilities
        expense_inputs[2].send_keys("600")  # Groceries
        expense_inputs[3].send_keys("150")  # Transportation
        expense_inputs[4].send_keys("100")  # Entertainment

        # Step 4: Verify all calculations
        # Wait for expenses to update
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.ID, "expenses").text == "$2550.00"
        )

        budget_text = driver.find_element(By.ID, "budget").text
        expenses_text = driver.find_element(By.ID, "expenses").text
        balance_text = driver.find_element(By.ID, "balance").text
        savings_text = driver.find_element(By.ID, "savings").text

        assert budget_text == "$5000.00"
        assert expenses_text == "$2550.00"
        assert balance_text == "$2450.00"  # 5000 - 2550 = 2450
        assert savings_text == "$1500.00"
