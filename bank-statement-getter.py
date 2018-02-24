import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# get firefox driver and send to halifax login page
driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
driver.get('https://www.halifax-online.co.uk/personal/logon/login.jsp')

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

# get the memorable character indexes required for sign in 
mem_char_idx1 = driver.find_element_by_xpath('//*[@for="frmentermemorableinformation1:strEnterMemorableInformation_memInfo1"]').text
mem_char_idx2 = driver.find_element_by_xpath('//*[@for="frmentermemorableinformation1:strEnterMemorableInformation_memInfo2"]').text
mem_char_idx3 = driver.find_element_by_xpath('//*[@for="frmentermemorableinformation1:strEnterMemorableInformation_memInfo3"]').text

# input required characters from memorable info
mem_chars = [getpass.getpass(c + ' > ') for c in [mem_char_idx1, mem_char_idx2, mem_char_idx3]]

mem_char1 = driver.find_element_by_xpath('//*[@id="frmentermemorableinformation1:strEnterMemorableInformation_memInfo1"]')
mem_char2 = driver.find_element_by_xpath('//*[@id="frmentermemorableinformation1:strEnterMemorableInformation_memInfo2"]')
mem_char3 = driver.find_element_by_xpath('//*[@id="frmentermemorableinformation1:strEnterMemorableInformation_memInfo3"]')

mem_char1.send_keys(mem_chars[0])
mem_char2.send_keys(mem_chars[1])
mem_char3.send_keys(mem_chars[2])

continue_button = driver.find_element_by_xpath('//*[@id="frmentermemorableinformation1:btnContinue"]')
continue_button.click()

view_statement_button = driver.find_element_by_xpath('//*[@id="lnkAccFuncs_viewStatement_des-m-sat-xx-1"]')
view_statement_button.click()

statement_options_dropdown = driver.find_element_by_xpath('//*[@id="top-bar-exports"]')
statement_options_dropdown.click()

download_csv_button = driver.find_element_by_xpath('//*[@aria-label="Export transactions (CSV, QIF). option 2 of 3"]')
download_csv_button.click()

driver.find_element_by_xpath('//*[@id="labelexportDateRangeRadio-1"]').click()

date_from_box = driver.find_element_by_xpath('//*[@aria-label="Enter from date"]')
date_from_box.click()
date_from_box.send_keys('20/02/2018')

date_to_box = driver.find_element_by_xpath('//*[@aria-label="Enter to date"]')
date_to_box.click()
date_to_box.send_keys('22/02/2018')

#
driver.find_element_by_xpath('//*[@name="exportFormat"]').send_keys('Internet banking text/spreadsheet (.CSV)')

driver.find_element_by_xpath('//*[@id="exportStatementsButton"]').click()

driver.find_element_by_xpath('//*[@id="modal-close"]').click()

driver.find_element_by_xpath('//*[@id="ifCommercial:ifCustomerBar:ifMobLO:outputLinkLogOut"]').click()








