from pages.sbis_contacts_page import SbisContactsPage
from pages.tensor_about_page import TensorAboutPage
from pages.sbis_main_page import SbisMainPage
from conftest import driver

def test_first_scenario(driver):
    main_page = SbisMainPage(driver)
    main_page.open_main_page()

    # Инициализация страницы контактов
    contacts_page = SbisContactsPage(driver)

    # Клик по вкладке "Контакты"
    contacts_page.click_contacts_tab()

    # Клик по элементу всплывающего окна
    contacts_page.click_region_offices_link()

    # Клик по баннеру Тензор
    contacts_page.click_tensor_banner()

    # Переключение на новую вкладку
    driver.switch_to.window(driver.window_handles[1])

    # Проверка блока "Сила в людях" с автоскроллингом
    about_page = TensorAboutPage(driver)
    about_page.verify_power_in_people_block()

    # Переход по ссылке "Подробнее"
    about_page.click_details()

    # Проверка URL
    assert driver.current_url == "https://tensor.ru/about", "Incorrect URL after clicking 'Подробнее'"

    # Проверка размеров изображений в разделе "Работаем"
    about_page.verify_timeline_images_dimensions()