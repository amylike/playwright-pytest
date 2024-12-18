import pytest
from playwright.sync_api import Page

from page_objects.locators.products_locators import (
    ProductList,
    ProductDetailPage,
    CartPage,
)
from test_scripts.product.conftest import (
    list_to_product_detail,
    confirm_product_added_to_cart,
    confirmed_modal_to_cart,
    search_items,
)


TEST_DATA = [
    {"keyword": "blue", "quantity": "15"},
]


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_add_to_cart_from_detail_page(page: Page, test_data: dict):
    """
    시나리오: 사용자가 제품 상세 페이지에서 제품을 장바구니에 담는다.
    1. 특정 Product 상세 페이지로 이동한다.
    2. 해당 제품을 장바구니에 추가한다.
    3. 장바구니로 이동하여 제품이 담겼는지 확인한다.
    """
    product_detail_page = ProductDetailPage(page)

    search_items(page, test_data)
    list_to_product_detail(page, test_data)
    details_title_text = product_detail_page.product_title__text.text_content()
    product_detail_page.add_to_cart__button.click()

    confirmed_modal_to_cart(page)
    confirm_product_added_to_cart(page, details_title_text, None)


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_add_to_cart_from_list(page: Page, test_data: dict):
    """
    시나리오: 사용자가 리스트에서 제품을 장바구니에 담는다.
    1. Product 리스트에서 특정 제품을 장바구니에 담는다.
    2. 장바구니로 이동하여 제품이 담겼는지 확인한다.
    """
    product_list = ProductList(page)

    search_items(page, test_data)
    list_title_text = product_list.random_product_title__text.text_content()
    product_list.random_add_to_cart__button.click()

    confirmed_modal_to_cart(page)
    confirm_product_added_to_cart(page, list_title_text, None)


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_remove_product_from_cart(page: Page, test_data: dict):
    """
    시나리오: 사용자가 장바구니에 담은 제품을 장바구니에서 제거한다.
    1. 특정 제품을 장바구니에 추가한다.
    2. 장바구니에서 해당 제품을 제거한다.
    3. 제품이 제거된 것을 확인한다.
    """
    cart_page = CartPage(page)

    test_add_to_cart_from_detail_page(page, test_data)
    cart_page.remove_item__button.is_visible()
    cart_page.remove_item__button.click()
    cart_page.empty_cart_message__text.is_visible()
    cart_page.remove_item__button.is_hidden()


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_add_to_cart_multiple(page: Page, test_data: dict):
    """
    시나리오: 사용자가 하나의 제품을 여러개 장바구니에 담는다.
    1. 특정 Product 상세 페이지로 이동한다.
    2. 해당 제품을 여러개 장바구니에 추가한다.
    3. 장바구니로 이동하여 제품이 입력한 갯수대로 담겼는지 확인한다.
    """
    product_detail_page = ProductDetailPage(page)

    search_items(page, test_data)
    list_to_product_detail(page, test_data)
    details_title_text = product_detail_page.product_title__text.text_content()
    product_detail_page.product_quantity__input.fill(test_data["quantity"])

    product_detail_page.add_to_cart__button.click()

    confirmed_modal_to_cart(page)
    confirm_product_added_to_cart(page, details_title_text, test_data["quantity"])


# TODO: 장바구니에 동일 제품 수량 여러개 담고 수량 및 가격 확인하는 시나리오 추가
