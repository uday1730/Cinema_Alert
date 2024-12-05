import json
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
user_date = 5
language = "telugu"  # Language selection (can be 'Telugu', 'Hindi', etc.)
format = "2D"  # Format selection (can be '2D', '3D', or 'ALL') ALL is not working properly

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# List of specific theaters to track
theater_list = [
    "Mythri Cinemas Phoenix Mall",
    "PVR Guntur",
    "JLE Cinemas"
]

# Dictionary to store the theater and show details
theater_shows = {}

# File path for storing previous show details
file_path = 'theater_show_details.json'

def load_previous_shows():
    """Load previous show data from the JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def compare_shows(previous_shows, current_shows):
    """Compare previous and current show data and print only the changes."""
    changes_detected = False  # Flag to track if there are any changes
    
    for theater, current in current_shows.items():
        if theater in previous_shows:
            previous = previous_shows[theater]
            added = [show for show in current if show not in previous]
            removed = [show for show in previous if show not in current]
            
            # Print the changes
            if added:
                print(f"CHANGES DETECTED IN {theater}:")
                print("  ADDED:", " | ".join(added))
                changes_detected = True
            if removed:
                print(f"CHANGES DETECTED IN {theater}:")
                print("  REMOVED:", " | ".join(removed))
                changes_detected = True
        else:
            # If the theater is new, print its shows
            print(f"NEW THEATER {theater} ADDED WITH SHOWS: {' | '.join(current)}")
            changes_detected = True

    if not changes_detected:
        print("NO CHANGES")

try:
    # Open the Paytm Movies page for the city
    url = f"https://paytm.com/movies/{city.lower()}"
    driver.get(url)

    # Check if the page loads correctly by waiting for the body tag
    try:
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(0.5)
    except TimeoutException:
        driver.quit()
        exit()

    # Step 1: Select language (either Hindi, Telugu, etc.), if available
    language_radio = driver.find_elements(By.XPATH, f"//input[@type='radio'][@value='{language.title()}']")
    if language_radio:
        language_radio[0].click()  # Click the radio button corresponding to the language
    else:
        pass

    # Step 2: Wait for a second before selecting the format
    time.sleep(0.5)

    # Step 3: Select format (either 2D, 3D, or ALL), if present
    format_radio = driver.find_elements(By.XPATH, f"//input[@type='radio'][@value='{format.upper()}']")
    if format_radio:
        format_radio[0].click()  # Click the radio button corresponding to the format
    else:
        pass

    # Step 4: Wait for the page with the movie details to load
    time.sleep(1.5)

    # Step 5: Check if the movie is available on the page
    try:
        driver.find_element(By.PARTIAL_LINK_TEXT, movie_name)
    except:
        driver.quit()
        exit()  # Stop the script if the movie is not found

    time.sleep(1)

    # Step 6: Find and click the Movie_name movie link
    movie_link = driver.find_element(By.PARTIAL_LINK_TEXT, movie_name)
    movie_link.click()
    time.sleep(2)

    # Check if the language selection popup is present
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "LanguageSelectionDialog_langSelectionContainer__jZY7u"))
        )
        time.sleep(0.5)
        
        # Handle the language selection popup
        telugu_radio_button = driver.find_element(By.ID, f"{language.title()}-index-selection-dialog")
        if not telugu_radio_button.is_selected():
            telugu_radio_button.click()

        # Click the Proceed button
        proceed_button = driver.find_element(By.CLASS_NAME, "LanguageSelectionDialog_applyBtn__2frJM")
        proceed_button.click()
        
    except:
        pass

    time.sleep(1)
    # Wait for the page with dates to load
    WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, "DatesDesktop_cinemaDates__jMukI"))
    )
    
    # Step 7: Select the date based on user input
    date_elements = driver.find_elements(By.CLASS_NAME, "DatesDesktop_cinemaDates__jMukI")

    for date_element in date_elements:
        try:
            date_text = date_element.find_element(By.CLASS_NAME, "DatesDesktop_date__bL7mg").text.strip()
            if date_text == str(user_date):
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable(date_element))
                actions = ActionChains(driver)
                actions.move_to_element(date_element).click().perform()
                driver.execute_script("arguments[0].scrollIntoView(true);", date_element)
                time.sleep(1.5)
                break
        except Exception as e:
            pass

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
    for theater in theater_elements:
        theater_name = theater.text.split(',')[0]  # Extract name before the first comma
        if not theater_name.strip():
            continue

        if theater_name in theater_list:  # Check if the theater is in our list
            total_theaters += 1
            shows = []
            try:
                parent_div = theater.find_element(By.XPATH, "..//..//..")
                session_times = parent_div.find_elements(By.XPATH, ".//div[contains(@class, 'yellowCol') or contains(@class, 'redCol') or contains(@class, 'greenCol') or contains(@class, 'greyCol')]")

                for session in session_times:
                    time_text = session.text.strip()
                    match = time_pattern.match(time_text)
                    if match:
                        status_class = session.get_attribute("class")
                        status_class_split = status_class.split()
                        status = status_mapping.get(status_class_split[0], "Unknown")
                        shows.append(f"{match.group(0)} ({status})")

                if shows:
                    theater_shows[theater_name] = shows
                else:
                    pass
            except Exception as e:
                pass

    if total_theaters > 0:
        # Compare with the previous data if available
        previous_shows = load_previous_shows()
        compare_shows(previous_shows, theater_shows)

        # Save the current data to a JSON file
        with open(file_path, 'w') as json_file:
            json.dump(theater_shows, json_file, indent=4)
    else:
        pass

finally:
    # Close the driver
    driver.quit()