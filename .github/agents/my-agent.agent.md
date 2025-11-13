---
# Fill in the fields below to create a basic custom agent for your repository.
# The Copilot CLI can be used for local testing: https://gh.io/customagents/cli
# To make this agent available, merge this file into the default repository branch.
# For format details, see: https://gh.io/customagents/config

name: Copilot 
description: A custom agent to test SpendChart application functionality using Selenium.
---

# My Agent

 Create test_file.py with Selenium tests

    Add pytest and selenium dependencies to requirements.txt
    Creat comprehensive test suite with 9 test cases
    Tests load HTML file
    Tests fill input fields (Rent, Groceries, etc.)
    Tests simulate clicks on "Add+" buttons
    Tests verify totals and balances update correctly

Format code with linters (black for Python, prettier for JS/HTML)
Run and validate all tests
Code review
Security check with CodeQL
Add .gitignore for Python cache files
