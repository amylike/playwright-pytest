from playwright.sync_api import Page


class SignIn:
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator("[data-qa='login-email']")
        self.password_input = page.locator("[data-qa='login-password']")
        self.signin_button = page.locator("[data-qa='login-button']")
        self.warning_text = page.locator("//p[@style='color: red;']")
        self.new_name_input = page.locator("[data-qa='signup-name']")
        self.new_email_input = page.locator("[data-qa='signup-email']")
        self.signup_button = page.locator("[data-qa='signup-button']")


class SignUp:
    def __init__(self, page: Page):
        self.page = page
        self.name_input = page.locator("[data-qa='name']")
        self.email_input = page.locator("[data-qa='email']")

        self.signup_title = page.locator("//b[text()='Enter Account Information']")
        self.password_input = page.locator("[data-qa='password']")
        self.signup_button = page.locator("[data-qa='signup-button']")
        self.select_day_dropdown = page.locator("[data-qa='days']")
        # self.select_day_input = pag
        self.select_month_dropdown = page.locator("[data-qa='months']")
        self.select_year_dropdown = page.locator("[data-qa='years']")
        self.signup_newsletter_checkbox = page.locator("[id='newsletter']")
        self.receive_offer_checkbox = page.locator("[id='optin']")

        self.first_name_input = page.locator("[data-qa='first_name']")
        self.last_name_input = page.locator("[data-qa='last_name']")
        self.company_name_input = page.locator("[data-qa='company']")
        self.address_01_input = page.locator("[data-qa='address']")
        self.address_02_input = page.locator("[data-qa='address2']")
        self.country_dropdown = page.locator("[data-qa='country']")
        self.country_input = page.locator("//option[text()='{}']")
        self.state_input = page.locator("[data-qa='state']")
        self.city_input = page.locator("[data-qa='city']")
        self.zipcode_input = page.locator("[data-qa='zipcode']")
        self.mobile_number_input = page.locator("[data-qa='mobile_number']")
        self.create_account_button = page.locator("[data-qa='create-account']")

        self.account_created_text = page.locator("[data-qa='account-created']")
        self.continue_button = page.locator("[data-qa='continue-button']")
