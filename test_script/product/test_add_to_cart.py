import pytest
from playwright.sync_api import Page

from page_objects.locators.products_locators import (
    ProductPage,
    ProductDetail,
    ConfirmModal,
)
from test_script.product.conftest import list_to_product_detail
from test_script.product.test_search_items import test_search_items

TEST_DATA = [
    {"keyword": "blue"},
]


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_detail_add_to_cart(page: Page, test_data):
    """
    시나리오: 사용자가 제품을 장바구니에 담는다.
    1. 특정 Product 상세 페이지로 이동한다.
    2. 해당 제품을 장바구니에 추가한다.
    """
    test_search_items(page, test_data)
    list_to_product_detail(page, test_data)

    ProductDetail(page).add_to_cart_button.click()
    ConfirmModal(page).confirmed_modal.is_visible()
    ConfirmModal(page).modal_added_title.is_visible()
    ConfirmModal(page).close_modal_button.click()
    ConfirmModal(page).confirmed_modal.is_hidden()

    page.wait_for_timeout(2000)


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_list_add_to_cart(page, test_data):
    """
    시나리오: 사용자가 제품을 장바구니에 담는다.
    1. Product 리스트에서 특정 제품을 장바구니에 담는다.
    2. 장바구니로 이동하여 제품이 담겼는지 확인한다.
    """
    test_search_items(page, test_data)

    ProductPage(page).add_to_cart_button.click()
    ConfirmModal(page).confirmed_modal.is_visible()
    ConfirmModal(page).modal_added_title.is_visible()
    ConfirmModal(page).close_modal_button.click()
    ConfirmModal(page).confirmed_modal.is_hidden()

    page.wait_for_timeout(2000)


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_confirm_cart(page, test_data):
    """
    시나리오: 사용자가 제품을 장바구니에 담고 장바구니를 확인한다.
    1. 특정 Product 상세 페이지로 이동한다.
    2. 해당 제품을 장바구니에 추가한다.
    3. 장바구니로 이동하여 제품이 담겼는지 확인한다.
    """
    test_search_items(page, test_data)

    ProductPage(page).add_to_cart_button.click()
    ConfirmModal(page).confirmed_modal.is_visible()
    ConfirmModal(page).modal_added_title.is_visible()
    ConfirmModal(page).view_cart_button.click()

    page.wait_for_timeout(2000)


# TODO: 장바구니에 동일 제품 수량 여러개 담고 수량 및 가격 확인하는 시나리오
