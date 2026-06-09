from playwright.sync_api import expect,Page
from pages.login_page import LoginPage
from pages.home_page import HomePage
from config import Config

def test_inspectoru(page):
    page.goto("https://tutorialsninja.com/demo/index.php?route=common/home")