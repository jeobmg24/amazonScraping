from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def url_or_item(item):
    if "www.amazon.com" in item:
        return "url"
    else:
        return "item"

def get_price(items):
    driver = webdriver.Chrome()
    results = {}

    for item in items:
        print(item)
        typa_shii = url_or_item(item)
        print(typa_shii)

        if typa_shii == "item":
            driver.get("https://www.amazon.com/")
            wait = WebDriverWait(driver, 10)
            searchbox = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
            searchbox.clear()
            searchbox.send_keys(item)
            submit = wait.until(EC.element_to_be_clickable((By.ID, "nav-search-submit-button")))
            submit.click()
            time.sleep(5)

            new = driver.find_element(By.CSS_SELECTOR, 'a.a-link-normal.s-no-outline')
            try:
                print(new.text)
                new.click()
                time.sleep(5)
            except:
                print(f"error: cannot find price")
                time.sleep(2)

            price_elements = driver.find_elements(By.CSS_SELECTOR, ".a-price")
            for price in price_elements:
                price = price.text
                if "$" in price:
                    price = price.replace('\n', ".")
                    results[item] = price
                    break

            try:
                savings = driver.find_element(By.CLASS_NAME, "a-section a-spacing-none aok-align-center aok-relative")
                if savings:
                    savings = savings.text
                    print(savings)
            except:
                print("No savings found")

        elif typa_shii == "url":
            driver.get(item)
            price_elements = driver.find_elements(By.CSS_SELECTOR, ".a-price")
            for price in price_elements:
                price = price.text
                if "$" in price:
                    price = price.replace('\n', ".")
                    results[item] = price
                    break

            try:
                savings = driver.find_element(By.CLASS_NAME, "a-section a-spacing-none aok-align-center aok-relative")
                if savings:
                    savings = savings.text
                    print(savings)
            except:
                print("No savings found")

    driver.quit()
    return results

