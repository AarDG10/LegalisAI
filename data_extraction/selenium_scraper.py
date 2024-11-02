import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def scroll_to_element(driver, element):
    """Scroll the webpage to bring the element into view."""
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)  # Add a slight delay to allow the page to adjust

def click_view_judgement_icons(driver):
    """Click on all 'View Judgement' eye icons on the page."""
    try:
        # Wait for the icons to be present
        icons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".view-icon"))
        )
        
        for icon in icons:
            attempts = 0
            while attempts < 3:  # Retry clicking the icon up to 3 times
                try:
                    scroll_to_element(driver, icon)
                    icon.click()
                    print("Clicked on icon successfully.")
                    break  # Break out of the retry loop if click is successful
                except Exception as e:
                    print(f"Error clicking icon: {e}")
                    attempts += 1
                    time.sleep(1)  # Wait before retrying
                    # Optionally, you can refresh the list of icons if necessary
                    icons = driver.find_elements(By.CSS_SELECTOR, ".view-icon")
    
    except Exception as e:
        print(f"An error occurred while clicking icons: {e}")

def main():
    # Setup Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode if desired
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Create a new Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Navigate to the target website
        driver.get("https://maharera.maharashtra.gov.in/orders-judgements?from_date=&to_date=&page=2&op=Submit")

        # Call the function to click on judgement icons
        click_view_judgement_icons(driver)

        # Wait for a few seconds to ensure all clicks are processed
        time.sleep(5)

    finally:
        driver.quit()  # Clean up and close the browser

if __name__ == "__main__":
    main()
