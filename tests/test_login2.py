"""
Test Case: User Login Functionality

===========================================
Test Steps
===========================================

Test Case 1: Verify Login with Invalid Credentials
--------------------------------------------------
1. Open the application in the browser.
2. Navigate to the "My Account" menu on the Home page.
3. Click on the "Login" link.
4. Enter an invalid email address and password.
5. Click on the "Login" button.
6. Verify that an error message appears indicating invalid credentials.

Expected Result:
----------------
An error message should be displayed, and the user should not be logged in.


Test Case 2: Verify Login with Valid Credentials
------------------------------------------------
1. Open the application in the browser.
2. Navigate to the "My Account" menu on the Home page.
3. Click on the "Login" link.
4. Enter a valid email address and password.
5. Click on the "Login" button.
6. Verify that the "My Account" page is displayed after successful login.

Expected Result:
----------------
The "My Account" page should appear, confirming a successful login.
"""

import pytest
import time

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.my_account_page import MyAccountPage
from pages.add_addresspageu import AddressPage
from playwright.sync_api import expect
from utilities import random_data_util
from config import Config

def test_valid_login_kiran(page):
   login_page= LoginPage(page)
   home_page=HomePage(page)
   my_acc_page=MyAccountPage(page)
   Addressu=AddressPage(page)
   fakeru=random_data_util.RandomDataUtil()

   home_page.click_my_account()
   home_page.click_login()


   login_page.set_email(Config.email)
   login_page.set_password(Config.password)
   login_page.click_login()


   Addressu.modify_addbukentry.click()
   Addressu.new_adress_btn.click()
   Addressu.first_nameu.fill(fakeru.get_first_name()+" kiran")
   Addressu.lastname.fill(fakeru.get_last_name())
   Addressu.company.fill(fakeru.get_random_company())
   Addressu.addres1.fill(fakeru.get_random_address())
   Addressu.address2.fill(fakeru.get_random_address() + "123 street")
   Addressu.city.fill(fakeru.get_random_city())
   Addressu.postalcode.fill(fakeru.get_random_pin())

   Addressu.country.select_option(label="India")
   Addressu.state.select_option(label="Karnataka")
   Addressu.radiobtn_no.check()

   Addressu.submit.click()
   page.wait_for_timeout(5000)
   # expect(Addressu.address_added).to_be_visible()
   expect(Addressu.address_added).to_be_visible(timeout=5000)
   expect(Addressu.address_added).to_have_text("Your address has been successfully added")

   Addressu.lastdelete.nth(-2).click()
   page.wait_for_timeout(5000)
   expect(Addressu.address_deleted).to_be_visible(timeout=2000)
   expect(Addressu.address_deleted).to_have_text("Your address has been successfully deleted")









def test_invalid_login_kiran(page):
   loginu=LoginPage(page)
   homeu=HomePage(page)
   account=MyAccountPage(page)

   homeu.click_my_account()
   homeu.click_login()
   page.wait_for_timeout(5000)

   loginu.set_email("kiranlearnsdaily@gmail.com")
   page.wait_for_timeout(2000)
   loginu.set_password("Test@17213")
   loginu.click_login()
   page.wait_for_timeout(2000)

   expect(loginu.get_login_error()).to_be_visible(timeout=3000)










