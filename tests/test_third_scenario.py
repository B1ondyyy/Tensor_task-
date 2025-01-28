from pages.sbis_main_page import SbisMainPage
from pages.sbis_download_page import SbisDownloadPage
from conftest import driver
import os
import time


def wait_for_download_to_finish(download_dir, timeout=30):
    end_time = time.time() + timeout
    while time.time() < end_time:
        files = os.listdir(download_dir)
        if any(file.endswith(".crdownload") for file in files):  # Проверка временных файлов
            time.sleep(1)
        else:
            return True
    raise TimeoutError(f"Файл не был загружен полностью за {timeout} секунд.")


def test_third_scenario(driver):
    main_page = SbisMainPage(driver)

    # Переход на страницу
    main_page.open_main_page()
    main_page.go_to_download_page()

    download_page = SbisDownloadPage(driver)

    # Скачивание плагина СБИС
    download_dir = os.path.join(os.getcwd(), "downloads")  # Папка для сохранения файла
    os.makedirs(download_dir, exist_ok=True) # Создать папку, если её нет

    downloaded_file_path = download_page.download_plugin_for_windows(download_dir)

    # Ожидание завершения загрузки
    wait_for_download_to_finish(download_dir)

    # Проверка, что файл скачался
    assert os.path.exists(downloaded_file_path), "Файл плагина не был скачан."
    print("Скачивание плагина подтверждено.")

    # Проверка размера файла
    actual_size = os.path.getsize(downloaded_file_path) / (1024 * 1024)  # Размер в МБ
    expected_size = download_page.get_expected_file_size()

    assert round(actual_size, 2) == round(expected_size, 2), (
        f"Размер файла не соответствует. Ожидалось: {expected_size} МБ, получено: {actual_size:.2f} МБ."
    )
    print(f"Размер файла совпадает: {actual_size:.2f} МБ.")