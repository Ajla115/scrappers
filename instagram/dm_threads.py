import threading
import random
import mysql.connector
from time import sleep
from dotenv import load_dotenv
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys  
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


load_dotenv("../.env")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQLdatabasepass123!",
    database="sdp_project"
)

#Autocommit is set to True, so everything will get autocomitted by default
mydb.autocommit = True

mycursor = mydb.cursor()

def get_scheduled_messages():
    query = "SELECT ud.users_email, ud.users_password, ia.username, ud.message, ud.port_value, ud.id FROM users_dms ud JOIN instagram_accounts ia ON ud.recipients_id = ia.id WHERE ud.status = 'Scheduled'"
    mycursor.execute(query)
    results = mycursor.fetchall()

    if not results:
        print("No scheduled messages found therefore nothing can be sent to anybody.")
        exit()  

    for result in results:
        port_value = result[4] 
        user_email = result[0]

        if not port_value:
            print("Port value is missing for certain DM sendings, therefore first that will get solved.")
            
            # Generate a unique new port
            # First, check if that user email already has somewhere else a db port in the db
            # If it has then use the same port, otherwise create a new one port

            query = "SELECT port_value FROM users_dms WHERE users_email = %s"

            #This %s needs a tuple as a parameter so below where the user_email is the only parameter
            # comma should be put behind it to mimic the behavior of a tuple
            mycursor.execute(query, (user_email, ))
            users_port_value = mycursor.fetchone()
            #Perhaps, this one port has been previously used multiple times by the user email so it is enough just to extract it once when we reach it

            if users_port_value:
                #Extract the exact value from the tuple
                users_port_value = users_port_value[0]
                print("This ", user_email, " already has an existing port valu ", users_port_value, ". Therefore this one will be used.")
            else:
                #If this user email has never had a port before, a new one will get generated foor the user
                users_port_value = generate_new_port()
            

            # Clear any unread results
            # Because above I had mycursor.fetchone() all rows got returned, but only one got read
            # There are other rows that are stuck inbetween and that are not read, but the cursor is filled with them so it cannot execute other queries
            # So, with the statement below, we are reading rows that were left behind, and cčeaning the cursor so we can go on with the query
            mycursor.fetchall()

            # Update the record with the new unique port value or the one that already existed
            update_query = "UPDATE users_dms SET port_value = %s WHERE users_email = %s"
            mycursor.execute(update_query, (users_port_value, user_email))
          

    query2 = "SELECT ud.users_email, ud.users_password, ia.username, ud.message, ud.port_value, ud.id FROM users_dms ud JOIN instagram_accounts ia ON ud.recipients_id = ia.id WHERE ud.status = 'Scheduled'"
    mycursor.execute(query2)
    results2 = mycursor.fetchall()

    return results2

def generate_new_port():
    while True:
        # Generate a new port value
        new_port = random.randint(100, 10000)
        # Check if this port is unique
        mycursor.execute("SELECT COUNT(*) FROM users_dms WHERE port_value = %s", (new_port,))
        if mycursor.fetchone()[0] == 0:
            # Port is unique, return it
            return new_port

def get_unique_senders():
    query = "SELECT users_email FROM users_dms WHERE status = 'Scheduled' GROUP BY users_email;"
    mycursor.execute(query)
    return mycursor.fetchall()

def no_of_messages_per_user():
    query = "SELECT users_email, COUNT(message) FROM users_dms WHERE status = 'Scheduled' GROUP BY users_email;"
    mycursor.execute(query)
    return mycursor.fetchall()
     

def log_in(driver, ig_username, ig_password):

    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    username_field.send_keys(ig_username)

    sleep(3)

    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
    password_field.send_keys(ig_password)

    sleep(3)

    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
    login_button.click()

    sleep(15)

def get_instagram_username(recipients_id):
    query = "SELECT username FROM instagram_accounts WHERE id = %s"
    mycursor.execute(query, (recipients_id,))
    result = mycursor.fetchone()
    return result[0] if result else None

def check_username_exists(driver, username):
    insta_url = 'https://www.instagram.com/'
    driver.get(insta_url + username + '/')
    
    try:
        try:
            check_existing_username = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(@class, 'x1lliihq') and contains(@class, 'x1plvlek') and contains(@class, 'xryxfnj') and contains(@class, 'x1n2onr6') and contains(@class, 'x1ji0vk5') and contains(@class, 'x18bv5gf') and contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and contains(@class, 'x1fj9vlw') and contains(@class, 'x13faqbe') and contains(@class, 'x1vvkbs') and contains(@class, 'x1s928wv') and contains(@class, 'xhkezso') and contains(@class, 'x1gmr53x') and contains(@class, 'x1cpjm7i') and contains(@class, 'x1fgarty') and contains(@class, 'x1943h6x') and contains(@class, 'x1i0vuye') and contains(@class, 'x1ms8i2q') and contains(@class, 'xo1l8bm') and contains(@class, 'x5n08af') and contains(@class, 'x10wh9bi') and contains(@class, 'x1wdrske') and contains(@class, 'x8viiok') and contains(@class, 'x18hxmgj')]"))
            )
            if check_existing_username.text == username:
                return True
        except:
            pass  

        try:
            unavailable_page = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'x1lliihq') and contains(@class, 'x1plvlek') and contains(@class, 'xryxfnj') and contains(@class, 'x1n2onr6') and contains(@class, 'x1ji0vk5') and contains(@class, 'x18bv5gf') and contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and contains(@class, 'x1fj9vlw') and contains(@class, 'x13faqbe') and contains(@class, 'x1vvkbs') and contains(@class, 'x1s928wv') and contains(@class, 'xhkezso') and contains(@class, 'x1gmr53x') and contains(@class, 'x1cpjm7i') and contains(@class, 'x1fgarty') and contains(@class, 'x1943h6x') and contains(@class, 'x1i0vuye') and contains(@class, 'x133cpev') and contains(@class, 'x1s688f') and contains(@class, 'x5n08af') and contains(@class, 'x2b8uid') and contains(@class, 'x4zkp8e') and contains(@class, 'x41vudc') and contains(@class, 'x10wh9bi') and contains(@class, 'x1wdrske') and contains(@class, 'x8viiok') and contains(@class, 'x18hxmgj')]"))
            )
            if unavailable_page.text == "Sorry, this page isn't available.":
                return False
        except:
            pass 
        
        return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return -1

def check_if_logged_in(driver):
    try:
        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        return False
    except TimeoutException:
        return True
    
def send_dm(driver, username, message):


    driver.get('https://www.instagram.com/direct/inbox/')

    try:
        turn_off_notifications_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Not Now')]"))
        )
        turn_off_notifications_button.click()
    except:
        pass

    message_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1i10hfl') and contains(@class, 'xjqpnuy') and contains(@class, 'xa49m3k') and contains(@class, 'xqeqjp1') and contains(@class, 'x2hbi6w') and contains(@class, 'x972fbf') and contains(@class, 'xcfux6l') and contains(@class, 'x1qhh985') and contains(@class, 'xm0m39n') and contains(@class, 'xdl72j9') and contains(@class, 'x2lah0s') and contains(@class, 'xe8uvvx') and contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'x2lwn1j') and contains(@class, 'xeuugli') and contains(@class, 'xexx8yu') and contains(@class, 'x18d9i69') and contains(@class, 'x1hl2dhg') and contains(@class, 'xggy1nq') and contains(@class, 'x1ja2u2z') and contains(@class, 'x1t137rt') and contains(@class, 'x1q0g3np') and contains(@class, 'x1lku1pv') and contains(@class, 'x1a2a7pz') and contains(@class, 'x6s0dn4') and contains(@class, 'xjyslct') and contains(@class, 'x1lq5wgf') and contains(@class, 'xgqcy7u') and contains(@class, 'x30kzoy') and contains(@class, 'x9jhf4c') and contains(@class, 'x1ejq31n') and contains(@class, 'xd10rxx') and contains(@class, 'x1sy0etr') and contains(@class, 'x17r0tee') and contains(@class, 'x9f619') and contains(@class, 'x9bdzbf') and contains(@class, 'x1ypdohk') and contains(@class, 'x78zum5') and contains(@class, 'x1f6kntn') and contains(@class, 'xwhw2v2') and contains(@class, 'x10w6t97') and contains(@class, 'xl56j7k') and contains(@class, 'x17ydfre') and contains(@class, 'x1swvt13') and contains(@class, 'x1pi30zi') and contains(@class, 'x1n2onr6') and contains(@class, 'x2b8uid') and contains(@class, 'xlyipyv') and contains(@class, 'x87ps6o') and contains(@class, 'x14atkfc') and contains(@class, 'xcdnw81') and contains(@class, 'x1i0vuye') and contains(@class, 'x1tu34mt') and contains(@class, 'xzloghq') and text()='Send message']")))
    message_button.click()

    sleep(2)

    input_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search')]")))

    input_field.click()
    input_field.send_keys(username)

    sleep(2)

    #ovdje treba nesto dodati da provjeri da li je to taj korisnik na osnovu subtitlea, jer ovi subtitles su isti za sve usere u listi
    #presence of elements located ovdje ne radi, mozda to trebam staviti na cijelu listu

    list_of_names = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'x1lliihq') and contains(@class, 'x1plvlek') and contains(@class, 'xryxfnj') and contains(@class, 'x1n2onr6') and contains(@class, 'x1ji0vk5') and contains(@class, 'x18bv5gf') and contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and contains(@class, 'x1fj9vlw') and contains(@class, 'x13faqbe') and contains(@class, 'x1vvkbs') and contains(@class, 'x1s928wv') and contains(@class, 'xhkezso') and contains(@class, 'x1gmr53x') and contains(@class, 'x1cpjm7i') and contains(@class, 'x1fgarty') and contains(@class, 'x1943h6x') and contains(@class, 'x1i0vuye') and contains(@class, 'xvs91rp') and contains(@class, 'xo1l8bm') and contains(@class, 'x1roi4f4') and contains(@class, 'x10wh9bi') and contains(@class, 'x1wdrske') and contains(@class, 'x8viiok') and contains(@class, 'x18hxmgj')]/span[contains(@class, 'x1lliihq') and contains(@class, 'x193iq5w') and contains(@class, 'x6ikm8r') and contains(@class, 'x10wlt62') and contains(@class, 'xlyipyv') and contains(@class, 'xuxw1ft')]")))
    list_of_names.click()

    sleep(2)

    chat_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1i10hfl') and contains(@class, 'xjqpnuy') and contains(@class, 'xa49m3k') and contains(@class, 'xqeqjp1') and contains(@class, 'x2hbi6w') and contains(@class, 'x972fbf') and contains(@class, 'xcfux6l') and contains(@class, 'x1qhh985') and contains(@class, 'xm0m39n') and contains(@class, 'xdl72j9') and contains(@class, 'x2lah0s') and contains(@class, 'xe8uvvx') and contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'x2lwn1j') and contains(@class, 'xeuugli') and contains(@class, 'xexx8yu') and contains(@class, 'x18d9i69') and contains(@class, 'x1hl2dhg') and contains(@class, 'xggy1nq') and contains(@class, 'x1ja2u2z') and contains(@class, 'x1t137rt') and contains(@class, 'x1q0g3np') and contains(@class, 'x1lku1pv') and contains(@class, 'x1a2a7pz') and contains(@class, 'x6s0dn4') and contains(@class, 'xjyslct') and contains(@class, 'x1lq5wgf') and contains(@class, 'xgqcy7u') and contains(@class, 'x30kzoy') and contains(@class, 'x9jhf4c') and contains(@class, 'x1ejq31n') and contains(@class, 'xd10rxx') and contains(@class, 'x1sy0etr') and contains(@class, 'x17r0tee') and contains(@class, 'x9f619') and contains(@class, 'x9bdzbf') and contains(@class, 'x1ypdohk') and contains(@class, 'x78zum5') and contains(@class, 'x1f6kntn') and contains(@class, 'xwhw2v2') and contains(@class, 'xl56j7k') and contains(@class, 'x17ydfre') and contains(@class, 'x1n2onr6') and contains(@class, 'x2b8uid') and contains(@class, 'xlyipyv') and contains(@class, 'x87ps6o') and contains(@class, 'x14atkfc') and contains(@class, 'xcdnw81') and contains(@class, 'x1i0vuye') and contains(@class, 'xn3w4p2') and contains(@class, 'x5ib6vp') and contains(@class, 'xc73u3c') and contains(@class, 'x1tu34mt') and contains(@class, 'xzloghq') and text()='Chat']")))
    chat_button.click()

    sleep(2)

    message_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'xzsf02u') and contains(@class, 'x1a2a7pz') and contains(@class, 'x1n2onr6') and contains(@class, 'x14wi4xw') and contains(@class, 'x1iyjqo2') and contains(@class, 'x1gh3ibb') and contains(@class, 'xisnujt') and contains(@class, 'xeuugli') and contains(@class, 'x1odjw0f') and contains(@class, 'notranslate') and @aria-label='Message' and @aria-placeholder='Message...' and @role='textbox']")))
    message_field.send_keys(message)

    sleep(2)

    send_message_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1i10hfl') and contains(@class, 'xjqpnuy') and contains(@class, 'xa49m3k') and contains(@class, 'xqeqjp1') and contains(@class, 'x2hbi6w') and contains(@class, 'xdl72j9') and contains(@class, 'x2lah0s') and contains(@class, 'xe8uvvx') and contains(@class, 'xdj266r') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'x2lwn1j') and contains(@class, 'xeuugli') and contains(@class, 'x1hl2dhg') and contains(@class, 'xggy1nq') and contains(@class, 'x1ja2u2z') and contains(@class, 'x1t137rt') and contains(@class, 'x1q0g3np') and contains(@class, 'x1lku1pv') and contains(@class, 'x1a2a7pz') and contains(@class, 'x6s0dn4') and contains(@class, 'xjyslct') and contains(@class, 'x1ejq31n') and contains(@class, 'xd10rxx') and contains(@class, 'x1sy0etr') and contains(@class, 'x17r0tee') and contains(@class, 'x9f619') and contains(@class, 'x1ypdohk') and contains(@class, 'x1f6kntn') and contains(@class, 'xwhw2v2') and contains(@class, 'xl56j7k') and contains(@class, 'x17ydfre') and contains(@class, 'x2b8uid') and contains(@class, 'xlyipyv') and contains(@class, 'x87ps6o') and contains(@class, 'x14atkfc') and contains(@class, 'xcdnw81') and contains(@class, 'x1i0vuye') and contains(@class, 'xjbqb8w') and contains(@class, 'xm3z3ea') and contains(@class, 'x1x8b98j') and contains(@class, 'x131883w') and contains(@class, 'x16mih1h') and contains(@class, 'x972fbf') and contains(@class, 'xcfux6l') and contains(@class, 'x1qhh985') and contains(@class, 'xm0m39n') and contains(@class, 'xt0psk2') and contains(@class, 'xt7dq6l') and contains(@class, 'xexx8yu') and contains(@class, 'x4uap5') and contains(@class, 'x18d9i69') and contains(@class, 'xkhd6sd') and contains(@class, 'x1n2onr6') and contains(@class, 'x1n5bzlp') and contains(@class, 'x173jzuc') and contains(@class, 'x1yc6y37') and contains(@class, 'xfs2ol5') and text()='Send' and @role='button']")))
    send_message_button.click()

    return True



def send_bulk_dms(sender):
    service1 = Service(ChromeDriverManager().install())  
    options1 = Options()
    options1.add_argument(f'--remote-debugging-port={sender["port"]}')
    options1.add_argument(f'--user-data-dir=/Users/ajlakorman/selenium/ChromeProfile{sender["port"]}')

    driver = webdriver.Chrome(service=service1, options=options1)
    driver.maximize_window()

    insta_url = 'https://www.instagram.com/'
    driver.get(insta_url)

    sleep(3)

    check_login_results = check_if_logged_in(driver)

    if check_login_results == False:
        log_in(driver, sender["sender"], sender["password"])

    sleep(3)

    successfully_sent_messages = []

    for message in sender["messages"]:
        recipient_username = message[0]
        message_text = message[1]
        message_id = message[2]

        check_username_exists_result = check_username_exists(driver, recipient_username)

        if not check_username_exists(driver, recipient_username):
            print(f"Recipient {recipient_username} does not exist. Skipping.")
            continue

        if send_dm(driver, recipient_username, message_text):
            successfully_sent_messages.append(message_id)  
        else:
            print(f"Failed to send message to {recipient_username}.")

    driver.quit()
    return successfully_sent_messages

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1
    
def change_message_status_to_sent(message_ids):
    if not message_ids:
        print("No messages to update. Skipping status update.")
        return

    id_list_str = ','.join(map(str, message_ids))
    query = f"UPDATE users_dms SET status = 'Sent' WHERE id IN ({id_list_str})"
    print(f"Executing query: {query}")
    mycursor.execute(query)
    print(f"Message statuses updated to 'Sent' for IDs: {message_ids}")


def main():

    messages = get_scheduled_messages()
    messages= tuple(messages)

    dms_to_send = []

    for message in messages:
        if not any(d['sender'] == message[0] for d in dms_to_send):
            dms_to_send.append({
                "sender" : message[0],
                "password" : message[1],
                "port" : message[4],
                "messages" : [(message[2], message[3], message[5])]
            })
        else:
            index = find(dms_to_send, "sender", message[0])
            dms_to_send[index]["messages"].append((message[2], message[3], message[5]))
        print(message)

    threads = []

    all_successfully_sent_messages = []

    for sender in dms_to_send:
        thread = threading.Thread(target=lambda s=sender: all_successfully_sent_messages.extend(send_bulk_dms(s)))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print(f"All successfully sent messages: {all_successfully_sent_messages}")
    change_message_status_to_sent(all_successfully_sent_messages)



if __name__ == "__main__":

    main()
