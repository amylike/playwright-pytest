import secrets
import string
import pytest
from playwright.sync_api import Page

from test_script.account.conftest import input_signin_data, go_to_signin_url
from page_objects.locators.common_locators import Menu
from page_objects.locators.users_locators import SignIn


TEST_DATA = [
    {"email": "asdf1234@gmail.com", "password": "google1234"},
]


def test_signin_incorrect(page: Page):
    """
    시나리오: 사용자가 잘못된 정보로 로그인 시도한다.
    1. Signin 페이지로 이동한다.
    2. 이메일과 패스워드에 잘못된 정보를 입력한다.
    3. 로그인에 실패했다는 메세지를 받는다.
    """
    go_to_signin_url(page)

    generated = "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for i in range(7)
    )
    wrong_email = generated + "@test.com"
    wrong_password = generated
    SignIn(page).email_input.fill(wrong_email)
    SignIn(page).password_input.fill(wrong_password)
    SignIn(page).signin_button.click()

    assert (
        SignIn(page).warning_text.text_content()
        == "Your email or password is incorrect!"
    )


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_signin_correct(page: Page, test_data):
    """
    시나리오: 사용자가 정상적인 정보로 로그인한다.
    1. Signup/login 페이지로 이동한다.
    2. 이메일과 패스워드에 올바른 정보를 입력한다.
    3. 로그인에 성공하여, 메뉴바에 로그아웃 버튼이 나타난다.
    """
    go_to_signin_url(page)
    input_signin_data(page, email=test_data["email"], password=test_data["password"])
    SignIn(page).signin_button.click()
    Menu(page).logout_nav_button.is_visible()


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_signout(page: Page, test_data):
    """
    시나리오: 사용자가 로그아웃한다.
    1. 사용자가 로그인한다.
    2. 사용자가 로그아웃에 성공하여, 메뉴바에서 로그인 버튼이 나타난다.
    """
    test_signin_correct(page, test_data)
    Menu(page).logout_nav_button.click()
    Menu(page).account_nav_button.is_visible()
