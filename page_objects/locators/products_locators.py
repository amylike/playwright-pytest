from playwright.sync_api import Page


class ProductPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_bar_input = page.locator("[id='search_product']")
        self.search_submit_button = page.locator("[id='submit_search']")
        self.product_info_elements = page.locator(
            "//div[contains(@class, 'productinfo')]/p"
        )
        self.view_product_buttons = page.locator(
            "(//ancestor::div[contains(@class, 'productinfo')]/descendant::a)"
        )
        self.first_view_product_button = page.locator(
            "(//a[contains(text(), 'View Product')])[1]"
        )
        self.add_to_cart_button = page.locator(
            "(//a[contains(@class, 'add-to-cart')])[5]"
        )


class ProductDetail:
    def __init__(self, page: Page):
        self.page = page
        self.product_title = page.locator("//div[@class='product-information']/h2")
        self.add_to_cart_button = page.locator("//button[contains(@class, 'cart')]")


class ConfirmModal:
    def __init__(self, page: Page):
        self.page = page
        self.confirmed_modal = page.locator("[class='modal-dialog modal-confirm']")
        self.modal_added_title = page.locator("//h4[contains(text(), 'Added!')]")
        self.close_modal_button = page.locator(
            "//button[contains(@class, 'btn-success')]"
        )
        self.view_cart_button = page.locator(
            "//div[@class='modal-content']//a[@href='/view_cart']"
        )


class ProductOrder:
    def __init__(self, page: Page):
        self.page = page
        self.add_product_01_button = page.locator("(//a[@data-product-id='21'])[1]")
        self.add_product_02_button = page.locator("(//a[@data-product-id='43'])[1]")
        self.proceed_order_button = page.locator("//a[text()='Proceed To Checkout']")

        self.check_signin_button = page.locator("//u[text()='Register / Login']")

        self.place_order_button = page.locator("//a[@href='/payment']")
        self.message_input = page.locator("//textarea[@name='message']")
        self.card_name_input = page.locator("[data-qa='name-on-card']")
        self.card_number_input = page.locator("[data-qa='card-number']")
        self.card_cvc_input = page.locator("[data-qa='cvc']")
        self.card_expiry_month_input = page.locator("[data-qa='expiry-month']")
        self.card_expiry_year_input = page.locator("[data-qa='expiry-year']")
        self.complete_payment_button = page.locator("[data-qa='pay-button']")

        self.confirm_order_text = page.locator("[data-qa='order-placed']")
        self.download_invoice_button = page.locator("//a[text()='Download Invoice']")

    def get_by_text(self, num: str):
        element = self.page.locator(
            f"(//a[@data-product-id='{num}'])[1]/preceding-sibling::h2"
        )
        return element
