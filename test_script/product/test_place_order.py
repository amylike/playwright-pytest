import pytest
from playwright.sync_api import Page

from page_objects.locators.common_locators import Menu
from page_objects.locators.products_locators import (
    ProductOrder,
)
from test_script.product.conftest import (
    download_invoice,
    add_to_cart_with_info,
    get_info_from_cart,
    input_card_data,
    check_signin_before_order,
    calculate_total_price,
    search_items,
)

TEST_DATA = [
    {
        "keyword": "blue",
        "email": "asdf1234@gmail.com",
        "password": "google1234",
        "product_numbers": ["21", "43"],
        "message": "ASAP",
        "card_name": "Amy Kim",
        "card_number": "1234432112344321",
        "card_cvc": "987",
        "card_expiry_month": "12",
        "card_expiry_year": "2025",
    },
]


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_place_order(page: Page, test_data: dict):
    """
    시나리오: 사용자가 장바구니에서 제품을 주문한다.
    1. 특정 키워드를 검색하여 제품을 장바구니에 추가한다.
    2. 장바구니로 이동하여 로그인 후 주문 페이지로 이동한다.
    3. 카드정보 입력 후 결제 및 주문 완료한다.
    4. 인보이스를 다운로드하여 결제 금액과 비교한다.
    """
    # 특정 키워드를 검색하여 제품을 장바구니에 추가
    search_items(page, test_data)
    product_info_list = []
    for product_number in test_data["product_numbers"]:
        product_info_list.append(add_to_cart_with_info(page, product_number))

    # 장바구니로 이동하여 제품 정보 확인
    Menu(page).cart_nav_button.click()
    cart_product_info_list = []
    for product_number in test_data["product_numbers"]:
        cart_product_info_list.append(get_info_from_cart(page, product_number))

    assert product_info_list == cart_product_info_list

    total_purchase_amount = calculate_total_price(page)

    # 로그인 후 주문 페이지로 이동
    check_signin_before_order(page, test_data["email"], test_data["password"])

    ProductOrder(page).order_message_input.fill(test_data["message"])
    ProductOrder(page).place_order_button.click()

    # 카드 정보 입력하여 결제
    input_card_data(
        page,
        card_name=test_data["card_name"],
        card_number=test_data["card_number"],
        card_cvc=test_data["card_cvc"],
        card_expiry_month=test_data["card_expiry_month"],
        card_expiry_year=test_data["card_expiry_year"],
    )
    ProductOrder(page).complete_payment_button.click()
    assert ProductOrder(page).confirm_order_text.text_content() == "Order Placed!"

    download_invoice(page, total_purchase_amount)
