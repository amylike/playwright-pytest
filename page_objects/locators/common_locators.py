from playwright.sync_api import Page


class Menu:
    def __init__(self, page: Page):
        self.page = page
        self.products_nav_button = page.locator("//a[@href='/products']")
        self.cart_nav_button = page.locator("//li//a[@href='/view_cart']")
        self.account_nav_button = page.locator("//a[@href='/login']")
        self.logout_nav_button = page.locator("//a[@href='/logout']")

        self.password_input = page.locator("[data-qa='login-password']")
