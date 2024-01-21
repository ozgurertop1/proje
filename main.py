# -*- coding: utf-8 -*-

import locale
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

# Türkçe sayı formatına uygunluğu sağlama
locale.setlocale(locale.LC_NUMERIC, "tr_TR.UTF-8")

# Web sürücüsünü başlatma (Chrome kullanıldı, kendi tarayıcınıza göre değiştirebilirsiniz)
driver_avis = webdriver.Chrome()
driver_enterprise = webdriver.Chrome()

# Web sitesinin URL'si
url1 = "https://www.avis.com.tr/rezervasyon/araciniz?id=IO_hMHEuGFriXGURTW8Qpze-cxbetB0L6kr1i1bjuUwGjIA33bZOz8mPyRejHVP_RXHIXk5elB6kJmTYWISuRaMM9MEV1FHArc34ZZ7jLsF3Eq79l-dxMqj6llbqUsUr2rScmMmIbdqF4oqH-HMVHw&utm_referrer=https%3A%2F%2Fwww.avis.com.tr%2F"
driver_avis.get(url1)

url2 = "https://www.enterprise.com.tr/rezervasyon/istanbul-havalimani-arac-kiralama?dropOffLocation=istanbul-havalimani-arac-kiralama&start=2024-01-19T12:00&end=2024-01-21T12:00&age=21-24&campaign"
driver_enterprise.get(url2)

# Sayfanın tam yüklenmesini beklemek için bir bekleme tanımlama
wait_avis = WebDriverWait(driver_avis, 30)
wait_avis.until(EC.presence_of_element_located((By.CLASS_NAME, "car-model")))

wait_enterprise = WebDriverWait(driver_enterprise, 30)
wait_enterprise.until(EC.presence_of_element_located((By.CLASS_NAME, "car__list-item-inner")))

# Çıktıları masaüstündeki bir not defterine yönlendirme
desktop_path = r"C:\Users\ozgur\OneDrive\Masaüstü\c.txt"
output_file_path = desktop_path + "output.txt"

with open(output_file_path, 'w', encoding='utf-8') as file:
    sys.stdout = file  # Çıktıyı dosyaya yönlendirme

    # AVİS KISMI
    print('AVİS')
    car_container1 = driver_avis.find_element(By.CLASS_NAME, "primary-vehicle-card-list")
    car_elements1 = car_container1.find_elements(By.XPATH, "//div[contains(@class, 'card-front')]")
    for car_element in car_elements1:
        car_model_data1 = car_element.find_element(By.CLASS_NAME, "car-model").text
        price_element1 = car_element.find_element(By.XPATH, ".//span[@class='price']")
        price_text1 = price_element1.text.replace('TL', '').replace('.', '').replace(',', '').strip()
        if price_text1:
            price_data1 = float(price_text1)
            print('Aracın modeli :', car_model_data1, 've', 'aracın fiyatı :', price_element1.text)
        else:
            print("Arac verisi bulunamadı.")

    # ENTERPRISE KISMI
    print("ENTERPRISE")
    car_container2 = driver_enterprise.find_element(By.CLASS_NAME, "car__list")
    car_elements2 = car_container2.find_elements(By.XPATH, "//div[contains(@class, 'car__list-item-inner')]")
    for car_element in car_elements2:
        car_model_data2 = car_element.find_element(By.CLASS_NAME, "title").text
        price_element2 = car_element.find_element(By.XPATH, ".//div[@class='price']")
        price_text2 = price_element2.text.replace('₺', '').replace('.', '').replace(',', '').strip()
        if price_text2:
            try:
                price_data2 = float(price_text2)
                print('Aracın modeli :', car_model_data2, 've', 'aracın fiyatı :', price_element2.text)
            except ValueError:
                print("Geçersiz fiyat formatı:", price_element2.text)
        else:
            print("Arac verisi bulunamadı.")

    sys.stdout = sys.__stdout__  # Çıktıyı tekrar orijinal durumuna getirme

print(f"Çıktılar başarıyla '{output_file_path}' dosyasına kaydedildi.")

# Selenium'u kapatma
driver_avis.quit()
driver_enterprise.quit()
