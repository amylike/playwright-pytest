from playwright.sync_api import Page


class SignIn:
    def __init__(self, page: Page):
        self.page = page
        self.email__input = page.locator("[data-qa='login-email']")
        self.password__input = page.locator("[data-qa='login-password']")
        self.signin__button = page.locator("[data-qa='login-button']")
        self.warning__text = page.locator("//p[@style='color: red;']")
        self.new_name__input = page.locator("[data-qa='signup-name']")
        self.new_email__input = page.locator("[data-qa='signup-email']")
        self.signup__button = page.locator("[data-qa='signup-button']")


class SignUp:
    def __init__(self, page: Page):
        self.page = page
        self.name__input = page.locator("[data-qa='name']")
        self.email__input = page.locator("[data-qa='email']")

        self.signup__title = page.locator("//b[text()='Enter Account Information']")
        self.password__input = page.locator("[data-qa='password']")
        self.signup__button = page.locator("[data-qa='signup-button']")
        self.select_day__dropdown = page.locator("[data-qa='days']")
        self.select_month__dropdown = page.locator("[data-qa='months']")
        self.select_year__dropdown = page.locator("[data-qa='years']")
        self.signup_newsletter__checkbox = page.locator("[id='newsletter']")
        self.receive_offer__checkbox = page.locator("[id='optin']")

        self.first_name__input = page.locator("[data-qa='first_name']")
        self.last_name__input = page.locator("[data-qa='last_name']")
        self.company_name__input = page.locator("[data-qa='company']")
        self.address_01__input = page.locator("[data-qa='address']")
        self.address_02__input = page.locator("[data-qa='address2']")
        self.country__dropdown = page.locator("[data-qa='country']")
        self.country__input = page.locator("//option[text()='{}']")
        self.state__input = page.locator("[data-qa='state']")
        self.city__input = page.locator("[data-qa='city']")
        self.zipcode__input = page.locator("[data-qa='zipcode']")
        self.mobile_number__input = page.locator("[data-qa='mobile_number']")
        self.create_account__button = page.locator("[data-qa='create-account']")

        self.account_created__text = page.locator("[data-qa='account-created']")
        self.continue__button = page.locator("[data-qa='continue-button']")
