from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time


class SbisMainPage:
    def __init__(self, driver):
        self.driver = driver

    def open_main_page(self):
        self.driver.get("https://sbis.ru/")
        print("\nГлавная страница открыта.")

    def go_to_download_page(self):
        footer_locator = (By.XPATH, "//a[@class='sbisru-Footer__link' and @href='/download']")

        # Ожидание появления элемента в DOM
        footer_link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(footer_locator))

        # Попытка кликнуть на элемент с обработкой StaleElementReferenceException
        attempts = 3
        for attempt in range(attempts):
            try:
                # Скроллинг до Footer
                self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", footer_link)
                time.sleep(1)

                # Клик по ссылке
                footer_link.click()
                print("Переход на страницу 'Скачать локальные версии' выполнен.")
                return
            except StaleElementReferenceException:
                print(f"Попытка #{attempt + 1} повторного поиска элемента...")
                footer_link = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(footer_locator))
        raise Exception("Не удалось выполнить клик по ссылке 'Скачать локальные версии' после нескольких попыток.")