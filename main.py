import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import locale

locale.setlocale(locale.LC_NUMERIC, "tr_TR.UTF-8")

def convert_to_turkish_number_format(price_text):
    try:
        price = float(price_text.replace('₺', '').replace('.', '').replace(',', '').strip())
        return '{:,.2f}'.format(price).replace(',', '.')
    except ValueError:
        return price_text


def convert_to_turkish_number_format2(price_text):
    try:
        price = float(price_text.replace('₺', '').replace('.', '').replace(',', '').strip())

        # Sayıyı bir birim sola kaydırıp ilk 5 birimi alıyoruz.
        shifted_price = int(price * 10)
        formatted_price = '{:,.0f}'.format(shifted_price)[:5].replace(',', '.')

        # Sonrasına TL ekliyoruz.
        return f"{formatted_price} TL"
    except ValueError:
        return price_text




driver_avis = webdriver.Chrome()
driver_enterprise = webdriver.Chrome()

url1 = "https://www.avis.com.tr/rezervasyon/araciniz?id=IO_hMHEuGFriXGURTW8Qp45TMSALpHD0PWICaR4PpgtUy6XrrH3XY40p384fKQejXQwEw9W6IlKAI3L211yK7Sq_yIMPujH_EPyogDOqSKinBzNnp3DmGXVlSkE6X5end_l_pmH80N7x31mX_w4aAg&utm_referrer=https%3A%2F%2Fwww.avis.com.tr%2F"
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
    price_text1 = convert_to_turkish_number_format(price_element1.text)
    if price_text1:
        avis_data.append({"model": car_model_data1, "fiyat": price_text1})

# ENTERPRISE KISMI
car_container2 = driver_enterprise.find_element(By.CLASS_NAME, "car__list")
car_elements2 = car_container2.find_elements(By.XPATH, "//div[contains(@class, 'car__list-item-inner')]")
for car_element in car_elements2:
    car_model_data2 = car_element.find_element(By.CLASS_NAME, "title").text
    price_element2 = car_element.find_element(By.XPATH, ".//div[@class='price']")
    price_text2 = convert_to_turkish_number_format2(price_element2.text)
    if price_text2:
        enterprise_data.append({"model": car_model_data2, "fiyat": price_text2})

# Selenium'u kapatma
driver_avis.quit()
driver_enterprise.quit()

# JSON dosyasına yazma
output_data = {"avis": avis_data, "enterprise": enterprise_data}
output_file_path = r"C:\Users\ozgur\OneDrive\Masaüstü\output.json"

with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=2)

print(f"Veriler başarıyla '{output_file_path}' dosyasına kaydedildi.")
