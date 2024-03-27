import os

import requests
from playwright.sync_api import Page

from page_objects.locators.common_locators import Menu
from page_objects.locators.products_locators import (
    ProductPage,
    ProductDetail,
    ConfirmModal,
    ProductOrder,
)
from page_objects.path import Path
from test_script.account.conftest import input_signin_data


def go_to_product_url(page):
    # Products 페이지로 이동
    page.goto(Path.PRODUCTS_URL)


def search_keyword(page, keyword):
    # 검색창에 키워드를 입력
    ProductPage(page).search_bar_input.fill(keyword)
    ProductPage(page).search_submit_button.click()

    # 검색 결과에 키워드가 포함되었는지 검증
    product_info_elements = ProductPage(page).product_info_elements.all()
    for element in product_info_elements:
        text_content = element.text_content().lower()
        assert keyword in text_content


def list_to_product_detail(page: Page, keyword):
    # 검색 결과에서 첫번째 item 상세 페이지 접근
    ProductPage(page).first_view_product_button.click()
    title_text = ProductDetail(page).product_title.text_content().lower()
    assert keyword["keyword"] in title_text


def check_signin_before_order(page: Page, email, password):
    ProductOrder(page).proceed_order_button.click()
    if not Menu(page).logout_nav_button.is_visible():
        ProductOrder(page).check_signin_button.click()
        input_signin_data(page, email, password)
        Menu(page).cart_nav_button.click()
        ProductOrder(page).proceed_order_button.click()


def add_to_cart_with_info(page: Page, product_number) -> dict:
    """제품 번호를 통해 제품 이름과 가격 정보를 저장하고 해당 제품을 장바구니에 추가"""
    product_info = {}
    product_price_element = page.locator(
        f"(//a[@data-product-id='{product_number}'])[1]/preceding-sibling::h2"
    )
    product_name_element = page.locator(
        f"(//a[@data-product-id='{product_number}'])[1]/preceding-sibling::p"
    )
    product_price_text = product_price_element.inner_text()
    product_name_text = product_name_element.inner_text()
    product_info["product_price"] = product_price_text
    product_info["product_name"] = product_name_text

    product_add_cart_button = page.locator(
        f"(//a[@data-product-id='{product_number}'])[1]"
    )
    product_add_cart_button.click()
    ConfirmModal(page).close_modal_button.click()

    return product_info


def get_info_from_cart(page: Page, product_number):
    cart_product_info = {}
    product_price_element = page.locator(
        f"//tr[@id='product-{product_number}']/td[@class='cart_price']/p"
    )
    product_name_element = page.locator(
        f"//a[@href='/product_details/{product_number}']"
    )
    product_price_text = product_price_element.inner_text()
    product_name_text = product_name_element.inner_text()
    cart_product_info["product_price"] = product_price_text
    cart_product_info["product_name"] = product_name_text

    return cart_product_info


def input_card_data(
    page: Page,
    card_name=None,
    card_number=None,
    card_cvc=None,
    card_expiry_month=None,
    card_expiry_year=None,
):
    ProductOrder(page).card_name_input.fill(card_name)
    ProductOrder(page).card_number_input.fill(card_number)
    ProductOrder(page).card_cvc_input.fill(card_cvc)
    ProductOrder(page).card_expiry_month_input.fill(card_expiry_month)
    ProductOrder(page).card_expiry_year_input.fill(card_expiry_year)


def calculate_total_price(page: Page):
    """"각 제품에 대해 가격과 수량을 기반으로 총금액을 구하고, 모든 총금액을 더해 전체 구매 총액을 계산"""
    price_elements = page.locator(".cart_price").all()
    quantity_elements = page.locator(".cart_quantity").all()
    total_price_elements = page.locator(".cart_total_price").all()

    total_purchase_amount = 0

    for price_element, quantity_element, total_price_element in zip(
        price_elements, quantity_elements, total_price_elements
    ):
        price = float(price_element.inner_text().split(" ")[1])
        quantity = int(quantity_element.inner_text())
        total_price = float(total_price_element.inner_text().split(" ")[1])

        assert price * quantity == total_price

        total_purchase_amount += total_price

    return str(total_purchase_amount)


def download_invoice(page: Page, total_purchase_amount):
    """주문 및 결제 완료 후 발급된 인보이스를 다운로드 받아 총 결제 금액 비교"""
    ProductOrder(page).download_invoice_button.is_visible()
    ProductOrder(page).download_invoice_button.click()

    filename = "invoice.txt"
    current_url = page.url
    invoice_num = current_url.split("/")[-1]
    formatted_invoice_num = '{:.1f}'.format(float(invoice_num))
    invoice_url = os.path.join(Path.BASE_URL, "download_invoice", invoice_num)

    assert formatted_invoice_num == total_purchase_amount

    response = requests.get(invoice_url)
    try:
        with open(filename, "wb") as file:
            file.write(response.content)
        with open(filename, "r") as file:
            invoice_content = file.read()

        assert (
            invoice_content
            == "Hi , Your total purchase amount is {}. Thank you".format(invoice_num)
        )
    finally:
        os.remove(filename)
