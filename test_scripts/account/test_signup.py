import secrets
import string

import pytest
from playwright.sync_api import Page

from test_scripts.account.conftest import input_account_data, go_to_signin_url
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
def test_signup_account(page: Page, test_data: dict):
    """
    시나리오: 사용자가 신규로 회원가입한다.
    1. Signup/Login 페이지로 이동한다.
    2. Name과 Email을 입력하여 회원가입 페이지로 이동한다.
    3. 계정 정보와 주소 정보를 입력하여 회원가입한다.
    """
    signin = SignIn(page)
    signup = SignUp(page)

    go_to_signin_url(page)
    generated = "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for i in range(5)
    )
    generated_password = "".join(
        secrets.choice(string.ascii_uppercase + string.digits) for i in range(7)
    )
    new_name = generated
    new_email = generated + "@test.com"
    signin.new_name__input.fill(new_name)
    signin.new_email__input.fill(new_email)
    signin.signup__button.click()

    signup.signup__title.is_visible()
    assert signup.name__input.input_value() == new_name
    assert signup.email__input.input_value() == new_email
    signup.email__input.is_disabled()
    signup.password__input.fill(generated_password)

    input_account_data(
        page,
        day=test_data["day"],
        month=test_data["month"],
        year=test_data["year"],
        newsletter=test_data["newsletter"],
        offer=False,
        company=None,
        first_name=test_data["first_name"],
        last_name=test_data["last_name"],
        address_01=test_data["address_01"],
        address_02=None,
        country=test_data["country"],
        state=test_data["state"],
        city=test_data["city"],
        zipcode=test_data["zipcode"],
        mobile_number=test_data["mobile_number"],
    )
    signup.create_account__button.click()
    signup.account_created__text.is_visible()


# TODO: 더 다양한 조합으로 회원 정보를 입력하여 회원 가입하는 시나리오 추가.
