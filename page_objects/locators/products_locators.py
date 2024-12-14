from playwright.sync_api import Page


class ProductList:
    def __init__(self, page: Page):
        self.page = page
        self.product_title__texts = page.locator(
            "//div[contains(@class, 'productinfo')]/p"
        )
        self.view_product__buttons = page.locator(
            "(//ancestor::div[contains(@class, 'productinfo')]/descendant::a)"
        )
        self.first_view_product__button = page.locator(
            "(//a[contains(text(), 'View Product')])[1]"
        )
        self.random_add_to_cart__button = page.locator(
            "(//a[contains(@class, 'add-to-cart')])[5]"
        )
        self.random_product_title__text = page.locator(
            "(//div[@class='productinfo text-center']/p)[3]"
        )
        self.category_title__text = page.locator("//h2[@class='title text-center']")


class ProductDetailPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_title__text = page.locator(
            "//div[@class='product-information']/h2"
        )
        self.add_to_cart__button = page.locator("//button[contains(@class, 'cart')]")
        self.product_quantity__input = page.locator("//input[@id='quantity']")


class ConfirmModal:
    def __init__(self, page: Page):
        self.page = page
        self.confirmed__modal = page.locator("[class='modal-dialog modal-confirm']")
        self.modal_product_added_title__text = page.locator(
            "//h4[contains(text(), 'Added!')]"
        )
        self.close_modal__button = page.locator(
            "//button[contains(@class, 'btn-success')]"
        )
        self.view_cart__button = page.locator(
            "//div[@class='modal-content']//a[@href='/view_cart']"
        )


class ProductOrder:
    def __init__(self, page: Page):
        self.page = page
        self.add_product_01__button = page.locator("(//a[@data-product-id='21'])[1]")
        self.add_product_02__button = page.locator("(//a[@data-product-id='43'])[1]")
        self.proceed_to_checkout__button = page.locator(
            "//a[text()='Proceed To Checkout']"
        )

        self.register_or_login__button = page.locator("//u[text()='Register / Login']")

        self.place_order__button = page.locator("//a[@href='/payment']")
        self.order_message__input = page.locator("//textarea[@name='message']")
        self.card_name__input = page.locator("[data-qa='name-on-card']")
        self.card_number__input = page.locator("[data-qa='card-number']")
        self.card_cvc__input = page.locator("[data-qa='cvc']")
        self.card_expiry_month__input = page.locator("[data-qa='expiry-month']")
        self.card_expiry_year__input = page.locator("[data-qa='expiry-year']")
        self.complete_payment__button = page.locator("[data-qa='pay-button']")

        self.confirm_order__text = page.locator("[data-qa='order-placed']")
        self.download_invoice__button = page.locator("//a[text()='Download Invoice']")


class SidePanel:
    def __init__(self, page: Page):
        self.page = page
        self.search__input = page.locator("[id='search_product']")
        self.search__button = page.locator("[id='submit_search']")
        self.men_category__button = page.locator("//a[@href='#Men']")
        self.jeans_sub_category__button = page.locator("//a[contains(text(), 'Jeans')]")


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_title__text = page.locator("//table[@id='cart_info_table']//h4/a")
        self.remove_item__button = page.locator("//a[@class='cart_quantity_delete']")
        self.empty_cart_message__text = page.locator("[id='empty_cart']")
        self.product_quantity__text = page.locator(
            "//td[@class='cart_quantity']/button"
        )
