from playwright.sync_api import expect,Page
from pages.cart_pageu import Addcart
from pages.login_page import LoginPage
from pages.home_page import HomePage
from config import Config

def test_login_and_cart(page):
    loginpage =LoginPage(page)
    homeu = HomePage(page)
    cartpage = Addcart(page)
    config=Config()


    homeu.click_my_account()
    homeu.click_login()


    loginpage.set_email(Config.email)
    loginpage.set_password(Config.password)
    loginpage.click_login()

    cartpage.searchbox.click()
    cartpage.searchbox.fill("Macbook")
    cartpage.searchbutton.click()

    cartpage.macbook.click()
    cartpage.addtocart.click()
    page.wait_for_timeout(2000)
    cartpage.backsearch.click()
    page.wait_for_timeout(2000)

    cartpage.macbookair.click()
    cartpage.addtocart.click()
    cartpage.backsearch.click()
    page.wait_for_timeout(2000)

    cartpage.macbookpro.click()
    cartpage.addtocart.click()
    page.wait_for_timeout(2000)

    cartpage.itemscart.click()
    cartpage.viewcart.click()
    expect(cartpage.cartpage_heading).to_be_visible()



















