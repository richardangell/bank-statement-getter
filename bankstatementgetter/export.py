import downloads # from bank-statement-getter
import getpass
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By




def wait_for_xpath(driver, xpath_str, timeout = 5, timeout_msg = 'Timed out waiting for page to load'):
    """
    Export bank statements from Halifax.
    
    Args:
        driver (webdriver.firefox.webdriver.WebDriver): selenium firefox web driver
        xpath_str (str): xpath string to look for.
        timeout (int): number of seconds to wait for page to load. Default value is 5.
        timeout_msg (str): timeoutException message is display if xpath is not found within timeout seconds.

    Returns:
        None.
    """
    
    if not isinstance(driver, webdriver.firefox.webdriver.WebDriver):
        
        raise TypeError('driver should be a selenium firefox driver')
    
    try:
        
        element_present = EC.presence_of_element_located((By.XPATH, xpath_str))
        
        WebDriverWait(driver, timeout).until(element_present)
        
    except TimeoutException:
        
        print(timeout_msg)
    
    


def export_halifax_statements(timeout = 5, download_timeout = 10):
    """
    Export bank statements from Halifax.
    
    Args:
        timeout (int): number of seconds to wait for pages to load.
        download_timeout (int): number of seconds to wait for statements to download.

    Returns:
        str: The filename and path of the exported statements.
    """

    # get firefox driver and send to halifax login page
    driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
    driver.get('https://www.halifax-online.co.uk/personal/logon/login.jsp')

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.helperApps.neverAsk.openFile", "application/msexcel, text/csv")
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/msexcel, text/csv")
    
    # get username and password
    hali_user = getpass.getpass('username > ')
    hali_pass = getpass.getpass('password > ')

    # get username and password boxes
    username_box = driver.find_element_by_xpath('//*[@id="frmLogin:strCustomerLogin_userID"]')
    password_box = driver.find_element_by_xpath('//*[@id="frmLogin:strCustomerLogin_pwd"]')

    # input username and password and submit
    username_box.send_keys(hali_user)
    password_box.send_keys(hali_pass)
    password_box.submit()

    # check if details were invalid id="useridInvalidError" 
    
    # wait to get to next page (memorable information)
    wait_for_xpath(driver,
                   xpath_str = '//*[@for="frmentermemorableinformation1:strEnterMemorableInformation_memInfo1"]', 
                   timeout_msg = 'Timed out waiting for memorable info page to load')
    
    # get the memorable character indexes required for sign in 
    mem_char_idx1 = driver.find_element_by_xpath('//*[@for="frmentermemorableinformation1:strEnterMemorableInformation_memInfo1"]').text.rstrip()
    mem_char_idx2 = driver.find_element_by_xpath('//*[@for="frmentermemorableinformation1:strEnterMemorableInformation_memInfo2"]').text.rstrip()
    mem_char_idx3 = driver.find_element_by_xpath('//*[@for="frmentermemorableinformation1:strEnterMemorableInformation_memInfo3"]').text.rstrip()

    # input required characters from memorable info
    mem_chars = [getpass.getpass(c + ' > ') for c in [mem_char_idx1, mem_char_idx2, mem_char_idx3]]

    # get the selection drop downs for memorable info characters
    mem_char1 = driver.find_element_by_xpath('//*[@id="frmentermemorableinformation1:strEnterMemorableInformation_memInfo1"]')
    mem_char2 = driver.find_element_by_xpath('//*[@id="frmentermemorableinformation1:strEnterMemorableInformation_memInfo2"]')
    mem_char3 = driver.find_element_by_xpath('//*[@id="frmentermemorableinformation1:strEnterMemorableInformation_memInfo3"]')

    # input the required characters
    mem_char1.send_keys(mem_chars[0])
    mem_char2.send_keys(mem_chars[1])
    mem_char3.send_keys(mem_chars[2])

    # click on continue after memorable info characters have been input to log in
    driver.find_element_by_xpath('//*[@id="frmentermemorableinformation1:btnContinue"]').click()
    
    # check login successful
    
    # wait to get to next page (accounts)
    wait_for_xpath(driver,
                   xpath_str = '//*[@id="lnkAccFuncs_viewStatement_des-m-sat-xx-1"]', 
                   timeout_msg = 'Timed out waiting for accounts page to load')
    
    # click on the view statement button for the first account
    driver.find_element_by_xpath('//*[@id="lnkAccFuncs_viewStatement_des-m-sat-xx-1"]').click()

    # wait to get to next page (statement)
    wait_for_xpath(driver,
                   xpath_str = '//*[@id="top-bar-exports"]', 
                   timeout_msg = 'Timed out waiting for accounts page to load')
    
    # click on the dropdown to export statements
    driver.find_element_by_xpath('//*[@id="top-bar-exports"]').click()

    # click on the option to export to csv
    driver.find_element_by_xpath('//*[@aria-label="Export transactions (CSV, QIF). option 2 of 3"]').click()
    
    # click on export date range
    driver.find_element_by_xpath('//*[@id="labelexportDateRangeRadio-1"]').click()

    # input export from date
    date_from_box = driver.find_element_by_xpath('//*[@aria-label="Enter from date"]')
    date_from_box.click()
    date_from_box.send_keys('20/02/2018')

    # input export to date
    date_to_box = driver.find_element_by_xpath('//*[@aria-label="Enter to date"]')
    date_to_box.click()
    date_to_box.send_keys('22/02/2018')

    # wait to get export button
    wait_for_xpath(driver,
                   xpath_str = '//*[@name="exportFormat"]', 
                   timeout_msg = 'Timed out waiting for export button')
    
    time.sleep(1)
    
    # select csv export option from drop down
    export_format_dropdown = driver.find_element_by_xpath('//*[@name="exportFormat"]')
    export_format_dropdown.click()
    export_format_dropdown.send_keys('Internet banking text/spreadsheet (.CSV)')

    time.sleep(1)
    
    # get the files in the download folder
    current_downloads = downloads.get_downloads()
    
    # click the export button
    driver.find_element_by_xpath('//*[@id="exportStatementsButton"]').click()

    # get the downloaded file
    downloaded_statement_file = downloads.get_new_download(current_downloads)
    
    # close the export window
    driver.find_element_by_xpath('//*[@id="modal-close"]').click()

    # log out of halifax
    driver.find_element_by_xpath('//*[@id="ifCommercial:ifCustomerBar:ifMobLO:outputLinkLogOut"]').click()

    return(downloaded_statement_file)
    





