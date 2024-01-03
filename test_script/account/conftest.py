from playwright.sync_api import Page

from page_objects.locators.common_locators import Menu
from page_objects.locators.users_locators import SignUp, SignIn
from page_objects.path import Path


def go_to_main_url(page):
    # 메인 페이지로 이동
    page.goto(Path.BASE_URL)


def go_to_signin_url(page):
    go_to_main_url(page)
    Menu(page).account_nav_button.click()


def input_signin_data(page: Page, email=None, password=None):
    SignIn(page).email_input.fill(email)
    SignIn(page).password_input.fill(password)
    SignIn(page).signin_button.click()
    Menu(page).logout_nav_button.is_visible()


def input_account_data(
    page: Page,
    day=None,
    month=None,
    year=None,
    newsletter=None,
    offer=None,
    first_name=None,
    last_name=None,
    company=None,
    address_01=None,
    address_02=None,
    country=None,
    state=None,
    city=None,
    zipcode=None,
    mobile_number=None,
):
    if day:
        SignUp(page).select_day_dropdown.click()
        SignUp(page).select_day_dropdown.select_option(value=[f"{day}"])
    if month:
        SignUp(page).select_month_dropdown.click()
        SignUp(page).select_month_dropdown.select_option(value=[f"{month}"])
    if year:
        SignUp(page).select_year_dropdown.click()
        SignUp(page).select_year_dropdown.select_option(value=[f"{year}"])

    if newsletter:
        SignUp(page).signup_newsletter_checkbox.check()
        SignUp(page).signup_newsletter_checkbox.is_checked()
    if offer:
        SignUp(page).receive_offer_checkbox.check()
        SignUp(page).receive_offer_checkbox.is_checked()

    SignUp(page).first_name_input.fill(first_name)
    SignUp(page).last_name_input.fill(last_name)
    if company:
        SignUp(page).company_name_input.fill(company)
    SignUp(page).address_01_input.fill(address_01)
    if address_02:
        SignUp(page).address_02_input.fill(address_02)
    SignUp(page).country_dropdown.click()
    SignUp(page).country_dropdown.select_option(value=[f"{country}"])
    SignUp(page).state_input.fill(state)
    SignUp(page).city_input.fill(city)
    SignUp(page).zipcode_input.fill(zipcode)
    SignUp(page).mobile_number_input.fill(mobile_number)
