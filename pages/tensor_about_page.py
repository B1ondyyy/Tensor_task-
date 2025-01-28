import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class TensorAboutPage(BasePage):
    POWER_IN_PEOPLE = (By.XPATH, "//p[text()='Сила в людях']")
    DETAILS_LINK = (By.XPATH, "//a[@href='/about' and contains(@class, 'tensor_ru-link')]")
    WORK_SECTION_IMAGES = (By.CSS_SELECTOR, "div.tensor_ru-About__block3 img")
    WORK_SECTION_TITLE = (By.XPATH, "//h2[text()='Работаем']")

    # Методы
    def verify_power_in_people_block(self):
        # Ожидание и скроллинг до блока
        element = self.wait_for_element(self.POWER_IN_PEOPLE)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        assert element.is_displayed(), "Power in People block not found"

    def click_details(self):
        time.sleep(1)
        # Переход по ссылке "Подробнее"
        details_link = self.wait_for_element(self.DETAILS_LINK)
        details_link.click()

    def verify_timeline_images_dimensions(self):
        # Скроллинг до раздела
        section_title = self.wait_for_element(self.WORK_SECTION_TITLE)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", section_title)

        # Ожидание появления изображений
        time.sleep(3)
        images = self.driver.find_elements(*self.WORK_SECTION_IMAGES)
        assert images, "No images found in the 'Работаем' section"

        # Проверка размеров изображений
        dimensions = [(img.size['width'], img.size['height']) for img in images]
        assert len(set(dimensions)) == 1, f"Images have inconsistent dimensions: {dimensions}"

        # Дополнительная проверка: вывод информации о размере каждой картинки
        for index, (width, height) in enumerate(dimensions):
            print(f"\nImage {index + 1}: Width = {width}, Height = {height}")

        # Проверяем, что размеры совпадают с первой картинкой
        first_width, first_height = dimensions[0]
        for width, height in dimensions:
            assert width == first_width and height == first_height, \
                f"Image size mismatch: Expected ({first_width}, {first_height}), got ({width}, {height})"