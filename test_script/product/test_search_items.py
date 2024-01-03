import pytest
from playwright.sync_api import Page

from test_script.product.conftest import go_to_product_url, search_keyword

TEST_DATA = [
    {"keyword": "blue"},
]


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_search_items(page: Page, test_data):
    """
    시나리오: 사용자가 제품을 검색한다.
    1. Products 페이지로 이동한다.
    2. 검색창에 키워드를 입력한다.
    3. 검색 결과에 검색창에 입력한 제품명이 포함되어 있는지 확인한다.
    """
    go_to_product_url(page)
    search_keyword(page, test_data["keyword"])


# TODO: 더 많은 검색 필터나 sorting 방식 적용.
