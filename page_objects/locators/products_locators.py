from playwright.sync_api import Page


class ProductList:
    def __init__(self, page: Page):
        self.page = page
        self.product_title_texts = page.locator(
            "//div[contains(@class, 'productinfo')]/p"
        )
        self.view_product_buttons = page.locator(
            "(//ancestor::div[contains(@class, 'productinfo')]/descendant::a)"
        )
        self.first_view_product_button = page.locator(
            "(//a[contains(text(), 'View Product')])[1]"
        )
        self.random_add_to_cart_button = page.locator(
            "(//a[contains(@class, 'add-to-cart')])[5]"
        )
        self.random_product_title_text = page.locator(
            "(//div[@class='productinfo text-center']/p)[3]"
        )
        self.category_title_text = page.locator("//h2[@class='title text-center']")


class ProductDetailPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_title_text = page.locator("//div[@class='product-information']/h2")
        self.add_to_cart_button = page.locator("//button[contains(@class, 'cart')]")
        self.product_quantity_input = page.locator("//input[@id='quantity']")


class ConfirmModal:
    def __init__(self, page: Page):
        self.page = page
        self.confirmed_modal = page.locator("[class='modal-dialog modal-confirm']")
        self.modal_product_added_title_text = page.locator(
            "//h4[contains(text(), 'Added!')]"
        )
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
        self.proceed_to_checkout_button = page.locator(
            "//a[text()='Proceed To Checkout']"
        )

        self.register_or_login_button = page.locator("//u[text()='Register / Login']")

        self.place_order_button = page.locator("//a[@href='/payment']")
        self.order_message_input = page.locator("//textarea[@name='message']")
        self.card_name_input = page.locator("[data-qa='name-on-card']")
        self.card_number_input = page.locator("[data-qa='card-number']")
        self.card_cvc_input = page.locator("[data-qa='cvc']")
        self.card_expiry_month_input = page.locator("[data-qa='expiry-month']")
        self.card_expiry_year_input = page.locator("[data-qa='expiry-year']")
        self.complete_payment_button = page.locator("[data-qa='pay-button']")

        self.confirm_order_text = page.locator("[data-qa='order-placed']")
        self.download_invoice_button = page.locator("//a[text()='Download Invoice']")


class SidePanel:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.locator("[id='search_product']")
        self.search_button = page.locator("[id='submit_search']")
        self.men_category_button = page.locator("//a[@href='#Men']")
        self.jeans_sub_category_button = page.locator("//a[contains(text(), 'Jeans')]")


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_title_text = page.locator("//table[@id='cart_info_table']//h4/a")
        self.remove_item_button = page.locator("//a[@class='cart_quantity_delete']")
        self.empty_cart_message_text = page.locator("[id='empty_cart']")
        self.product_quantity_text = page.locator("//td[@class='cart_quantity']/button")
