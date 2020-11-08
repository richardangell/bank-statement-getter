import json


def save_cookie(driver, path):

    with open(path, 'w') as filehandler:

        json.dump(driver.get_cookies(), filehandler)



def load_cookies(path):

    with open(path, 'r') as cookiesfile:

        cookies = json.load(cookiesfile)

    return cookies


def add_cookies_to_driver(driver, cookies, domain):

    for cookie in cookies:
        
        if cookie['domain'] == domain:

            driver.add_cookie(cookie)


def load_and_add_cookies(driver, path, domain):

    cookies = load_cookies(path)

    add_cookies_to_driver(driver, cookies, domain)



