from playwright.sync_api import expect, Page

class Pwlocators:
    def __init__(self, page:Page):

        self.page=page
        self.name=page.get_by_role("textbox", name="Enter Name")
        self.email=page.get_by_role("textbox", name="Enter EMail")
        self.phone=page.get_by_role("textbox", name="Enter Phone")



