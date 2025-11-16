import pytest
from playwright.sync_api import sync_playwright
import os


@pytest.fixture(scope="session")
def html_file_path():
    return "file://" + os.path.abspath("index.html")


def test_initial_display(html_file_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_file_path)

        # Check initial values
        assert page.locator("#budget").inner_text() == "$0.00"
        assert page.locator("#expenses").inner_text() == "$0.00"
        assert page.locator("#balance").inner_text() == "$0.00"
        assert page.locator("#savings").inner_text() == "$0.00"

        browser.close()


def test_expense_input_updates_totals(html_file_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_file_path)

        inputs = page.locator(".expense-input")
        inputs.nth(0).fill("100")   # Rent
        inputs.nth(1).fill("50")    # Utilities
        inputs.nth(2).fill("25")    # Groceries

        # Small wait to allow events to fire
        page.wait_for_timeout(200)

        assert page.locator("#expenses").inner_text() == "$175.00"

        browser.close()


def test_budget_add_button(html_file_path, monkeypatch):
    """
    Test clicking the budget Add+ button by mocking prompt return value.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Mock window.prompt() before page load
        page.add_init_script("""
            window.originalPrompt = window.prompt;
            window.prompt = () => "200";
        """)

        page.goto(html_file_path)
        
        # Click Add+ for budget
        page.locator('.update-btn[data-type="budget"]').click()

        page.wait_for_timeout(200)

        assert page.locator("#budget").inner_text() == "$200.00"

        browser.close()


def test_savings_add_button(html_file_path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.add_init_script("""
            window.originalPrompt = window.prompt;
            window.prompt = () => "50";
        """)

        page.goto(html_file_path)

        # Click Add+ for savings
        page.locator('.update-btn[data-type="savings"]').click()

        page.wait_for_timeout(200)

        assert page.locator("#savings").inner_text() == "$50.00"

        browser.close()
