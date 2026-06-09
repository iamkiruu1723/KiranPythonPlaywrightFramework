from playwright.sync_api import expect,Page

class Addcart:
    def __init__(self,page : Page):
        self.page= page
        self.searchbox=page.get_by_placeholder("Search")
        self.searchbutton=page.locator("button.btn.btn-default.btn-lg:visible")
        self.macbook = page.locator("#content").get_by_text("MacBook", exact=True)
        self.macbookair = page.locator("#content").get_by_text("MacBook Air", exact=True)
        self.macbookpro = page.locator("#content").get_by_text("MacBook Pro", exact=True)
        self.addtocart=page.locator("#button-cart")
        self.backsearch=page.get_by_role("link", name="Search")
        self.itemscart=page.locator("//span[@id='cart-total']")
        self.viewcart=page.get_by_text("View Cart", exact=True)
        self.cartpage_heading=page.locator("h1:visible").get_by_text('Shopping Cart')














