import json
import locale
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

locale.setlocale(locale.LC_NUMERIC, "tr_TR.UTF-8")

driver_avis = webdriver.Chrome()
driver_enterprise = webdriver.Chrome()

url1 = "https://www.avis.com.tr/rezervasyon/araciniz?id=IO_hMHEuGFriXGURTW8Qp3DiYqOy5hYt9CeE66AxdwQFoJiIzELuJeZExRVDT_H3l_iX8I4cxPC3BcBSaTq_alw_UCD9Cre5eFIcjlm58dStvg0U8OLkBkSEsd1HMf_VyAZB3cvXPXyRgqKCmrR9LA&utm_referrer=https%3A%2F%2Fwww.avis.com.tr%2F"
driver_avis.get(url1)

url2 = "https://www.enterprise.com.tr/rezervasyon/istanbul-havalimani-arac-kiralama?dropOffLocation=istanbul-havalimani-arac-kiralama&start=2024-01-22T12:00&end=2024-01-24T12:00&age=21-24&campaign"
driver_enterprise.get(url2)

wait_avis = WebDriverWait(driver_avis, 30)
wait_avis.until(EC.presence_of_element_located((By.CLASS_NAME, "car-model")))

wait_enterprise = WebDriverWait(driver_enterprise, 30)
wait_enterprise.until(EC.presence_of_element_located((By.CLASS_NAME, "car__list-item-inner")))

avis_data = []
enterprise_data = []

# AVİS KISMI
car_container1 = driver_avis.find_element(By.CLASS_NAME, "primary-vehicle-card-list")
car_elements1 = car_container1.find_elements(By.XPATH, "//div[contains(@class, 'card-front')]")
for car_element in car_elements1:
    car_model_data1 = car_element.find_element(By.CLASS_NAME, "car-model").text
    price_element1 = car_element.find_element(By.XPATH, ".//span[@class='price']")
    price_text1 = price_element1.text.replace('TL', '').replace('.', '').replace(',', '').strip()
    if price_text1:
        price_data1 = float(price_text1)
        avis_data.append({"model": car_model_data1, "fiyat": str(price_data1)})

# ENTERPRISE KISMI
car_container2 = driver_enterprise.find_element(By.CLASS_NAME, "car__list")
car_elements2 = car_container2.find_elements(By.XPATH, "//div[contains(@class, 'car__list-item-inner')]")
for car_element in car_elements2:
    car_model_data2 = car_element.find_element(By.CLASS_NAME, "title").text
    price_element2 = car_element.find_element(By.XPATH, ".//div[@class='price']")
    price_text2 = price_element2.text.replace('₺', '').replace('.', '').replace(',', '').strip()
    if price_text2:
        try:
            price_data2 = float(price_text2)
            enterprise_data.append({"model": car_model_data2, "fiyat": str(price_data2)})
        except ValueError:
            print("Geçersiz fiyat formatı:", price_element2.text)

# Selenium'u kapatma
driver_avis.quit()
driver_enterprise.quit()

# JSON dosyasına yazma
output_data = {"avis": avis_data, "enterprise": enterprise_data}
output_file_path = r"C:\Users\ozgur\OneDrive\Masaüstü\output.json"

with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, indent=2)

print(f"Veriler başarıyla '{output_file_path}' dosyasına kaydedildi.")
