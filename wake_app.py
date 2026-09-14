import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Ambil URL aplikasi Streamlit kamu dari environment variable
STREAMLIT_URL = os.environ.get("STREAMLIT_APP_URL")

def main():
    if not STREAMLIT_URL:
        print("Error: STREAMLIT_APP_URL tidak diatur.")
        exit(1)

    # Konfigurasi Chrome untuk berjalan tanpa antarmuka (headless)
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = None
    try:
        # Inisialisasi driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print(f"Membuka {STREAMLIT_URL}...")
        driver.get(STREAMLIT_URL)

        wait = WebDriverWait(driver, 20)

        # Cek apakah ada tombol untuk membangunkan aplikasi
        try:
            # Tombolnya biasanya memiliki teks "Yes, get this app back up"
            wake_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Yes, get this app back up')]"))
            )
            print("Tombol 'wake up' ditemukan. Mengklik tombol...")
            wake_button.click()
            print("Tombol berhasil diklik. Aplikasi seharusnya mulai bangun.")
            # Tunggu beberapa saat agar proses loading berjalan
            time.sleep(10)
        except Exception:
            # Jika tombol tidak ditemukan, kemungkinan aplikasi sedang bangun
            print("Tombol 'wake up' tidak ditemukan. Aplikasi diasumsikan sudah bangun.")

    except Exception as e:
        print(f"Terjadi error: {e}")
        exit(1)
    finally:
        if driver:
            driver.quit()
            print("Proses selesai.")

if __name__ == "__main__":
    main()
