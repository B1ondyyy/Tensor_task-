import os
import requests
from selenium.webdriver.common.by import By

class SbisDownloadPage:
    def __init__(self, driver):
        self.driver = driver

    def download_plugin_for_windows(self, download_dir):
        download_button = self.driver.find_element(By.XPATH, "//a[contains(@href, 'sbisplugin-setup-web.exe')]")
        file_url = download_button.get_attribute("href")

        # Скачать файл
        response = requests.get(file_url, stream=True)
        file_path = os.path.join(download_dir, "SbisPluginSetup.exe")

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        print(f"Файл скачан и сохранен в {file_path}")
        return file_path

    def get_expected_file_size(self):
        download_button = self.driver.find_element(By.XPATH, "//a[contains(@href, 'sbisplugin-setup-web.exe')]")
        size_text = download_button.text.strip()
        print(f"Текст кнопки для скачивания: '{size_text}'")

        # Убедиться, что текст содержит информацию о размере
        if "МБ" not in size_text:
            raise ValueError(f"Размер файла не найден в тексте кнопки: '{size_text}'")

        # Извлечь размер файла
        try:
            size = size_text.split("(")[1].split(" ")[1].replace("МБ", "").replace(",", ".")
            return float(size)
        except (IndexError, ValueError) as e:
            raise ValueError(f"Не удалось извлечь размер файла из текста: '{size_text}'. Ошибка: {str(e)}")