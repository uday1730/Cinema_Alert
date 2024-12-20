from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

def booking_movie_tickets(url):

    driver.get(url)
    driver.maximize_window()

    search_movie = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type = 'search']"))
    )
    search_movie.send_keys(movie_name)

    select_movie = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[.//img[contains(@alt, '{movie_name}')]]"))
    )
    select_movie.click()

    '''time_slot = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='greenCol MovieSessionsListingDesktop_time__r6FAI' and contains(text(), '06:30 PM')]"))
    )
    time_slot.click()'''

    # Calling time function i.e; in which time we want to select the movie tickets
    select_time()

    # Calling seats booking function
    seats_booking()
    
    '''book_tickets = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(text())='Book Tickets']"))
    )
    book_tickets.click()'''
    
    

    input()

def select_time():
    
    try:
        time_slot = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '0{hrs}:45 {noon}')]"))
        )
        time_slot.click()
    except:
        for minutes in range(0, 60, 5):
            try:
                if(hrs < 10 and minutes < 10):
                    time_slot = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '0{hrs}:0{minutes} {noon}')]"))
                    )
                    time_slot.click()
                    break
                elif(hrs < 10 and minutes > 10):
                    time_slot = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '0{hrs}:{minutes} {noon}')]"))
                    )
                    time_slot.click()
                    break
                elif(hrs > 10 and minutes < 10):
                    time_slot = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{hrs}:0{minutes} {noon}')]"))
                    )
                    time_slot.click()
                    break
                else:
                    time_slot = WebDriverWait(driver, 2).until(
                        EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{hrs}:{minutes} {noon}')]"))
                    )
                    time_slot.click()
                    break
            except:
                print(f"0{hrs}:{minutes} {noon}")
                pass


def seats_booking():
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, f"//div[@class='FixedSeatingDesktop_seatName__m6_Hm' and contains(text(), '{ticket_row}')]"))
        )
    except:
        pass

    no_rows = WebDriverWait(driver, 1).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class = 'FixedSeatingDesktop_seatName__m6_Hm']"))
    )
    print(f'count : {len(no_rows)}')

    pos_alp = ord(ticket_row) - ord('A') + 1

    if(pos_alp <= len(no_rows)):
        for seat in seats_arr:
            try:
                try:
                    seats = driver.find_element(By.XPATH, f"//div[@class='FixedSeatingDesktop_seatName__m6_Hm' and contains(text(), '{ticket_row}')]/following-sibling::div//span[contains(@class, 'available') and text()='{seat}']")
                    seats.click()
                    selected_seats.append(f"{ticket_row}{seat} seat is alloted to you.")
                except:
                    seats = driver.find_element(By.XPATH, f"//div[@class='FixedSeatingDesktop_seatName__m6_Hm' and contains(text(), '{ticket_row}')]/following-sibling::div//span[contains(@class, 'FixedSeatingDesktop_disable__RQsl1') and text()='{seat}']")
                    not_selected_seats.append(f"{ticket_row}{seat} seat already occupied by others.")
            except:
                try:
                    seats = driver.find_element(By.XPATH, f"//div[@class='FixedSeatingDesktop_seatName__m6_Hm']/following-sibling::div//span[contains(@class, 'available') and text()='{ticket_row}{seat}']")
                    seats.click()
                    selected_seats.append(f"{ticket_row}{seat} seat is alloted to you.")
                except:
                    seats = driver.find_element(By.XPATH, f"//div[@class='FixedSeatingDesktop_seatName__m6_Hm']/following-sibling::div//span[contains(@class, 'FixedSeatingDesktop_disable__RQsl1') and text()='{ticket_row}{seat}']")
                    not_selected_seats.append(f"{ticket_row}{seat} seat already occupied by others.")
    else:
        print(f"{RED}In that movie theatre their are only upto {chr(ord('A') + (len(no_rows) - 1))} row/s.")
        print(f"Please book the rows from A to {chr(ord('A') + (len(no_rows) - 1))} row/s.{RESET}")


GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"  # Reset to default color

place = "guntur".title()
movie_name = "pranaya godari".lower().title()


ticket_row = input("Enter which row do you want to book the ticket : ")[:1].upper()
try:
    error = 0
    int(ticket_row)
    print(f'\n{RED}You want to enter alphabet to book the desired row.{RESET}')
    print()
    error = 1
    exit()
except:
    pass
if(error == 1):
    exit()
else:
    pass


seats_arr = []

selected_seats = []
not_selected_seats = []


try:
    tickets_count = int(input("Enter how many tickets do you want to book : "))
    for i in range(tickets_count):
        seats_arr.append(str(input(f"Enter {i + 1} seat number : ")))
except ValueError:
    print(f"\n{RED}occured Value Error due to invalid input is entered by the user !!!{RESET}")
    print()
    exit()


while(True):
    shows = int(input('Enter which show do you want to see the movie\n1) Morning show\n2) Matinee show\n3) First show\n4) Second show\n\nEnter the choice (1/2/3/4) : '))
    if(shows == 1):
        hrs = 11
        noon = 'AM'
        break
    elif(shows == 2):
        hrs = 2
        noon = 'PM'
        break
    elif(shows == 3):
        hrs = 6
        noon = 'PM'
        break
    elif(shows == 4):
        hrs = 9
        noon = 'PM'
        break
    else:
        pass


# Start Chrome with the specified user profile
driver = webdriver.Chrome()

# Run the movie ticket booking process
booking_movie_tickets(f"https://paytm.com/movies/{place}/search")


if(len(selected_seats) == len(seats_arr)):
    print(f"{GREEN}All seats are allocated.{RESET}")
elif(len(selected_seats) == 0):
    print(f"{RED}No seats are allocated.{RESET}")
else:
    print(f"{GREEN}{len(selected_seats)} seats had allocated{RESET} and {RED}{len(not_selected_seats)} seats had not allocated.")

if(len(selected_seats) == 0):
    pass
else:
    print()
    for select_seat in selected_seats:
        print(f"{GREEN}{select_seat}{RESET}")
    print("\n\n")

if(len(not_selected_seats) == 0):
    pass
else:
    print()
    for not_select_seat in not_selected_seats:
        print(f"{RED}{not_select_seat}{RESET}")
    print("\n\n")













'''

# ANSI escape codes for colors
WHITE = "\033[37m"
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
RESET = "\033[0m"  # Reset to default color

print(f"{RED}This is red{RESET}, {GREEN}this is green{RESET}, and {BLUE}this is blue{RESET}.")

'''