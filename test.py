from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import TimeoutException

# Initializing User Input
city = "tenali"
movie_name = "Pushpa 2: The Rule"
user_date = 5
language = "Hindi"  # Language selection (can be 'Telugu', 'Hindi', etc.)
format = "3D"  # Format selection (can be '2D', '3D')

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Open the Paytm Movies page for the city
    url = f"https://paytm.com/movies/{city.lower()}"
    driver.get(url)

    # Check if the page loads correctly by waiting for the body tag
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except TimeoutException:
        print("URL is invalid (check city name).")
        driver.quit()
        exit()

    # Step 1: Select language (either Hindi, Telugu, etc.), if available
    language_radio = driver.find_elements(By.XPATH, f"//input[@type='radio'][@value='{language}']")
    if language_radio:
        language_radio[0].click()  # Click the radio button corresponding to the language

    # Step 2: Wait for a second before selecting the format
    time.sleep(1)

    # Step 3: Select format (either 2D or 3D), if present
    format_radio = driver.find_elements(By.XPATH, f"//input[@type='radio'][@value='{format}']")
    if format_radio:
        format_radio[0].click()  # Click the radio button corresponding to the format

    # Step 4: Wait for the page to load with the movie details (if necessary)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "DatesDesktop_cinemaDates__jMukI"))
    )

    # Step 5: Proceed with other actions (such as selecting the date) if necessary

finally:
    # Close the driver
    driver.quit()
