import time
import random
from .conftest import ValueStorage
from .settings import console_logger
from .settings import answer_logger
from pytest_bdd import scenario, given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# Constants
LINK = 'https://yandex.ru/'
UP_LIMIT_COST = 20000
DOWN_LIMIT_DIAGONAL = 3

ALL_FILTERS_BUTTON = 'a[data-auto= "allFiltersButton"]'
CATALOG_BUTTON = 'catalogPopupButton'
CONFIRM_SORT_BUTTON = "//div[@data-tid='4add5a7e']//a[2]"
DIAGONAL_PRECISE_FILTER = '//h4[contains(text(),"Диагональ экрана (точно)")]'
DIAGONAL_PRECISE_INPUT = "div[data-prefix = 'от'] > input[placeholder='2.45']"
LAST_PHONE_SELECTOR = 'div[data-test-id="virtuoso-item-list"] > div:last-child'
MANUFACTURES_CHECKBOX = '//div[@data-filter-id="7893318" and @data-tid="46a32646"]/div'
MANUFACTURES_FILTER = "div[data-filter-id='7893318']"
MARKET_ICON = 'a[data-id="market"]'
RATING_ICON_CSS_SELECTOR = 'span[data-auto="rating-badge-value"]'
RATING_ICON_XPATH_SELECTOR = 'span[@data-auto="rating-badge-value"]'
PHONES_SELECTOR = 'div[data-test-id="virtuoso-item-list"] > div'
RATING_SORT_SELECTOR = "//button[contains(text(), 'рейтинг')]"
PRODUCT_TITLE = '//div[@data-zone-name="productCardTitle"]//h1'
SMARTPHONE_SECTION = '//a[contains(text(),"Смартфоны")]'
UP_LIMIT_COST_INPUT = "div[data-prefix = 'до'] > input"


# Scenarios
@scenario('../feature/web.feature', 'Smartphone searching by specified parameters')
def test_web(browser):
    pass


@given('full screen browser')
def ya_market_(browser):
    console_logger.debug(f'Connection by {LINK}')
    browser.get(LINK)


@given('Yandex Market page')
def yandex_market_page(browser):
    console_logger.debug(f'Search for Market icon {browser.current_url}')
    browser.find_element(By.CSS_SELECTOR, MARKET_ICON).click()

    console_logger.debug('Switching to market window')
    old_window, new_window = browser.window_handles[0], browser.window_handles[1]
    browser.switch_to.window(new_window)


@given('Smartphone section')
def smartphone_section(browser):
    console_logger.debug(f'Search for Smartphones section {browser.current_url}')
    catalog_button = WebDriverWait(browser, 12).until(
        EC.element_to_be_clickable((By.ID, CATALOG_BUTTON))
    )
    catalog_button.click()

    browser.find_element(By.XPATH, SMARTPHONE_SECTION).click()


@when('I push the All filters button')
def all_filters_button(browser):
    console_logger.debug(f'Search for "All filters" button on the {browser.current_url}')
    all_filt_button = browser.find_element(By.CSS_SELECTOR, ALL_FILTERS_BUTTON)

    browser.execute_script("return arguments[0].scrollIntoView(true);", all_filt_button)

    all_filt_button.click()


@when('I set the search parameter to 20,000 rub. and a screen diagonal of 3 inches')
def filters_param(browser):
    console_logger.debug(f'Search for up limit cost filter on the {browser.current_url}')
    cost_input = browser.find_element(By.CSS_SELECTOR, UP_LIMIT_COST_INPUT)
    cost_input.send_keys(UP_LIMIT_COST)
    browser.refresh()

    console_logger.debug('Search for diagonal filter')
    diagonal_precise = browser.find_element(By.XPATH, DIAGONAL_PRECISE_FILTER)
    browser.execute_script("return arguments[0].scrollIntoView(true);", diagonal_precise)
    WebDriverWait(browser, 12).until(EC.element_to_be_clickable(diagonal_precise))
    diagonal_precise.click()

    diagonal_input = browser.find_element(By.CSS_SELECTOR, DIAGONAL_PRECISE_INPUT)
    WebDriverWait(browser, 12).until(EC.element_to_be_clickable(diagonal_input))
    diagonal_input.send_keys(DOWN_LIMIT_DIAGONAL)
    browser.refresh()


@when('choose at least 5 any manufacturers')
def choose_firm(browser):
    console_logger.debug('Search for manufactures filter')
    manufacturers_menu = browser.find_element(By.CSS_SELECTOR, MANUFACTURES_FILTER)
    browser.execute_script("return arguments[0].scrollIntoView(true);", manufacturers_menu)

    list_manufact = browser.find_elements(By.XPATH, MANUFACTURES_CHECKBOX)
    list_of_numbers_of_manufact = random.sample(range(1, len(list_manufact)), 5)
    for item in list_of_numbers_of_manufact:
        browser.find_element(By.XPATH, MANUFACTURES_CHECKBOX + f'[{item}]//label').click()
    browser.refresh()


@when('I click the "Show" button')
def execute_sort(browser):
    console_logger.debug('Search for sort confirmation button')
    browser.find_element(By.XPATH, CONFIRM_SORT_BUTTON).click()


@when('I remember the last phone on the first page')
def remember_last_child(browser):
    console_logger.debug('Search for last element on the page')
    length_list = len(browser.find_elements(By.CSS_SELECTOR, PHONES_SELECTOR))
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(browser, 12).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, LAST_PHONE_SELECTOR))
        )

        new_length_list = len(browser.find_elements(By.CSS_SELECTOR, PHONES_SELECTOR))
        if new_length_list == length_list:

            ValueStorage.remembered_phone = browser.find_element(By.CSS_SELECTOR,
                                                                 LAST_PHONE_SELECTOR + ' a[data-baobab-name="title"]>span').text
            ValueStorage.remembered_phone_rating = browser.find_element(By.CSS_SELECTOR,
                                                                        LAST_PHONE_SELECTOR + ' ' + RATING_ICON_CSS_SELECTOR).text
            break
        else:
            length_list = new_length_list
            continue

    console_logger.debug(f'The last smartphone on the page: {ValueStorage.remembered_phone}')
    console_logger.debug(f'Rating: {ValueStorage.remembered_phone_rating}')

    browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL and Keys.HOME)


@when('choose the sort by rating')
def change_sort(browser):
    console_logger.debug('Choose sort by rating')
    sort_by_rating = browser.find_element(By.XPATH, RATING_SORT_SELECTOR)
    WebDriverWait(browser, 12).until(EC.element_to_be_clickable((By.XPATH, RATING_SORT_SELECTOR)))
    sort_by_rating.click()
    time.sleep(3)


@when('find the phone that was remembered')
def search_for_remembered_phone(browser):

    page_number = 1
    not_found = True

    while not_found:
        console_logger.debug(f'Searching on the {page_number} page for the remembered phone')
        last_phone_item = browser.find_element(By.CSS_SELECTOR, LAST_PHONE_SELECTOR)
        length_list = len(browser.find_elements(By.CSS_SELECTOR, PHONES_SELECTOR))

        while True:
            browser.execute_script('return arguments[0].scrollIntoView(true);', last_phone_item)
            last_phone_item = WebDriverWait(browser, 12).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, LAST_PHONE_SELECTOR))
            )
            new_length_list = len(browser.find_elements(By.CSS_SELECTOR, PHONES_SELECTOR))
            if new_length_list == length_list:
                break
            else:
                length_list = new_length_list
                continue

        list_items = browser.find_elements(By.CSS_SELECTOR, PHONES_SELECTOR)

        # Поиск по элементам страницы
        for i in range(length_list):
            if ValueStorage.remembered_phone in list_items[0].text:
                item = browser.find_element(By.CSS_SELECTOR,
                                            f"div[data-index='{i}'] h3[data-zone-name='title'] > a")
                browser.execute_script('return arguments[0].scrollIntoView(true);', item)
                item.click()

                old_window, new_window = browser.window_handles[1], browser.window_handles[2]
                browser.switch_to.window(new_window)  # Переключение на новое окно браузера

                not_found = False
                break
            else:
                list_items.pop(0)

                # Переход на другую страницу
                if not list_items:
                    page_number += 1
                    pagination_page = WebDriverWait(browser, 12).until(
                        EC.visibility_of_element_located((By.XPATH,
                                                          f"//div[@data-auto='pagination-page' and text()='{page_number}']"))
                    )
                    pagination_page.click()
                    browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL and Keys.HOME)
                    time.sleep(3)
                continue


@then('I print out a rating of the phone')
def print_out_rating(browser):
    console_logger.debug('Comparing items')
    item_rating = browser.find_element(By.XPATH,
                                       '//div/' + RATING_ICON_XPATH_SELECTOR).get_attribute("textContent")
    item_title = browser.find_element(By.XPATH, PRODUCT_TITLE).text
    assert ValueStorage.remembered_phone == item_title and ValueStorage.remembered_phone_rating == item_rating, \
        "It's not that phone or rating has changed "
    print()
    answer_logger.warning(f'THE ANSWER ON TEST: rating - {item_rating}')
    print()
