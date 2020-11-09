from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import getpass
import time
import datetime
from pathlib import Path

import bankstatementgetter.downloads as downloads 
import bankstatementgetter.cookies as cookies 



class BankStatementGetter():
    """Class to manage downloading bank statements."""

    def __init__(self, start_date, end_date, verbose = True):

        self.verbose = verbose
        self.download_dir = str(Path.home() / "Downloads")
        self.profile = self.set_profile()
        self.login_page = 'https://www.halifax-online.co.uk/personal/logon/login.jsp'
        self.webdriver_executable_path = '/usr/local/bin/geckodriver'
        self.start_date_range = start_date
        self.end_date_range = end_date
        
    def run(self):

        self.print_message(f'running for date range {self.start_date_range} - {self.end_date_range}')

        self.start_webdriver()
        self.add_cookies_to_browser()
        self.refresh_page()
        self.enter_login_details()

        # wait to get to next page - memorable information
        self.wait_for_xpath(
            xpath_str = '//*[@for="frmentermemorableinformation1:strEnterMemorableInformation_memInfo1"]',
            timeout_msg = 'memorable information'
        )

        self.enter_memorable_characters()
        self.sleep(2)
        self.enter_passcode()

        self.sleep(5)
        self.check_for_trust_this_device_popup()
        self.sleep(5)

        # wait to get to next page - accounts
        self.wait_for_xpath(
            xpath_str = '//*[@id="lnkAccFuncs_viewStatement_des-m-sat-xx-1"]',
            timeout_msg = 'accounts'
        )

        self.move_to_accounts()

        # wait to get to next page - statement
        self.wait_for_xpath(
            xpath_str = '//*[@id="top-bar-exports"]',
            timeout_msg = 'statement'
        )

        self.download_statement()
        self.sign_out()

        self.downloaded_file = self.get_downloaded_file()
        self.downloaded_file = self.rename_downloaded_file()

    def set_profile(self):
        """Set profile for webdriver to avoid download popup boxes for CSV files."""

        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.helperApps.neverAsk.openFile", "application/msexcel, text/csv application/csv")
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/msexcel, text/csv application/csv")
        profile.set_preference("browser.download.dir", self.download_dir)

        return profile

    def print_message(self, msg):
        """Print message if verbose attribute is True."""

        if self.verbose:
            print(datetime.datetime.now(), msg)       

    def sleep(self, s):
        """Sleep for s seconds."""

        self.print_message(f'sleeping for {s}s')

        time.sleep(s)

    def start_webdriver(self):
        """Start firefox driver and send to login page."""

        self.print_message('starting webdriver')

        driver = webdriver.Firefox(executable_path = self.webdriver_executable_path, firefox_profile = self.profile)
        driver.get(self.login_page)

        self.driver = driver

    def add_cookies_to_browser(self):
        """Add cookies to selenium session.
        
        Seems to prevent looping back to first login screen after entering memorable info characters.
        """

        self.print_message('adding cookies to browser')

        cookies.load_and_add_cookies(self.driver, 'cookies/cookies.json', '.halifax-online.co.uk')

    def refresh_page(self):
        """Refresh webpage."""

        self.print_message('refreshing page')

        self.driver.refresh()

    def enter_login_details(self):
        """Enter username and password on login page and submit."""
    
        self.print_message('accepting login details')

        username = getpass.getpass('username > ')
        pwd = getpass.getpass('password > ')

        # get username and password boxes
        username_box = self.driver.find_element_by_xpath('//*[@id="frmLogin:strCustomerLogin_userID"]')
        password_box = self.driver.find_element_by_xpath('//*[@id="frmLogin:strCustomerLogin_pwd"]')

        # input login details and submit
        username_box.send_keys(username)
        password_box.send_keys(pwd)
        password_box.submit()
        
    def wait_for_xpath(self, xpath_str, timeout_msg, timeout = 5):
        """Method to wait for xpath to be available on page.
        
        Args:
            xpath_str (str): xpath string to look for.
            timeout (int): number of seconds to wait for page to load. Default value is 5.
            timeout_msg (str): timeoutException message is display if xpath is not found within timeout seconds.

        Returns:
            None.

        """
        
        self.print_message(f'wating for {timeout}s for {timeout_msg} (xpath: {xpath_str})')

        timeout_msg = f'timeout waiting for {timeout_msg} - after {timeout}s, xpath: {xpath_str}'

        try:
            
            element_present = expected_conditions.presence_of_element_located((By.XPATH, xpath_str))
            
            WebDriverWait(self.driver, timeout).until(element_present)
            
        except TimeoutException as err:
            
            raise TimeoutError(timeout_msg) from err

    def enter_memorable_characters(self):
        """Input memorable characters and proceed to next page."""

        self.print_message('accepting memorable information')

        # loop through 3 memorbale characters
        for i in range(1, 4):
            
            # get text identifying which character is required
            character_index = self.driver.find_element_by_xpath(
                f'//*[@for="frmentermemorableinformation1:strEnterMemorableInformation_memInfo{i}"]'
            ).text.rstrip()

            # input character
            character = getpass.getpass(character_index + ' > ')

            # get drop down box 
            drop_down = self.driver.find_element_by_xpath(f'//*[@id="frmentermemorableinformation1:strEnterMemorableInformation_memInfo{i}"]')

            # input the required character into drop down box
            drop_down.send_keys(character)

        # click on continue after memorable info characters have been input to log in
        self.driver.find_element_by_xpath('//*[@id="frmentermemorableinformation1:btnContinue"]').click()

    def enter_passcode(self):
        """Enter passcode sent by text message."""

        self.print_message('accepting passcode')

        page_title_elements = self.driver.find_elements_by_class_name("page-title")

        # if we are being asked to verify with a passcode text
        if len(page_title_elements) == 1 and page_title_elements[0].text == 'VERIFY YOURSELF WITH A PASSCODE.':
            
            # click on continue button to send text
            self.driver.find_elements_by_class_name("base-button")[1].click()

            # accept passcode
            passcode = getpass.getpass('passcode > ')

            # populate passcode box
            self.driver.find_elements_by_class_name("base-input")[0].send_keys(passcode)

            # click on continue button
            self.driver.find_elements_by_class_name("base-button")[0].click()

    def check_for_trust_this_device_popup(self):
        """Check if the trust this device pop up? has come up."""

        self.print_message('checking for trust this device pop up')

        trust_this_device_popup = self.driver.find_elements_by_class_name("sca-over-text-retaila")

        if len(trust_this_device_popup) > 0:

            self.driver.find_elements_by_id("scayesspan")[0].click()
            self.driver.find_elements_by_id("dcontinue")[0].click()
            self.driver.find_elements_by_id("dclose")[0].click()

    def move_to_accounts(self):
        """Click on the view statement button for the first account"""

        self.print_message('moving to accounts page')

        self.driver.find_element_by_xpath('//*[@id="lnkAccFuncs_viewStatement_des-m-sat-xx-1"]').click()

    def download_statement(self):
        """Choose to download CSV, enter date range and download."""

        self.print_message('downloading statement')

        # click on the dropdown to export statements
        self.driver.find_element_by_xpath('//*[@id="top-bar-exports"]').click()

        # click on the option to export to csv
        self.driver.find_element_by_xpath('//*[@aria-label="Export transactions (CSV, QIF). option 3 of 4"]').click()
        
        # click on export date range
        self.driver.find_element_by_xpath('//*[@id="labelexportDateRangeRadio-1"]').click()

        # input export from date
        date_from_box = self.driver.find_element_by_xpath('//*[@aria-label="Enter from date"]')
        date_from_box.click()
        date_from_box.send_keys(self.start_date_range)

        # input export to date
        date_to_box = self.driver.find_element_by_xpath('//*[@aria-label="Enter to date"]')
        date_to_box.click()
        date_to_box.send_keys(self.end_date_range)

        # wait to get export button
        self.wait_for_xpath(
            xpath_str = '//*[@name="exportFormat"]', 
            timeout_msg = 'export button'
        )
        
        self.sleep(1)
        
        # select csv export option from drop down
        export_format_dropdown = self.driver.find_element_by_xpath('//*[@name="exportFormat"]')
        export_format_dropdown.click()
        export_format_dropdown.send_keys('Internet banking text/spreadsheet (.CSV)')

        self.sleep(1)
        
        # click the export button
        self.driver.find_element_by_xpath('//*[@id="exportStatementsButton"]').click()

        self.sleep(5)

        # close the export window
        self.driver.find_element_by_xpath('//*[@id="modal-close"]').click()

    def sign_out(self):
        """Click log out button."""

        self.print_message('signing out')

        self.driver.find_element_by_xpath('//*[@id="ifCommercial:ifCustomerBar:ifMobLO:outputLinkLogOut"]').click()

    def get_downloaded_file(self):
        """Get the latest file in the downloads folder."""

        self.print_message('getting downloaded file')

        return downloads.get_latest_download(self.download_dir)

    def rename_downloaded_file(self):
        """Rename the downloaded file."""

        self.print_message('renaming downloaded file')

        return downloads.rename_download_file(self.downloaded_file, self.start_date_range, self.end_date_range)


