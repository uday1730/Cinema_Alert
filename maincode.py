



# Initializing User Input
movie_name = "Mufasa: The Lion King" # Paste exactly
city = "guntur".title()
user_date = 22
language = "telugu"  # Language selection (can be 'Telugu', 'Hindi', etc.)
theater_to_track = []
format = "2D"  # Format selection (can be '2D', '3D', or 'ALL') ALL is not working properly
iteration = 0 #To print the present iteration
running_frequencey = 5 #At what time gap should next iteration of entire program
tracking_frequencey = 50 #At what iterations should tracking be printed
missed_call = 0

# Dictionary of all available theaters
theaters_dict = {
    1: "GS Cinemas", 
    2: "V Celluloid Bhaskar Cinemas", 
    3: "Cine Prime Cinema", 
    4: "Pallavi Keerthana Complex", 
    5: "Hollywood Bollywood Theaters",
    6: "Naaz Cinemas",
    7: "Mythri Cinemas Phoenix Mall",
    8: "Plateno Cinemas Dolby Atmos 4K Barco Projection",
    9: "PVR Guntur",
    10: "Cine Square Dolby Atmos A/C",
    11: "JLE Cinemas",
    12: "Sri Saraswathi Picture Palace A/C Christie Laser Projection",
    13: "Krishna Mahal",
    14: "Venkata Krishna Theatre",
    15: "KKR Sai Nivya A/C Dts"
}

# Initialize an empty set to store unique theater names
theater_set = set()

# Add the selected theaters to the theater_set based on the provided numbers
for num in theater_to_track:
    if num in theaters_dict:  # Check if the number exists in the dictionary
        theater_set.add(theaters_dict[num])

# Convert the set back to a list (optional if you need a list)
theater_list = list(theater_set)

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

# Dictionary to store the theater and show details
theater_shows = {}

# File path for storing previous show details
file_path = 'theater_show_details.json'

#running code
"""
[ec2-user@ip-172-31-95-123 ~]$ sudo yum install -y Xvfb
Last metadata expiration check: 0:09:23 ago on Mon Dec 16 06:38:09 2024.
Package xorg-x11-server-Xvfb-21.1.13-5.amzn2023.0.2.x86_64 is already installed.
Dependencies resolved.
Nothing to do.
Complete!
[ec2-user@ip-172-31-95-123 ~]$ Xvfb :99 & export DISPLAY=:99
[1] 36451
[ec2-user@ip-172-31-95-123 ~]$ python3 maincode.py

Xvfb :99 & export DISPLAY=:99

"""
#For cmd copy code
#scp -i final_pem.pem maincode.py ec2-user@3.83.104.46:/home/ec2-user/  
#scp -i final_pem.pem theater_show_details.json ec2-user@52.90.83.185:/home/ec2-user/

def trigger_call():
    # Exotel API credentials
    api_key = "5dda9acd22b250d3acc0eb77015085b86941c49bcbb2463a"  # API Key
    api_token = "2ebc28cfd635a51deff365a4551063d26cf18c1540e02d99"  # API Token
    account_sid = "student1300"  # Account SID
    base_url = "https://api.exotel.com/v1/Accounts"

    # Replace with verified ExoPhone and target phone number
    exophone = "04045209865"  # Exotel's ExoPhone number
    target_number = "9014166047"  # The phone number to call

    # API endpoint and payload
    url = f"{base_url}/{account_sid}/Calls/connect"
    payload = {
        "From": target_number,  # Your verified number
        "To": target_number,    # To make a missed call to the same number
        "CallerId": exophone,   # Exotel's ExoPhone number
        "CallType": "trans"     # Call type (transactional or promotional)
    }

    try:
        # Make the API request with Basic Auth
        response = requests.post(url, data=payload, auth=(api_key, api_token))

        # Check the response status
        if response.status_code == 200 or response.status_code == 202:
            print("Missed call triggered successfully!")
        else:
            print(f"Failed to trigger the call: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"An error occurred: {e}")

def send_telegram_message_for_alert(message):
    #Send a message to a Telegram bot, ensuring theater entries aren't split across messages.

    bot_token = "7750538327:AAHCmx3F3QHNCnMRasuuhCFY-4tCyaAgiHU"  # Replace with your bot's token
    chat_id = "831517295"  # Replace with your chat ID
    send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    max_message_length = 4000
    message_parts = []
    current_message = ""

    # Split message by theaters to avoid splitting within a theater
    try:
        theater_entries = message.split("\n")
    except Exception as e:
        total_function()

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
                file_json = json.load(file)
                return file_json
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

    content += (f"<b><i>\"Movie: {movie_name.upper()}\"\n")
    content += (f"City: {city.upper()}\n")
    content += (f"Date: {user_date}th\n")
    content += (f"Total Theaters: {total_theaters}\n")
    content += (f"Total Shows: {total_shows}\n")
    content += "Shows breakup\n"
    content += f"Available: {available_count}\n"
    content += f"Fast Filling: {ff_count}\n"
    content += f"Few Left: {few_feft_count}\n"
    content += f"Blocked: {blocked_count}</i></b>"
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
                if missed_call:
                    trigger_call()

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

def total_function():
        
    #For aws
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    import sys

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    try:
        
        def core_process():
            global iteration
            while True:
                global aws_message
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

                except Exception as e:
                    print(e)
                    core_process()

                print("URL Loaded")

                # Step 1: Select language (either Hindi, Telugu, etc.), if available
                language_radio = driver.find_elements(By.XPATH, f"//input[@type='radio'][@value='{language.title()}']")
                if language_radio:
                    language_radio[0].click()  # Click the radio button corresponding to the language
                    print("Clicked language radio button")
                else:
                    print("No language radio button")
                    pass

                # Step 2: Wait for a second before selecting the format
                # time.sleep(0.5)

                # Step 3: Select format (either 2D, 3D, or ALL), if present
                format_radio = driver.find_elements(By.XPATH, f"//input[@type='radio'][@value='{format.upper()}']")
                if format_radio:
                    format_radio[0].click()  # Click the radio button corresponding to the format
                    print("Clicked format radio button")
                else:
                    print("No language radio button")
                    pass
                

                # Step 4: Wait for the page with the movie details to load
                time.sleep(1)

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
                                print("Movie found on page")
                                print("Movie clicked")
                                break  # Exit the loop after finding the match
                            else:
                                raise Exception("Force moving to except block")
                    movie_check()
                except :
                    try:
                        driver.get(f"https://paytm.com/movies/{city.lower()}/search")

                        search_movie = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//input[@type = 'search']"))
                        )
                        search_movie.send_keys(movie_name)

                        select_movie = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, f"//a[.//img[contains(@alt, '{movie_name.title()}')]]"))
                        )
                        select_movie.click()
                        print("Movie found on search")
                        print("Movie clicked")

                    except Exception as e:
                        movie_not_available = ""
                        movie_not_available += f"\"{movie_name}\" is not available in {city}."
                        print(movie_not_available)
                        aws_message += movie_not_available + "\n"
                        aws_message += send_telegram_message_for_tracking(movie_not_available)+"\n"
                        send_telegram_message_for_aws_status(aws_message)
                        time.sleep(30)
                        core_process()
                    

                time.sleep(1)

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
                        print(f"Pop-upped and clicked {language}")

                    # Click the Proceed button
                    proceed_button = driver.find_element(By.CLASS_NAME, "LanguageSelectionDialog_applyBtn__2frJM")
                    proceed_button.click()
                    print("Clicked proceed button")
                    
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
                            print(f"{user_date} Date selected")
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
                        time.sleep(30)
                        core_process()

                except Exception as e:
                    print(e)
                    driver.quit()
                    exit()  # Stop the script as the date is invalid

                time.sleep(3)

                def theater_run():
                    global aws_message
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

                        if (iteration % tracking_frequencey == 0 or iteration == 1):
                            print(f"Time to track entire {city}")
                            aws_message += all_theaters() + "\n"
                        time.sleep(1)
                        count = 0
                        print("Extracting theaters")
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

                    sys.stdout.flush()
                theater_run()

                while(True):
                    try:
                        iteration += 1
                        print(f"{iteration} Iteration.")
                        aws_message = f"{iteration} Iteration.\n"
                        driver.refresh()
                        WebDriverWait(driver, 20).until(
                            lambda d: d.execute_script("return document.readyState") == "complete"
                        )
                        print("Page loaded")
                        try:
                            # Wait until the element with the specified class appears and contains the required text
                            WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "MovieSessionsListingDesktop_movieSessions__KYv1d"))
                            )

                            # Locate the specific anchor tag containing the text
                            theater_element = WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, f"//a[not(normalize-space(text())={city.title()}) and normalize-space(text())!='']"))
                            )


                            # Print the text to verify
                            print("Theater element found:", theater_element.text)

                        except Exception as e:
                            print("Error:", e)
                        time.sleep(running_frequencey)
                        theater_run()
                    except:
                        total_function()
        core_process()

    except Exception as e :
        print(e)
        send_telegram_message_for_alert(e)
        send_telegram_message_for_aws_status(e)
        send_telegram_message_for_tracking(e)
        print("Running again")
        total_function()

total_function()