from playwright.sync_api import expect,Page
from pages.pwlocatorspageu import Pwlocators
import pytest

def test_playwright_locators(page):
    pwlocator=Pwlocators(page)