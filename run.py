from model import *
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep

def wait_for(condition_function):
  while True:
    if condition_function():
        return True
    else:
        sleep(1)

def link_has_gone_stale(link):
    def inner_func():
        try:
            link.find_elements_by_id('doesnt-matter')
            return False
        except StaleElementReferenceException:
            return True
    return inner_func

def click_and_wait(btn):
    btn.click()
    wait_for(link_has_gone_stale(btn))

def run_datapoint(data_point: DataPoint, driver: WebDriver):
    match data_point.id_type:
        case FieldType.NAME:
            driver.find_element_by_name(data_point.field).send_keys(data_point.value)
        case FieldType.ID:
            driver.find_element_by_id(data_point.field).send_keys(data_point.value)
        case _:
            raise TypeError(f"unknown field type: {data_point}")

def run_dataentry_action(data: list[DataPoint], driver: WebDriver):
    match data:
        case [DataPoint() as data_point, *rest]:
            run_datapoint(data_point, driver)
            run_dataentry_action(rest, driver)
        case []:
            return
        case _:
            raise TypeError(f"unrecognized data entry item: {data}")

def get_button(action: ClickAction, driver: WebDriver):
    match action.id_type:
        case FieldType.ID:
            return driver.find_element_by_id(action.btn)
        case FieldType.NAME:
            return driver.find_element_by_name(action.btn)
        case _:
            raise TypeError(f"error getting button: {ClickAction}")

def run_click_action(action: ClickAction, driver: WebDriver):
    if action.wait:
        click_and_wait(get_button(action, driver))
    else:
        get_button(action, driver).click()

def run_sleep_action(action: SleepAction, driver: WebDriver):
    sleep(action.time)

def run_action(action: Action, driver: WebDriver):
    match action:
        case DataEntryAction(data_points=dp):
            run_dataentry_action(dp, driver)
        case ClickAction() as action:
            run_click_action(action, driver)
        case SleepAction() as action:
            run_sleep_action(action, driver)
        case _:
            raise TypeError(f"unrecognized action: {action}")

def run_actionlist(actions: list[Action], driver: WebDriver):
    match actions:
        case [Action() as action, *rest]:
            run_action(action, driver)
            run_actionlist(rest, driver)
        case []:
            return
        case _:
            raise TypeError(f"unrecognized action in list: {actions}")

def run(ast: AST):
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)

    driver.get(ast.url)

    run_actionlist(ast.actions, driver)