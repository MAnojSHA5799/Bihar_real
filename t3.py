import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

URL = "https://rera.bihar.gov.in/RegisteredPP.aspx"

# ==========================
# DRIVER SETUP
# ==========================
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


# ==========================
# SCRAPE CURRENT PAGE
# ==========================
def scrape_current_page(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    tbody = soup.find("tbody")

    developers = []

    if tbody:
        rows = tbody.find_all("tr", class_="text-dark")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 5:
                project = cols[0].get_text(strip=True)
                reg_no = cols[1].get_text(strip=True)
                promoter = cols[2].get_text(strip=True)
                address = cols[3].get_text(strip=True)
                date = cols[4].get_text(strip=True)

                if "DEVELOPER" in promoter.upper():
                    developers.append({
                        "Project Name": project,
                        "Registration No": reg_no,
                        "Promoter Name": promoter,
                        "Address": address,
                        "Date": date
                    })

    return developers


# ==========================
# SCRAPE ALL PAGES
# ==========================
def scrape_all_pages():
    driver = get_driver()
    driver.get(URL)
    time.sleep(5)

    all_data = []

    page_number = 1

    while True:
        print(f"\nScraping Page {page_number}...")

        data = scrape_current_page(driver)
        all_data.extend(data)

        try:
            # Find pagination link for next page number
            next_page_link = driver.find_element(
                By.XPATH,
                f"//a[contains(@href,'Page${page_number + 1}')]"
            )

            driver.execute_script("arguments[0].click();", next_page_link)
            time.sleep(4)

            page_number += 1

        except:
            print("No more pages available.")
            break

    driver.quit()
    return all_data


# ==========================
# MAIN
# ==========================
if __name__ == "__main__":

    print("Starting Full Pagination Scraping...")

    developers = scrape_all_pages()

    print("\nDevelopers Found:\n")

    for dev in developers:
        print("--------------------------------------------------")
        print("Project:", dev["Project Name"])
        print("Promoter:", dev["Promoter Name"])
        print("Registration:", dev["Registration No"])
        print("Date:", dev["Date"])

    df = pd.DataFrame(developers)
    df.to_csv("bihar_rera_all_pages_developers.csv", index=False)

    print("\nData saved to bihar_rera_all_pages_developers.csv")