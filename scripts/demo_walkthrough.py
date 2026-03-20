#!/usr/bin/env python3
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

ROOT = Path(__file__).resolve().parent.parent
BASE = 'http://127.0.0.1:8000'
API = 'http://127.0.0.1:8765'
SCREEN_DIR = ROOT / 'demo-screens'
SCREEN_DIR.mkdir(exist_ok=True)


def snap(driver, name):
    driver.save_screenshot(str(SCREEN_DIR / f'{name}.png'))


def main():
    driver = webdriver.Safari()
    wait = WebDriverWait(driver, 20)
    try:
        driver.get(f'{BASE}/index.html')
        time.sleep(1)
        snap(driver, '01-home')

        driver.get(f'{BASE}/robotics-brief-download.html')
        wait.until(EC.presence_of_element_located((By.ID, 'email')))
        driver.find_element(By.ID, 'email').send_keys('demo-walkthrough@example.com')
        Select(driver.find_element(By.ID, 'persona')).select_by_value('operator')
        snap(driver, '02-brief-form')
        driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

        time.sleep(2)
        snap(driver, '03-after-submit')
        driver.get(f'{API}/thank-you')
        time.sleep(1)
        snap(driver, '04-thank-you')

        driver.get(f'{API}/premium-offer')
        time.sleep(1)
        snap(driver, '05-premium-offer')

        driver.get(f'{BASE}/tools.html')
        time.sleep(1)
        snap(driver, '06-tools')

        print('Demo walkthrough complete. Screenshots saved to', SCREEN_DIR)
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
