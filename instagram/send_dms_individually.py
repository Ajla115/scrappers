import mysql.connector
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert

load_dotenv("../.env")

# Connecting to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQLdatabasepass123!",
    database="sdp_project"
)

mycursor = mydb.cursor()

account_username = os.getenv("IGUSERNAME")
account_password = os.getenv("IGPASSWORD")

def instagram_driver(username, message):

    service1 = Service(ChromeDriverManager().install())  
    options1 = Options()
    options1.add_argument(f'--remote-debugging-port=9227')
    options1.add_argument(f'--user-data-dir=/Users/ajlakorman/selenium/ChromeProfile9227')

    driver = webdriver.Chrome(service=service1, options=options1)
    driver.maximize_window()
   
    driver.get('https://www.instagram.com/')

    print("Is user logged in? ", check_if_logged_in(driver))

    if check_if_logged_in(driver) == False:
        log_in(driver, account_username, account_password)

    #if the username does not exist, just exit
    if  check_username_exists(driver, username) != True:
            print("Username does not exist. Exiting...")
            return False
    
    
    #if username exists, send a DM to it
    print("Username exists. Proceeding with further action.")

    send_dm(driver, username, "Automated message")

    sleep(5)

    driver.quit()

def log_in(driver, ig_username, ig_password):

        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        username_field.send_keys(ig_username)

        sleep(2)

        password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
        password_field.send_keys(ig_password)

        sleep(2)

        login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
        login_button.click()

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

    sleep(7)
    #pada ovdje
    # input_field = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'x5ur3kl') and contains(@class, 'xopu45v') and contains(@class, 'x1bs97v6') and contains(@class, 'xmo9t06') and contains(@class, 'x1j8ye7u') and contains(@class, 'x1rjkts5') and contains(@class, 'x13z9klp') and contains(@class, 'xjc6cxp') and contains(@class, 'x178xt8z') and contains(@class, 'xm81vs4') and contains(@class, 'xso031l') and contains(@class, 'xy80clv') and contains(@class, 'x5n08af') and contains(@class, 'x1iyjqo2') and contains(@class, 'xvs91rp') and contains(@class, 'xklk4pu') and contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'x1plvlek') and contains(@class, 'xryxfnj') and contains(@class, 'x1iorvi4') and contains(@class, 'xn6708d') and contains(@class, 'xjkvuk6') and contains(@class, 'x1s3xk63') and contains(@class, 'xlqc9nw') and contains(@class, 'x8tigb1') and contains(@class, 'x1ad04t7') and contains(@class, 'x1glnyev') and contains(@class, 'xs3hnx8') and contains(@class, 'x7xwk5j') and contains(@class, 'x1rheh84') and contains(@class, 'x1ck6gwh') and contains(@class, 'x175bfct') and contains(@class, 'x1meze4m') and contains(@class, 'x10eltez') and contains(@class, 'x1qt4tve') and contains(@class, 'x1s07b3s') and contains(@class, 'xkq2eht') and contains(@class, 'x1rvh84u') and contains(@class, 'x1ejq31n') and contains(@class, 'xd10rxx') and contains(@class, 'x1sy0etr') and contains(@class, 'x17r0tee') and contains(@class, 'x5ib6vp') and contains(@class, 'xjbqb8w') and contains(@class, 'xzd0ubt')]"))
    # )
    input_field = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Search')]"))
)
    input_field.click()
    input_field.send_keys(username)

    sleep(5)
    #ovdje treba nesto dodati da provjeri da li je to taj korisnik na osnovu subtitlea, jer ovi subtitles su isti za sve usere u listi
    #presence of elements located ovdje ne radi, mozda to trebam staviti na cijelu listu
    list_of_names = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'x1lliihq') and contains(@class, 'x1plvlek') and contains(@class, 'xryxfnj') and contains(@class, 'x1n2onr6') and contains(@class, 'x1ji0vk5') and contains(@class, 'x18bv5gf') and contains(@class, 'x193iq5w') and contains(@class, 'xeuugli') and contains(@class, 'x1fj9vlw') and contains(@class, 'x13faqbe') and contains(@class, 'x1vvkbs') and contains(@class, 'x1s928wv') and contains(@class, 'xhkezso') and contains(@class, 'x1gmr53x') and contains(@class, 'x1cpjm7i') and contains(@class, 'x1fgarty') and contains(@class, 'x1943h6x') and contains(@class, 'x1i0vuye') and contains(@class, 'xvs91rp') and contains(@class, 'xo1l8bm') and contains(@class, 'x1roi4f4') and contains(@class, 'x10wh9bi') and contains(@class, 'x1wdrske') and contains(@class, 'x8viiok') and contains(@class, 'x18hxmgj')]/span[contains(@class, 'x1lliihq') and contains(@class, 'x193iq5w') and contains(@class, 'x6ikm8r') and contains(@class, 'x10wlt62') and contains(@class, 'xlyipyv') and contains(@class, 'xuxw1ft')]")))
    print(list_of_names.text)
    list_of_names.click()

    sleep(5)

    chat_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1i10hfl') and contains(@class, 'xjqpnuy') and contains(@class, 'xa49m3k') and contains(@class, 'xqeqjp1') and contains(@class, 'x2hbi6w') and contains(@class, 'x972fbf') and contains(@class, 'xcfux6l') and contains(@class, 'x1qhh985') and contains(@class, 'xm0m39n') and contains(@class, 'xdl72j9') and contains(@class, 'x2lah0s') and contains(@class, 'xe8uvvx') and contains(@class, 'xdj266r') and contains(@class, 'x11i5rnm') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'x2lwn1j') and contains(@class, 'xeuugli') and contains(@class, 'xexx8yu') and contains(@class, 'x18d9i69') and contains(@class, 'x1hl2dhg') and contains(@class, 'xggy1nq') and contains(@class, 'x1ja2u2z') and contains(@class, 'x1t137rt') and contains(@class, 'x1q0g3np') and contains(@class, 'x1lku1pv') and contains(@class, 'x1a2a7pz') and contains(@class, 'x6s0dn4') and contains(@class, 'xjyslct') and contains(@class, 'x1lq5wgf') and contains(@class, 'xgqcy7u') and contains(@class, 'x30kzoy') and contains(@class, 'x9jhf4c') and contains(@class, 'x1ejq31n') and contains(@class, 'xd10rxx') and contains(@class, 'x1sy0etr') and contains(@class, 'x17r0tee') and contains(@class, 'x9f619') and contains(@class, 'x9bdzbf') and contains(@class, 'x1ypdohk') and contains(@class, 'x78zum5') and contains(@class, 'x1f6kntn') and contains(@class, 'xwhw2v2') and contains(@class, 'xl56j7k') and contains(@class, 'x17ydfre') and contains(@class, 'x1n2onr6') and contains(@class, 'x2b8uid') and contains(@class, 'xlyipyv') and contains(@class, 'x87ps6o') and contains(@class, 'x14atkfc') and contains(@class, 'xcdnw81') and contains(@class, 'x1i0vuye') and contains(@class, 'xn3w4p2') and contains(@class, 'x5ib6vp') and contains(@class, 'xc73u3c') and contains(@class, 'x1tu34mt') and contains(@class, 'xzloghq') and text()='Chat']")))
    chat_button.click()

    sleep(7)

    message_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'xzsf02u') and contains(@class, 'x1a2a7pz') and contains(@class, 'x1n2onr6') and contains(@class, 'x14wi4xw') and contains(@class, 'x1iyjqo2') and contains(@class, 'x1gh3ibb') and contains(@class, 'xisnujt') and contains(@class, 'xeuugli') and contains(@class, 'x1odjw0f') and contains(@class, 'notranslate') and @aria-label='Message' and @aria-placeholder='Message...' and @role='textbox']")))
    message_field.send_keys(message)

    sleep(7)

    send_message_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x1i10hfl') and contains(@class, 'xjqpnuy') and contains(@class, 'xa49m3k') and contains(@class, 'xqeqjp1') and contains(@class, 'x2hbi6w') and contains(@class, 'xdl72j9') and contains(@class, 'x2lah0s') and contains(@class, 'xe8uvvx') and contains(@class, 'xdj266r') and contains(@class, 'xat24cr') and contains(@class, 'x1mh8g0r') and contains(@class, 'x2lwn1j') and contains(@class, 'xeuugli') and contains(@class, 'x1hl2dhg') and contains(@class, 'xggy1nq') and contains(@class, 'x1ja2u2z') and contains(@class, 'x1t137rt') and contains(@class, 'x1q0g3np') and contains(@class, 'x1lku1pv') and contains(@class, 'x1a2a7pz') and contains(@class, 'x6s0dn4') and contains(@class, 'xjyslct') and contains(@class, 'x1ejq31n') and contains(@class, 'xd10rxx') and contains(@class, 'x1sy0etr') and contains(@class, 'x17r0tee') and contains(@class, 'x9f619') and contains(@class, 'x1ypdohk') and contains(@class, 'x1f6kntn') and contains(@class, 'xwhw2v2') and contains(@class, 'xl56j7k') and contains(@class, 'x17ydfre') and contains(@class, 'x2b8uid') and contains(@class, 'xlyipyv') and contains(@class, 'x87ps6o') and contains(@class, 'x14atkfc') and contains(@class, 'xcdnw81') and contains(@class, 'x1i0vuye') and contains(@class, 'xjbqb8w') and contains(@class, 'xm3z3ea') and contains(@class, 'x1x8b98j') and contains(@class, 'x131883w') and contains(@class, 'x16mih1h') and contains(@class, 'x972fbf') and contains(@class, 'xcfux6l') and contains(@class, 'x1qhh985') and contains(@class, 'xm0m39n') and contains(@class, 'xt0psk2') and contains(@class, 'xt7dq6l') and contains(@class, 'xexx8yu') and contains(@class, 'x4uap5') and contains(@class, 'x18d9i69') and contains(@class, 'xkhd6sd') and contains(@class, 'x1n2onr6') and contains(@class, 'x1n5bzlp') and contains(@class, 'x173jzuc') and contains(@class, 'x1yc6y37') and contains(@class, 'xfs2ol5') and text()='Send' and @role='button']")))
    send_message_button.click()



def main():

    username = input("Enter username: ")
    message = input("Enter message: ")
    instagram_driver(username, message)

if __name__ == "__main__":

    main()
