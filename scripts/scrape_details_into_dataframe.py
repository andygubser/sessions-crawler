import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def scrape_class_name(driver, class_name: str):
    try:
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
        return driver.find_element(By.CLASS_NAME, class_name).text

    except TimeoutException:
        return ""


def scrape_xpath(driver, xpath: str):
    try:
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return driver.find_element(By.XPATH, xpath).text

    except TimeoutException:
        return ""


def scrape_link(driver, xpath: str):
    try:
        WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return driver.find_element(By.XPATH, xpath).get_attribute('href')

    except TimeoutException:
        return ""


def scrape_details_into_dataframe(driver, url):
    """

    :param url:
    :return:
    """

    driver.get(url)

    # TODO: improve wait condition, reduce wait time
    driver.implicitly_wait(3)

    str_title = "gds"
    title = scrape_class_name(driver, str_title)

    xpath_affair_number = \
        '//tr[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "w66", " " ))]'
    str_affair_number = scrape_xpath(driver, xpath_affair_number)

    xpath_affair_type = \
        '//tr[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "w66", " " ))]'
    str_affair_type = scrape_xpath(driver, xpath_affair_type)

    # xpath_document = \
    #     '//tr[(((count(preceding-sibling::*) + 1) = 3) and parent::*)]//li'
    xpath_document = "/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/table/tbody/tr[3]/td/ul/li/a"
    str_document = scrape_link(driver, xpath_document)

    xpath_submitter = \
        '//tr[(((count(preceding-sibling::*) + 1) = 4) and parent::*)]//li'
    str_submitter = scrape_xpath(driver, xpath_submitter)

    #TODO: XPATH are not the same on every page...
    xpath_lead = \
        '//tr[(((count(preceding-sibling::*) + 1) = 5) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "w66", " " ))]'
    str_lead = scrape_xpath(driver, xpath_lead)

    xpath_emergency = \
        '//tr[(((count(preceding-sibling::*) + 1) = 6) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "w66", " " ))]'
    str_emergency = scrape_xpath(driver, xpath_emergency)

    xpath_importance_granted = \
        '//tr[(((count(preceding-sibling::*) + 1) = 8) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "w66", " " ))]'
    str_importance_granted = scrape_xpath(driver, xpath_importance_granted)

    xpath_submit_date = \
        '//tr[(((count(preceding-sibling::*) + 1) = 9) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "w66", " " ))]'
    str_submit_date = scrape_xpath(driver, xpath_submit_date)

    dict_affairs = {
        "Link zum Geschäft": url,
        "Titel": title,
        "Geschäftsnummer": [str_affair_number],
        "Geschäftstyp": [str_affair_type],
        "Vorstossdokument": [str_document],
        "Eingereicht durch": [str_submitter],
        "Federführung": [str_lead],
        "Dringlichkeit beantragt": [str_emergency],
        "Dringlichkeit gewährt": [str_importance_granted],
        "Eingereicht am": [str_submit_date]
    }
    print(dict_affairs)

    df = pd.DataFrame.from_dict(dict_affairs)
    print(df)
    return df
