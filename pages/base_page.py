from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator):
        self.wait_for_element(locator).click()

    def get_text(self, locator):
        return self.wait_for_element(locator).text

    def wait_and_click(self, locator, timeout=10, attempts=3):
        for attempt in range(attempts):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(locator)
                )
                element.click()
                return
            except StaleElementReferenceException:
                print(f"Попытка #{attempt + 1} повторного поиска элемента...")
        raise Exception("Не удалось выполнить клик по элементу после нескольких попыток.")