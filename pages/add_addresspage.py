from playwright.sync_api import expect, Page

class AddressPage:
    def __init__(self, page:Page):

        self.page=page

        self.modify_addbukentry =page.get_by_text("Modify your address book entries")
        self.new_adress_btn = page.get_by_text("New Address", exact=True)
        self.first_nameu = page.locator("#input-firstname")
        self.lastname = page.get_by_placeholder("Last Name")
        self.company= page.get_by_role("textbox", name="Company")
        self.addres1= page.get_by_label("Address 1")
        self.address2 =page.get_by_label("Address 2")
        self.city=page.get_by_placeholder("City")
        self.postalcode=page.get_by_placeholder("Post Code")
        self.country=page.locator("#input-country")
        self.state=page.locator("#input-zone")
        self.submit=page.locator("input[type='submit']")
        self.radiobtn=page.get_by_label("Yes", exact=True)
        page.wait_for_timeout(2000)
        self.radiobtn_no = page.get_by_label("No", exact=True)
        self.address_added=page.get_by_text("Your address has been successfully added", exact=True)
        self.address_deleted=page.get_by_text("Your address has been successfully deleted", exact=True)

        #nextpage

        self.lastdelete=page.locator("a:has-text('Delete')")





