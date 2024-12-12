from playwright.sync_api import Page
from typing import Optional

from page_objects.locators.common_locators import Menu
from page_objects.locators.users_locators import SignUp, SignIn
from page_objects.path import Path


def go_to_main_url(page: Page):
    """
    메인 페이지로 이동
    """
    page.goto(Path.BASE_URL)


def go_to_signin_url(page: Page):
    """
    로그인 페이지로 이동
    """
    go_to_main_url(page)
    Menu(page).account_nav__button.click()


def input_signin_data(page: Page, email: str, password: str):
    """
    로그인할 사용자 정보를 입력하여 로그인
    """
    signin = SignIn(page)
    menu = Menu(page)

    signin.email__input.fill(email)
    signin.password__input.fill(password)
    signin.signin__button.click()
    menu.logout_nav__button.is_visible()


def input_account_data(
    page: Page,
    day: str,
    month: str,
    year: str,
    newsletter: Optional[bool],
    offer: Optional[bool],
    first_name: str,
    last_name: str,
    company: Optional[str],
    address_01: str,
    address_02: Optional[str],
    country: str,
    state: str,
    city: str,
    zipcode: str,
    mobile_number: str,
):
    """
    회원가입 시 필요한 정보 입력.
    선택 정보는 값이 존재하면 처리.
    """
    signup = SignUp(page)

    if day:
        signup.select_day__dropdown.click()
        signup.select_day__dropdown.select_option(value=[f"{day}"])
    if month:
        signup.select_month__dropdown.click()
        signup.select_month__dropdown.select_option(value=[f"{month}"])
    if year:
        signup.select_year__dropdown.click()
        signup.select_year__dropdown.select_option(value=[f"{year}"])

    if newsletter:
        signup.signup_newsletter__checkbox.check()
        signup.signup_newsletter__checkbox.is_checked()
    if offer:
        signup.receive_offer__checkbox.check()
        signup.receive_offer__checkbox.is_checked()

    signup.first_name__input.fill(first_name)
    signup.last_name__input.fill(last_name)
    if company:
        signup.company_name__input.fill(company)
    signup.address_01__input.fill(address_01)
    if address_02:
        signup.address_02__input.fill(address_02)
    signup.country__dropdown.click()
    signup.country__dropdown.select_option(value=[f"{country}"])
    signup.state__input.fill(state)
    signup.city__input.fill(city)
    signup.zipcode__input.fill(zipcode)
    signup.mobile_number__input.fill(mobile_number)
