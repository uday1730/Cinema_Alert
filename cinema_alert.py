from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from selenium.common.exceptions import TimeoutException

# Initializing User Input
city = "guntur"
movie_name = "Pushpa 2: The Rule"
user_date = 6
language = "telugu"  # Language selection (can be 'Telugu', 'Hindi', etc.)
format = "2D"  # Format selection (can be '2D', '3D', or 'ALL') ALL is not working properly

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Open the Paytm Movies page for the city
    url = f"https://paytm.com/movies/{city.lower()}"
    driver.get(url)
    print(f"Opened URL: {url}")

    # Check if the page loads correctly by waiting for the body tag
    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))
        )
        print("Page loaded successfully.")
        time.sleep(0.5)
    except TimeoutException:
        print("URL is invalid (check city name).")
        driver.quit()
        exit()

    # Step 1: Select language (either Hindi, Telugu, etc.), if available
    language_radio = driver.find_elements(By.XPATH, f"//input[@type='radio'][@value='{language.title()}']")
    if language_radio:
        language_radio[0].click()  # Click the radio button corresponding to the language
        print(f"Language '{language.title()}' selected.")
        
    else:
        print(f"Language '{language.title()}' not available.")

    # Step 2: Wait for a second before selecting the format
    time.sleep(0.5)

    # Step 3: Select format (either 2D, 3D, or ALL), if present
    if format.upper() == "ALL":
        format_radio_2d = driver.find_elements(By.XPATH, "//input[@type='radio'][@value='2D']")
        format_radio_3d = driver.find_elements(By.XPATH, "//input[@type='radio'][@value='3D']")
        
        if format_radio_2d:
            format_radio_2d[0].click()  # Click the 2D radio button
            print("2D format selected.")
        if format_radio_3d:
            format_radio_3d[0].click()  # Click the 3D radio button
            print("3D format selected.")
        if not format_radio_2d and not format_radio_3d:
            print("No format options available.")
    else:
        format_radio = driver.find_elements(By.XPATH, f"//input[@type='radio'][@value='{format.upper()}']")
        if format_radio:
            format_radio[0].click()  # Click the radio button corresponding to the format
            print(f"Format '{format.upper()}' selected.")
        else:
            print(f"Format '{format.upper()}' not available.")

    # Step 4: Wait for the page with the movie details to load
    time.sleep(1.5)

    # Step 5: Check if the movie is available on the page
    try:
        driver.find_element(By.PARTIAL_LINK_TEXT, movie_name)
        print(f"Movie '{movie_name}' found.")
    except:
        print(f"Bookings for {movie_name}({language}) in {city.upper()} are not yet released!")
        driver.quit()
        exit()  # Stop the script if the movie is not found

    time.sleep(1)

    # Step 6: Find and click the Movie_name movie link
    movie_link = driver.find_element(By.PARTIAL_LINK_TEXT, movie_name)
    movie_link.click()
    print(f"Clicked on movie '{movie_name}' link.")
    time.sleep(2)

    # Check if the language selection popup is present
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "LanguageSelectionDialog_langSelectionContainer__jZY7u"))
        )
        time.sleep(0.5)
        
        # Step 2: Handle the language selection popup
        telugu_radio_button = driver.find_element(By.ID, f"{language.title()}-index-selection-dialog")
        if not telugu_radio_button.is_selected():
            telugu_radio_button.click()

        # Step 3: Click the Proceed button
        proceed_button = driver.find_element(By.CLASS_NAME, "LanguageSelectionDialog_applyBtn__2frJM")
        proceed_button.click()
        print("Language selected and proceeding...")
        
    except:
        print("No language selection popup found, proceeding to the next steps. or check the language")

    time.sleep(1)
    # Wait for the page with dates to load
    WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "DatesDesktop_cinemaDates__jMukI"))
    )
    print("Movie dates loaded successfully.")
    
    # Step 7: Select the date based on user input
    date_elements = driver.find_elements(By.CLASS_NAME, "DatesDesktop_cinemaDates__jMukI")

    for date_element in date_elements:
        try:
            date_text = date_element.find_element(By.CLASS_NAME, "DatesDesktop_date__bL7mg").text.strip()
            if date_text == str(user_date):
                # Use WebDriverWait to ensure the element is clickable
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable(date_element))
                # Use ActionChains to move to the element and click it
                actions = ActionChains(driver)
                actions.move_to_element(date_element).click().perform()

                # Optionally, scroll the element into view before clicking
                driver.execute_script("arguments[0].scrollIntoView(true);", date_element)

                # Add a delay of 3 seconds after clicking the date element
                time.sleep(1.5)
                print(f"Date {user_date} selected successfully!")
                break
        except Exception as e:
            print(f"Error selecting date: {str(e)}")

    # Step 8: Extract theater names and session times
    theater_elements = driver.find_elements(By.XPATH, f"//a[contains(@href, '/movies/{city.lower()}')]")

    # Regular expression to extract only time ending with AM/PM
    time_pattern = re.compile(r'\d{2}:\d{2} (AM|PM)')

    # Mappings for the session status
    status_mapping = {
        'yellowCol': 'FF',
        'greenCol': 'Available',
        'redCol': 'Few Left',
        'greyCol': 'Blocked'
    }

    # Initialize counters
    total_theaters = 0
    total_shows = 0

    # Extract details for each theater
    theater_count = 1
    for theater in theater_elements:
        theater_name = theater.text.split(',')[0]  # Extract name before the first comma
        if not theater_name.strip():
            continue

        total_theaters += 1
        print(f"Theater {theater_count}: {theater_name}")
        try:
            parent_div = theater.find_element(By.XPATH, "..//..//..")
            session_times = parent_div.find_elements(By.XPATH, ".//div[contains(@class, 'yellowCol') or contains(@class, 'redCol') or contains(@class, 'greenCol') or contains(@class, 'greyCol')]")
            
            valid_session_times = []
            for session in session_times:
                time_text = session.text.strip()
                match = time_pattern.match(time_text)
                if match:
                    status_class = session.get_attribute("class")
                    status_class_split = status_class.split()
                    status = status_mapping.get(status_class_split[0], "Unknown")
                    valid_session_times.append(f"{match.group(0)} ({status})")

            show_count = len(valid_session_times)
            total_shows += show_count
            if valid_session_times:
                print(f"  Shows ({show_count}): {' | '.join(valid_session_times)}")
            else:
                print("  No session times available.")
        except Exception as e:
            print(f"Error processing theater: {str(e)}")

        print("---------------------------------------------------")
        theater_count += 1

    # Print summary
    print(f"Movie: \"{movie_name.upper()}\"")
    print(f"City: {city.upper()}")
    print(f"Date: {user_date}th")
    print(f"Total Theaters: {total_theaters}")
    print(f"Total Shows: {total_shows}")

finally:
    # Close the driver
    driver.quit()