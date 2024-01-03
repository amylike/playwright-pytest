import secrets
import string

import pytest
from playwright.sync_api import Page

from test_script.account.conftest import input_account_data, go_to_signin_url
from page_objects.locators.users_locators import SignIn, SignUp


TEST_DATA = [
    {
        "day": "25",
        "month": "April",
        "year": "1994",
        "newsletter": True,
        "first_name": "Amy",
        "last_name": "Kim",
        "address_01": "Alphabet 101",
        "country": "Canada",
        "state": "Alpa",
        "city": "Beta",
        "zipcode": "12345",
        "mobile_number": "821011111111",
    },
]


@pytest.mark.parametrize("test_data", TEST_DATA)
def test_signup_account(page: Page, test_data):
    """
    시나리오: 사용자가 신규로 회원가입한다.
    1. Signup/login 페이지로 이동한다.
    2. Name과 Email을 입력하여 회원가입 페이지로 이동한다.
    3. 계정 정보와 주소 정보를 입력하여 회원가입한다.
    """
    go_to_signin_url(page)
    generated = "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for i in range(5)
    )
    generated_password = "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for i in range(7)
    )
    new_name = generated
    new_email = generated + "@test.com"
    SignIn(page).new_name_input.fill(new_name)
    SignIn(page).new_email_input.fill(new_email)
    SignIn(page).signup_button.click()

    SignUp(page).signup_title.is_visible()
    assert SignUp(page).name_input.input_value() == new_name
    assert SignUp(page).email_input.input_value() == new_email
    SignUp(page).email_input.is_disabled()
    SignUp(page).password_input.fill(generated_password)
    # TODO:로그인 페이지에서 name, email 입력하고 회원가입 페이지에서 해당 정보가 나타는지를 체크하는 것도 분리할지 결정

    input_account_data(
        page,
        day=test_data["day"],
        month=test_data["month"],
        year=test_data["year"],
        newsletter=test_data["newsletter"],
        first_name=test_data["first_name"],
        last_name=test_data["last_name"],
        address_01=test_data["address_01"],
        country=test_data["country"],
        state=test_data["state"],
        city=test_data["city"],
        zipcode=test_data["zipcode"],
        mobile_number=test_data["mobile_number"],
    )
    SignUp(page).create_account_button.click()
    SignUp(page).account_created_text.is_visible()
