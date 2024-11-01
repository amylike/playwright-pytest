import os

import requests
from playwright.sync_api import Page
from typing import Dict, Optional

from page_objects.locators.common_locators import Menu
from page_objects.locators.products_locators import (
    ProductList,
    ProductDetailPage,
    ConfirmModal,
    ProductOrder,
    SidePanel,
    CartPage,
)
from page_objects.path import Path
from test_script.account.conftest import input_signin_data


def go_to_product_url(page: Page):
    """Products 리스트 페이지로 이동"""
    page.goto(Path.PRODUCTS_URL)


def search_keyword(page: Page, keyword: str):
    """검색창에 키워드를 입력하고, 검색 결과에 키워드가 포함되었는지 검증"""
    SidePanel(page).search_input.fill(keyword)
    SidePanel(page).search_button.click()

    product_titles = ProductList(page).product_titles.all()
    if not product_titles:
        raise AssertionError(f"No products found for keyword: {keyword}")
    for element in product_titles:
        text_content = element.text_content().lower()
        assert keyword in text_content


def search_items(page: Page, test_data: Dict[str, str]):
    """제품 리스트 페이지에서 특정 키워드를 검색"""
    go_to_product_url(page)
    search_keyword(page, test_data["keyword"])


def list_to_product_detail(page: Page, keyword: Dict[str, str]):
    """검색 결과에서 첫번째 item 상세 페이지 접근"""
    ProductList(page).first_view_product_button.click()
    product_title_text = (
        ProductDetailPage(page).product_title_text.text_content().lower()
    )
    assert keyword["keyword"] in product_title_text


def confirmed_modal_to_cart(page: Page):
    """장바구니 확인 모달에서 장바구니로 이동"""
    ConfirmModal(page).confirmed_modal.is_visible()
    ConfirmModal(page).modal_product_added_title_text.is_visible()
    ConfirmModal(page).view_cart_button.click()


def confirm_product_added_to_cart(
    page: Page, compared_title_text: str, quantity: Optional[str]
):
    """선택한 제품과 장바구니에 담긴 제품이 동일한 제품인지 체크"""
    CartPage(page).product_title_text.is_visible()

    cart_product_title_text = CartPage(page).product_title_text.text_content()
    cart_product_quantity = CartPage(page).product_quantity_text.text_content()

    assert compared_title_text == cart_product_title_text
    if quantity is not None:
        assert quantity == cart_product_quantity


def check_signin_before_order(page: Page, email: str, password: str):
    ProductOrder(page).proceed_to_checkout_button.click()
    if not Menu(page).logout_nav_button.is_visible():
        ProductOrder(page).register_or_login_button.click()
        input_signin_data(page, email, password)
        Menu(page).cart_nav_button.click()
        ProductOrder(page).proceed_to_checkout_button.click()


def add_to_cart_with_info(page: Page, product_number: str) -> Dict[str, str]:
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


def get_info_from_cart(page: Page, product_number) -> Dict[str, str]:
    """제품의 이름과 가격 정보를 저장하여 리턴"""
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
    card_name: str,
    card_number: str,
    card_cvc: str,
    card_expiry_month: str,
    card_expiry_year: str,
):
    """결제 카드 정보 입력"""
    ProductOrder(page).card_name_input.fill(card_name)
    ProductOrder(page).card_number_input.fill(card_number)
    ProductOrder(page).card_cvc_input.fill(card_cvc)
    ProductOrder(page).card_expiry_month_input.fill(card_expiry_month)
    ProductOrder(page).card_expiry_year_input.fill(card_expiry_year)


def calculate_total_price(page: Page) -> str:
    """각 제품에 대해 가격과 수량을 기반으로 총금액을 구하고, 모든 총금액을 더해 전체 구매 총액을 계산"""
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


def download_invoice(page: Page, total_purchase_amount: str):
    """주문 및 결제 완료 후 발급된 인보이스를 다운로드 받아 총 결제 금액 비교"""
    ProductOrder(page).download_invoice_button.is_visible()
    ProductOrder(page).download_invoice_button.click()

    filename = "invoice.txt"
    current_url = page.url
    invoice_num = current_url.split("/")[-1]
    formatted_invoice_num = "{:.1f}".format(float(invoice_num))
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
