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
from test_scripts.account.conftest import input_signin_data


def go_to_product_url(page: Page):
    """
    Products 리스트 페이지로 이동
    """
    page.goto(Path.PRODUCTS_URL)


def search_keyword(page: Page, keyword: str):
    """
    검색창에 키워드를 입력하고, 검색 결과에 키워드가 포함되었는지 검증
    """
    product_list = ProductList(page)
    side_panel = SidePanel(page)

    side_panel.search__input.fill(keyword)
    side_panel.search__button.click()

    # 검색 결과에 나타난 모든 상품에 키워드 포함 여부 확인
    product_titles_list = product_list.product_title__texts.all()
    if not product_titles_list:
        raise AssertionError(f"No products found for keyword: {keyword}")
    for element in product_titles_list:
        text_content = element.text_content().lower()
        assert keyword in text_content


def search_items(page: Page, test_data: Dict[str, str]):
    """
    제품 리스트 페이지에서 특정 키워드를 검색
    """
    go_to_product_url(page)
    search_keyword(page, test_data["keyword"])


def list_to_product_detail(page: Page, keyword: Dict[str, str]):
    """
    검색 결과에서 첫번째 item 상세 페이지 접근
    """
    product_list = ProductList(page)
    product_detail_page = ProductDetailPage(page)

    product_list.first_view_product__button.click()
    product_title_text = product_detail_page.product_title__text.text_content().lower()
    assert keyword["keyword"] in product_title_text


def confirmed_modal_to_cart(page: Page):
    """
    장바구니 확인 모달에서 장바구니로 이동
    """
    confirm_modal = ConfirmModal(page)

    confirm_modal.confirmed__modal.is_visible()
    confirm_modal.modal_product_added_title__text.is_visible()
    confirm_modal.view_cart__button.click()


def confirm_product_added_to_cart(
    page: Page, compared_title_text: str, quantity: Optional[str]
):
    """
    선택한 제품과 장바구니에 담긴 제품이 동일한 제품인지 체크
    """
    cart_page = CartPage(page)

    # 장바구니의 제품 제목과 수량 확인
    cart_page.product_title__text.is_visible()
    cart_product_title_text = cart_page.product_title__text.text_content()
    cart_product_quantity = cart_page.product_quantity__text.text_content()
    assert compared_title_text == cart_product_title_text
    if quantity is not None:
        assert quantity == cart_product_quantity


def check_signin_before_order(page: Page, email: str, password: str):
    """
    주문하기 전에 로그인 여부 체크해서 로그인
    """
    product_order = ProductOrder(page)
    menu = Menu(page)

    product_order.proceed_to_checkout__button.click()
    if not menu.logout_nav__button.is_visible():
        product_order.register_or_login__button.click()
        input_signin_data(page, email, password)
        menu.cart_nav__button.click()
        product_order.proceed_to_checkout__button.click()


def add_to_cart_with_info(page: Page, product_number: str) -> Dict[str, str]:
    """
    제품 번호를 통해 제품 이름과 가격 정보를 저장하고 해당 제품을 장바구니에 추가
    """
    confirm_modal = ConfirmModal(page)

    # 제품의 이름과 가격 가져와서 product_info 딕셔너리에 저장
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

    # 장바구니 추가
    product_add_cart_button = page.locator(
        f"(//a[@data-product-id='{product_number}'])[1]"
    )
    product_add_cart_button.click()
    confirm_modal.close_modal__button.click()

    return product_info


def get_info_from_cart(page: Page, product_number) -> Dict[str, str]:
    """
    제품의 이름과 가격 정보를 저장하여 리턴
    """
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
    """
    결제 카드 정보를 입력
    """
    product_order = ProductOrder(page)

    product_order.card_name__input.fill(card_name)
    product_order.card_number__input.fill(card_number)
    product_order.card_cvc__input.fill(card_cvc)
    product_order.card_expiry_month__input.fill(card_expiry_month)
    product_order.card_expiry_year__input.fill(card_expiry_year)


def calculate_total_price(page: Page) -> str:
    """
    각 제품에 대해 가격과 수량을 기반으로 총 금액을 구하고, 모든 총 금액을 더해 장바구니 전체 총액을 계산
    """
    # 장바구니에 있는 각 제품의 가격, 수량, 총 가격 정보를 가져옴
    price_elements = page.locator(".cart_price").all()
    quantity_elements = page.locator(".cart_quantity").all()
    total_price_elements = page.locator(".cart_total_price").all()

    # 각 제품의 가격, 수량을 곱하여 총 금액을 구하고, 모두 더하여 장바구니 전체 총액을 계산
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
    """
    주문 및 결제 완료 후 발급된 인보이스를 다운로드 받아 총 결제 금액 비교
    """
    product_order = ProductOrder(page)

    product_order.download_invoice__button.is_visible()
    product_order.download_invoice__button.click()

    # 인보이스 url에서 추출한 정보와 총 결제 금액이 일치하는지 확인
    filename = "invoice.txt"
    current_url = page.url
    invoice_num = current_url.split("/")[-1]
    formatted_invoice_num = "{:.1f}".format(float(invoice_num))
    invoice_url = os.path.join(
        Path.BASE_URL, "download_invoice", invoice_num
    )  # 인보이스 다운로드 URL 구성
    assert formatted_invoice_num == total_purchase_amount

    # 인보이스 다운로드 요청 전송
    response = requests.get(invoice_url)
    try:
        # 파일을 바이너리 쓰기 모드로 열어 다운로드한 내용을 저장
        with open(filename, "wb") as file:
            file.write(response.content)
        # 저장된 파일을 읽기 모드로 열어 내용 확인
        with open(filename, "r") as file:
            invoice_content = file.read()

        # 인보이스 내용이 예상된 형식과 일치하는지 확인
        assert (
            invoice_content
            == "Hi , Your total purchase amount is {}. Thank you".format(invoice_num)
        )
    finally:
        os.remove(filename)  # 다운로드 한 파일을 삭제. 다음 테스트에 새로운 파일을 다운받고 열기 위한 작업
