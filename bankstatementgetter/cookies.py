import json


def save_cookie(driver, path):
    """Function to save cookies from webdriver to json file."""

    with open(path, 'w') as filehandler:

        json.dump(driver.get_cookies(), filehandler)


def load_cookies(path):
    """Function to load cookies saved in json file."""

    with open(path, 'r') as cookiesfile:

        cookies = json.load(cookiesfile)

    return cookies


def add_cookies_to_driver(driver, cookies, domain):
    """Function to add cookies for the given domain to a selenium webdriver."""

    for cookie in cookies:
        
        if cookie['domain'] == domain:

            driver.add_cookie(cookie)


def load_and_add_cookies(driver, path, domain):
    """Function to load cookies from json file and add to webdriver."""

    cookies = load_cookies(path)

    add_cookies_to_driver(driver, cookies, domain)



