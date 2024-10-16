import pytest
from playwright.sync_api import Page

from page_objects.locators.products_locators import SidePanel, ProductList
from test_script.product.conftest import go_to_product_url, search_items

TEST_DATA = [{"keyword": "blue", "category": "Men", "sub_category": "Jeans"}]


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_search_product(page: Page, test_data: dict):
    """
    시나리오: 사용자가 제품을 검색한다.
    1. Products 페이지로 이동한다.
    2. 검색창에 키워드를 입력한다.
    3. 검색 결과에 검색창에 입력한 제품명이 포함되어 있는지 확인한다.
    """
    search_items(page, test_data)


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_confirm_category(page: Page, test_data: dict):
    """
    시나리오: 사용자가 특정 카테고리에서 제품을 살펴본다.
    1. Category에서 특정 제품군을 선택한다.
    2. 해당 카테고리에 해당하는 제품들로만 구성되어 있는지 확인한다.
    """
    go_to_product_url(page)
    SidePanel(page).men_category_button.is_visible()
    SidePanel(page).men_category_button.click()
    SidePanel(page).jeans_sub_category_button.is_visible()
    SidePanel(page).jeans_sub_category_button.click()

    title_text = ProductList(page).category_title_text.text_content()
    assert (
        title_text == f'{test_data["category"]} - {test_data["sub_category"]} Products'
    )

    product_titles = ProductList(page).product_title_texts.all()
    for element in product_titles:
        text_content = element.text_content()
        assert test_data["sub_category"] in text_content

    # TODO: 필요하다면 카테고리 선택하는 함수와 일치 여부를 확인하는 함수를 conftest에 선언하여 재사용


# TODO: 더 많은 카테고리나 브랜드 sorting을 적용하여 제품을 검색하는 시나리오 추가
