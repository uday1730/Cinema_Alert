import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re
from selenium.common.exceptions import TimeoutException
import requests

# Initializing User Input
city = "bengaluru"
movie_name = "ui" # Paste exactly
user_date = 21
language = "kannada"  # Language selection (can be 'Telugu', 'Hindi', etc.)
format = "2D"  # Format selection (can be '2D', '3D', or 'ALL') ALL is not working properly
iteration = 0 #To print the present iteration
tracking_frequencey = 10 #At what iterations should tracking be printed
running_frequencey = 30 #At what time gap should next iteration of entire program

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# List of specific theaters to track
theater_list = []

# Dictionary to store the theater and show details
theater_shows = {}

# File path for storing previous show details
file_path = 'theater_show_details.json'

def send_telegram_message_for_alert(message):
    #Send a message to a Telegram bot, ensuring theater entries aren't split across messages.

    bot_token = "7750538327:AAHCmx3F3QHNCnMRasuuhCFY-4tCyaAgiHU"  # Replace with your bot's token
    chat_id = "831517295"  # Replace with your chat ID
    send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    max_message_length = 4000
    message_parts = []
    current_message = ""

    # Split message by theaters to avoid splitting within a theater
    theater_entries = message.split("\n")

    for entry in theater_entries:
        if len(current_message) + len(entry) + 1 > max_message_length:  # +1 for the newline character
            # Add the current message to parts and start a new one
            message_parts.append(current_message.strip())
            current_message = entry + "\n"
        else:
            current_message += entry + "\n"

    # Add the last message if any content remains
    if current_message.strip():
        message_parts.append(current_message.strip())

    try:
        for part in message_parts:
            payload = {
                "chat_id": chat_id,
                "text": part,
                "parse_mode": "HTML"  # Optional: Use HTML formatting in messages
            }
            response = requests.post(send_url, data=payload)
            if response.status_code == 200:
                print("Alert message sent to Telegram!")
            else:
                print(f"Failed to send alert message: {response.status_code}, {response.text}")
                return f"Failed to send alert message: {response.status_code}, {response.text}"
        return "Alert message sent to Telegram!"
    except Exception as e:
        print(f"Error sending alert message: {e}")
        return f"Error sending alert message: {e}"


    

def send_telegram_message_for_tracking(message):
    # Send a message to a Telegram bot, ensuring theater entries aren't split across messages.

    bot_token = "7867650386:AAHafcmdd1YEzLJVikrhVWE5xjzm4mvpk7Y"  # Replace with your bot's token
    chat_id = "831517295"  # Replace with your chat ID
    send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    max_message_length = 4000
    message_parts = []
    current_message = ""

    # Split message by theaters to avoid splitting within a theater
    theater_entries = message.split("\n")

    for entry in theater_entries:
        if len(current_message) + len(entry) + 1 > max_message_length:  # +1 for the newline character
            # Add the current message to parts and start a new one
            message_parts.append(current_message.strip())
            current_message = entry + "\n"
        else:
            current_message += entry + "\n"

    # Add the last message if any content remains
    if current_message.strip():
        message_parts.append(current_message.strip())

    try:
        for part in message_parts:
            payload = {
                "chat_id": chat_id,
                "text": part,
                "parse_mode": "HTML"  # Optional: Use HTML formatting in messages
            }
            response = requests.post(send_url, data=payload)
            if response.status_code == 200:
                print("Tracking message sent to Telegram!")
            else:
                print(f"Failed to send tracking message: {response.status_code}, {response.text}")
                return f"Failed to send tracking message: {response.status_code}, {response.text}"
        return "Tracking message sent to Telegram!"
    except Exception as e:
        print(f"Error sending tracking message: {e}")
        return f"Error sending tracking message: {e}"



def send_telegram_message_for_aws_status(message):
    """Send a message to a Telegram bot, ensuring logical entries are not split across messages."""

    bot_token = "7898681070:AAFYbQ7svmQvIrpLdWAZmli761K5datgu0I"  # Replace with your bot's token
    chat_id = "831517295"  # Replace with your chat ID
    send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    max_message_length = 4000
    message_parts = []
    current_message = ""

    # Split the message by logical entries (e.g., lines or blocks)
    entries = message.split("\n")

    for entry in entries:
        if len(current_message) + len(entry) + 1 > max_message_length:  # +1 for the newline character
            # Add the current message to parts and start a new one
            message_parts.append(current_message.strip())
            current_message = entry + "\n"
        else:
            current_message += entry + "\n"

    # Add the last message if any content remains
    if current_message.strip():
        message_parts.append(current_message.strip())

    try:
        for part in message_parts:
            payload = {
                "chat_id": chat_id,
                "text": part,
                "parse_mode": "HTML"  # Optional: Use HTML formatting in messages
            }
            response = requests.post(send_url, data=payload)
            if response.status_code != 200:
                print(f"Failed to send AWS_STATUS message: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending AWS_STATUS message: {e}")



def load_previous_shows():
    """Load previous show data from the JSON file."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def all_theaters():

    global theater_elements
    global time_pattern
    global status_mapping

    content = ""

    # Initialize counters
    total_theaters = 0
    total_shows = 0
    available_count = 0
    ff_count = 0
    few_feft_count = 0
    blocked_count = 0
    
    # Extract details for each theater
    theater_count = 1
    for theater in theater_elements:
        theater_name = theater.text.split(',')[0]  # Extract name before the first comma
        if not theater_name.strip():
            continue

        total_theaters += 1
        content += f"Theater {theater_count}: {theater_name}\n"
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
                    if (status == "Available"):
                        available_count+=1
                    elif(status == "FF"):
                        ff_count += 1
                    elif(status == "Few Left"):
                        few_feft_count += 1
                    elif(status == "Blocked"):
                        blocked_count += 1
                        
                    valid_session_times.append(f"{match.group(0)} ({status})")

            show_count = len(valid_session_times)
            total_shows += show_count
            if valid_session_times:
                content += f"  Shows ({show_count}): {' | '.join(valid_session_times)}\n"
            else:
                print("  No session times available.")
        except Exception as e:
            print(f"Error processing theater: {str(e)}")

        theater_count += 1

    content += (f"\"Movie: {movie_name.upper()}\"\n")
    content += (f"City: {city.upper()}\n")
    content += (f"Date: {user_date}th\n")
    content += (f"Total Theaters: {total_theaters}\n")
    content += (f"Total Shows: {total_shows}\n")
    content += "Shows breakup\n"
    content += f"Available: {available_count}\n"
    content += f"Fast Filling: {ff_count}\n"
    content += f"Few Left: {few_feft_count}\n"
    content += f"Blocked: {blocked_count}"
    return send_telegram_message_for_tracking(content)

def compare_shows(previous_shows, current_shows):
    """Compare previous and current show data and send WhatsApp message on changes."""
    changes_detected = False  # Flag to track if there are any changes
    message = ""

    # Loop through the current shows
    for theater, current in current_shows.items():
        if theater in previous_shows:
            previous = previous_shows[theater]
            
            # Create dictionaries for current and previous shows with time as key and status as value
            previous_dict = {show.split(' (')[0]: show.split(' (')[1][:-1] for show in previous}
            current_dict = {show.split(' (')[0]: show.split(' (')[1][:-1] for show in current}

            added = []
            removed = []
            status_changed = []
            

            # Check for status changes, additions, and removals
            for time, status in current_dict.items():
                if time not in previous_dict:
                    added.append(f"{time} ({status})")
                elif previous_dict[time] != status:
                    status_changed.append(f"{time} ({status}) from (<s>{previous_dict[time]}</s>)")
            
            for time, status in previous_dict.items():
                if time not in current_dict:
                    removed.append(f"{time} ({status})")

            # Format the message if any changes are detected
            if added or removed or status_changed:
                message += f"CHANGES IN <i>{theater}</i>:\n"
                
                if status_changed:
                    message += "-- <b>update</b> : " + " | ".join(status_changed) + "\n"
                if added:
                    message += "-- <b>added</b> : " + " | ".join(added) + "\n"
                if removed:
                    message += "-- <b>removed</b> : <s>" + " | ".join(removed) + "</s>\n"

                
                changes_detected = True

        else:
            # If the theater is new, print its shows
            message += f"NEW THEATER \"<i>{theater}</i>\" ADDED WITH SHOWS: " + " | ".join(current) + "\n"
            changes_detected = True

    if not changes_detected:
        message = "<u>NO CHANGES</u>"
    
    print(message)

    if message!="<u>NO CHANGES</u>":
        send_telegram_message_for_alert(message)
    
    return str(message)

def main_function(theater,theater_name):
    global total_theaters
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
    

try:
    
    def core_process():
        global iteration
        while True: 
            aws_message = ""
            iteration += 1
            print(f"{iteration} Iteration.")
            aws_message = f"{iteration} Iteration.\n"
            #send_telegram_message_for_aws_status(aws_message)
            # Open the Paytm Movies page for the city
            url = f"https://paytm.com/movies/{city.lower()}"
            driver.get(url)

            # Check if the page loads correctly by waiting for the body tag
            try:
                WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.TAG_NAME, "body"))
                )
                time.sleep(0.5)
                
                if driver.current_url == "https://paytm.com/movies/select-city":
                    print(f"\"{city}\" is invalid. Please check the city name.")
                    driver.quit()
                    exit()  # Stop the script as the city is invalid

            except TimeoutException:
                core_process()

            # Step 1: Select language (either Hindi, Telugu, etc.), if available
            language_radio = driver.find_elements(By.XPATH, f"//input[@type='radio'][@value='{language.title()}']")
            if language_radio:
                language_radio[0].click()  # Click the radio button corresponding to the language
            else:
                pass

            # Step 2: Wait for a second before selecting the format
            # time.sleep(0.5)

            # Step 3: Select format (either 2D, 3D, or ALL), if present
            format_radio = driver.find_elements(By.XPATH, f"//input[@type='radio'][@value='{format.upper()}']")
            if format_radio:
                format_radio[0].click()  # Click the radio button corresponding to the format
            else:
                pass
            

            # Step 4: Wait for the page with the movie details to load
            time.sleep(2)

            # Step 5: Check if the movie is available on the page
            try:
                def movie_check():
                    movie_elements = driver.find_elements(By.CLASS_NAME, "DesktopRunningMovie_movTitle__Q1pOY")
                    # Loop through each element and compare
                    for movie_element in movie_elements:
                        # Extract text and normalize (lowercase + remove spaces)
                        element_text = movie_element.text.lower().replace(" ", "")
                        # Compare normalized strings
                        if element_text == movie_name.lower().replace(" ", ""):
                            movie_link = movie_element
                            movie_link.click()
                            break  # Exit the loop after finding the match
                        else:
                            raise Exception("Force moving to except block")
                movie_check()
            except :
                try:
                    driver.get(f"https://paytm.com/movies/{city}/search")

                    search_movie = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type = 'search']"))
                    )
                    search_movie.send_keys(movie_name)

                    select_movie = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//a[.//img[contains(@alt, '{movie_name.title()}')]]"))
                    )
                    select_movie.click()

                except Exception as e:
                    movie_not_available = ""
                    movie_not_available += f"\"{movie_name}\" is not available in {city}."
                    print(movie_not_available)
                    aws_message += movie_not_available + "\n"
                    aws_message += send_telegram_message_for_tracking(movie_not_available)+"\n"
                    send_telegram_message_for_aws_status(aws_message)
                    time.sleep(50)
                    core_process()
                

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
                    
            # Wait for the page with dates to load
            WebDriverWait(driver, 15).until(
                EC.visibility_of_all_elements_located((By.CLASS_NAME, "DatesDesktop_cinemaDates__jMukI"))
            )
            
            # Step 7: Select the date based on user input
            date_elements = driver.find_elements(By.CLASS_NAME, "DatesDesktop_cinemaDates__jMukI")

            available_dates = []

            try:
                for date_element in date_elements:
                    date_text = date_element.find_element(By.CLASS_NAME, "DatesDesktop_date__bL7mg").text.strip()
                    available_dates.append(date_text)
                    if date_text == str(user_date):
                        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(date_element))
                        actions = ActionChains(driver)
                        actions.move_to_element(date_element).click().perform()
                        driver.execute_script("arguments[0].scrollIntoView(true);", date_element)
                        break
                else:
                    date_not_available = f"Date \"{user_date}\" is not available.\n"
                    print(date_not_available)
                    aws_message += date_not_available
                    print("Available dates are: ")
                    aws_message += "Available dates are: "
                    for available_date in available_dates:
                        aws_message += str(available_date) + " "
                        print(available_date,end=" ")
                    print("\n")
                    aws_message += "\n" + send_telegram_message_for_alert(date_not_available) + "\n"
                    aws_message += send_telegram_message_for_tracking(date_not_available) + "\n"
                    send_telegram_message_for_aws_status(aws_message)
                    time.sleep(50)
                    core_process()

            except Exception as e:
                print(e)
                driver.quit()
                exit()  # Stop the script as the date is invalid

            time.sleep(2)

            try:
                # Step 8: Extract theater names and session times
                global theater_elements
                theater_elements = driver.find_elements(By.XPATH, f"//a[contains(@href, '/movies/{city.lower()}')]")

                # Regular expression to extract only time ending with AM/PM
                global time_pattern
                time_pattern = re.compile(r'\d{2}:\d{2} (AM|PM)')

                # Mappings for the session status
                global status_mapping
                status_mapping = {
                    'yellowCol': 'FF',
                    'greenCol': 'Available',
                    'redCol': 'Few Left',
                    'greyCol': 'Blocked'
                }
                global total_theaters
                total_theaters = 0
                global total_shows
                total_shows = 0

                global tracking_frequencey

                if (iteration % tracking_frequencey == 0):
                    aws_message += all_theaters() + "\n"

                count = 0

                for theater in theater_elements:
                    theater_name = theater.text.split(',')[0]  # Extract name before the first comma

                    if theater_name.lower() == city.lower():
                        continue
                    if not theater_name.strip():
                        break

                    if not theater_list:
                        main_function(theater,theater_name)
                        count += 1
                    else:
                        if theater_name in theater_list:  # Check if the theater is in our list
                            main_function(theater,theater_name)    
                            count += 1
                        
                if not count:
                    aws_message += "No mentioned theaters are available!"
                    print("No mentioned theaters are available!")
                    send_telegram_message_for_aws_status(aws_message)
                    pass


                if total_theaters > 0:
                    # Compare with the previous data if available
                    previous_shows = load_previous_shows()
                    aws_message += compare_shows(previous_shows, theater_shows) + "\n"
                    send_telegram_message_for_aws_status(aws_message)
                    # Save the current data to a JSON file
                    with open(file_path, 'w') as json_file:
                        json.dump(theater_shows, json_file, indent=4)
                else:
                    pass
            except Exception as e:
                print(e)
                pass 

            # Sleep for 30 seconds before running again
            global running_frequencey
            time.sleep(running_frequencey)

    core_process()

finally:
    # Close the driver
    driver.quit()