import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class SbisContactsPage(BasePage):
    CONTACTS_TAB = (By.XPATH, "//div[contains(@class, 'sbisru-Header__menu-link') and text()='Контакты']")
    REGION_OFFICES_LINK = (By.XPATH, "//a[@href='/contacts' and contains(@class, 'sbisru-link')]")
    TENSOR_BANNER = (By.XPATH, "//a[@href='https://tensor.ru/' and contains(@class, 'sbisru-Contacts__logo-tensor')]")
    REGION_TEXT = (By.XPATH, "//span[contains(@class, 'sbis_ru-Region-Chooser__text')]")
    PARTNERS_LIST_CONTAINER = (By.XPATH, "//div[@name='itemsContainer' and @data-qa='items-container']")
    PARTNERS_LIST_ITEMS = (By.XPATH, "//div[contains(@class, 'sbisru-Contacts-List__city')]")

    def click_contacts_tab(self):
        self.click(self.CONTACTS_TAB)

    def click_region_offices_link(self):
        self.click(self.REGION_OFFICES_LINK)

    def click_tensor_banner(self):
        time.sleep(2)
        banner = self.wait_for_element(self.TENSOR_BANNER)
        banner.click()

    def get_region_text(self):
        # Получение текста региона
        return self.get_text(self.REGION_TEXT)

    def get_partners_list_text(self):
        # Ожидание и получение списка названий партнеров.
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sbisru-Contacts-List__name"))
        )
        partner_elements = self.driver.find_elements(By.CSS_SELECTOR, ".sbisru-Contacts-List__name")
        return [partner.text.strip() for partner in partner_elements]

    def verify_region_and_partners(self, expected_region, expected_city):
        time.sleep(2)
        current_region = self.get_region_text()
        print(f"\nТекущий регион: {current_region}")

        if current_region != expected_region:
            raise AssertionError(f"Ожидался регион '{expected_region}', но получен '{current_region}'.")

        # Извлечение города из списка партнеров
        city_elements = self.driver.find_elements(By.XPATH, "//div[contains(@id, 'city-id-')]")
        city_names = [city.text for city in city_elements]
        print(f"Города партнеров: {city_names}\n")

        # Проверка, есть ли ожидаемый город в списке
        if expected_city not in city_names:
            raise AssertionError(f"Город '{expected_city}' не найден в списке городов партнеров.")

    def change_region(self, new_region):
        # Нажать на текущий регион
        current_region_element = self.driver.find_element(By.XPATH, "//span[contains(@class, 'sbis_ru-Region-Chooser')]")
        current_region_element.click()

        # Подождать появления списка регионов
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[@title='{new_region}']"))
        )

        # Найти элемент нового региона и кликнуть по нему
        new_region_element = self.driver.find_element(By.XPATH, f"//span[@title='{new_region}']")
        new_region_element.click()

    def verify_region_change(self, expected_region, expected_city):
        # Словарь для сопоставления региона с его URL-формой
        region_to_url = {
            "Камчатский край": "41-kamchatskij-kraj",
            "Тюменская обл.": "72-tjumenskaja-obl",
        }

        # Ожидание обновления региона
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, "//span[contains(@class, 'sbis_ru-Region-Chooser__text')]"),
                expected_region
            )
        )

        # Проверка текущего региона
        current_region = self.get_region_text()
        if current_region != expected_region:
            raise AssertionError(f"Регион не изменился. Ожидалось '{expected_region}', но получено '{current_region}'.")

        print(f"Регион успешно изменен на: {current_region}")

        # Проверить URL
        current_url = self.driver.current_url
        expected_region_in_url = region_to_url.get(expected_region)
        if expected_region_in_url not in current_url:
            raise AssertionError(
                f"URL не содержит информацию о регионе. Ожидалось '{expected_region_in_url}' в {current_url}."
            )
        print(f"URL корректен: {current_url}")

        # Извлечение информации о партнере и городе
        partner_title_xpath = "//div[contains(@class, 'sbisru-Contacts-List__name')]"
        partner_city_xpath = "//div[contains(@class, 'sbisru-Contacts-List__city')]"

        partner_title = self.driver.find_element(By.XPATH, partner_title_xpath).text.strip()
        partner_city = self.driver.find_element(By.XPATH, partner_city_xpath).text.strip()

        # Вывод информации в консоль
        print(f"Название партнера: {partner_title}")
        print(f"Город партнера: {partner_city}")

        # Проверка title страницы
        page_title = self.driver.title
        if expected_region not in page_title:
            raise AssertionError(
                f"Title страницы не содержит информацию о регионе. Ожидалось '{expected_region}' в '{page_title}'."
            )
        print(f"Title корректен и содержит информацию о регионе: {page_title}")