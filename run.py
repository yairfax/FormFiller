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

def click_and_wait(id, driver: WebDriver):
    btn = driver.find_element_by_id(id)
    btn.click()
    wait_for(link_has_gone_stale(btn))

def run_datapoint(data_point: DataPoint, driver: WebDriver):
    match data_point.id_type:
        case FieldType.NAME:
            driver.find_element_by_name(data_point.field).send_keys(data_point.value)
        case FieldType.ID:
            driver.find_element_by_id(data_point.field).send_keys(data_point.value)
        case _:
            raise TypeError("unknown field type: %s" % data_point)

def run_dataentry_action(data: list[DataPoint], driver: WebDriver):
    match data:
        case [DataPoint() as data_point, *rest]:
            run_datapoint(data_point, driver)
            run_dataentry_action(rest, driver)
        case []:
            return
        case _:
            raise TypeError("unrecognized data entry item: %s" % data)


def run_click_action(action: ClickAction, driver: WebDriver):
    if action.wait:
        click_and_wait(action.btn, driver)
    else:
        driver.find_element_by_id(action.btn, driver).click()

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

def run_actionlist(actions: list[Action], driver: WebDriver):
    match actions:
        case [Action() as action, *rest]:
            run_action(action, driver)
            run_actionlist(rest, driver)
        case []:
            return
        case _:
            raise TypeError("unrecognized action in list: %s" % actions)

def run(ast: AST):
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)

    driver.get(ast.url)

    run_actionlist(ast.actions, driver)