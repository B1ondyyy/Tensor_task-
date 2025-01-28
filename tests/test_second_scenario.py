from pages.sbis_main_page import SbisMainPage
from conftest import driver
from pages.sbis_contacts_page import SbisContactsPage

def test_second_scenario(driver):
    main_page = SbisMainPage(driver)
    main_page.open_main_page()

    # Инициализация страницы контактов
    contacts_page = SbisContactsPage(driver)

    # Клик по вкладке "Контакты"
    contacts_page.click_contacts_tab()

    # Клик по элементу во всплывающем окне
    contacts_page.click_region_offices_link()

    # Проверка региона и списка партнеров
    contacts_page.verify_region_and_partners(expected_region="Тюменская обл.", expected_city="Тюмень")

    # Изменение региона
    contacts_page.change_region("Камчатский край")

    # Проверка, что регион изменился, список партнеров обновился, URL и title корректны
    contacts_page.verify_region_change(expected_region="Камчатский край", expected_city="Петропавловск-Камчатский")