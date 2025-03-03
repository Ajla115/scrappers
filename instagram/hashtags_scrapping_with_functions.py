import mysql.connector
from time import sleep
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

load_dotenv("../.env")
ig_account_username = os.getenv("IGUSERNAME")
ig_account_password = os.getenv("IGPASSWORD")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQLdatabasepass123!",
    database="sdp_project"
)

#Autocommit is set to True, so everything will get autocomitted by default
mydb.autocommit = True
mycursor = mydb.cursor()

def addAccountsAndHashtagsToCombinedTable(hashtag, extracted_usernames):
    # Fetch the hashtag id
    sql = "SELECT id FROM instagram_hashtags WHERE hashtag_name = %s"
    val = (hashtag,)
    mycursor.execute(sql, val)
    hashtag_id = mycursor.fetchone()[0]  # Extracting the ID from the tuple

    # Fetch the username ids
    username_ids = []
    for username in extracted_usernames:
        sql = "SELECT id FROM instagram_accounts WHERE username = %s"
        val = (username,)
        mycursor.execute(sql, val)
        username_id = mycursor.fetchone()
        if username_id:  # Only append if the username exists
            username_ids.append(username_id[0])  # Extracting the ID from the tuple

    # Check existing pairs in accounts_with_hashtags table
    mycursor.execute("SELECT account_id, hashtag_id FROM accounts_with_hashtag")
    existing_pairs = mycursor.fetchall()

    # Inserting into accounts_with_hashtags table
    for username_id in username_ids:
        if (username_id, hashtag_id) not in existing_pairs:
            sql = "INSERT INTO accounts_with_hashtag (account_id, hashtag_id) VALUES (%s, %s)"
            val = (username_id, hashtag_id)
            mycursor.execute(sql, val)
            mydb.commit()

    print("Accounts and hashtags added to the combined table.")

# Function to add usernames to the database
def addUsernamesToTheDatabase(extracted_usernames):
    for username in extracted_usernames:
        sql = "SELECT id FROM instagram_accounts WHERE username = %s"
        val = (username,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()

        if not result:
            sql = "INSERT INTO instagram_accounts (username, stats, activity) VALUES (%s, 0, 'active')"
            val = (username, )
            mycursor.execute(sql, val)
            mydb.commit()

    print("Usernames added to the database.")

def addHashtagToTheDatabase(hashtag):
    # Check if the hashtag exists and is not marked as deleted
    sql = "SELECT * FROM instagram_hashtags WHERE hashtag_name = %s AND activity != 'deleted'"
    val = (hashtag,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    if not result:
        # Check if the hashtag exists but is marked as deleted
        sql = "SELECT * FROM instagram_hashtags WHERE hashtag_name = %s"
        mycursor.execute(sql, val)
        result_deleted = mycursor.fetchone()
        
        if result_deleted:
            # Update the record if it exists but is marked as deleted
            sql = "UPDATE instagram_hashtags SET activity = 'active' WHERE hashtag_name = %s"
            print(f"Hashtag '{hashtag}' was marked as deleted and has now been reactivated.")
        else:
            # Insert the new hashtag into the database
            sql = "INSERT INTO instagram_hashtags (hashtag_name, activity) VALUES (%s, 'active')"
            print(f"Hashtag '{hashtag}' added to the database.")

        mycursor.execute(sql, val)
        mydb.commit()

    else:
        print(f"Hashtag '{hashtag}' already exists in the database and is active.")

def searchHashtag(driver, hashtag):
    hashtags_url = 'https://www.instagram.com/explore/tags/'
    driver.get(hashtags_url + hashtag) # --> accessing specific hashtag page

    #ovo je sad ako hashtag ne postoji na ig
    try:
        no_result_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 
        "//span[contains(@class, 'x1lliihq') and "
        "contains(@class, 'x1plvlek') and "
        "contains(@class, 'xryxfnj') and "
        "contains(@class, 'x1n2onr6') and "
        "contains(@class, 'x1ji0vk5') and "
        "contains(@class, 'x18bv5gf') and "
        "contains(@class, 'x193iq5w') and "
        "contains(@class, 'xeuugli') and "
        "contains(@class, 'x1fj9vlw') and "
        "contains(@class, 'x13faqbe') and "
        "contains(@class, 'x1vvkbs') and "
        "contains(@class, 'x1s928wv') and "
        "contains(@class, 'xhkezso') and "
        "contains(@class, 'x1gmr53x') and "
        "contains(@class, 'x1cpjm7i') and "
        "contains(@class, 'x1fgarty') and "
        "contains(@class, 'x1943h6x') and "
        "contains(@class, 'x1i0vuye') and "
        "contains(@class, 'x1ms8i2q') and "
        "contains(@class, 'xo1l8bm') and "
        "contains(@class, 'x5n08af') and "
        "contains(@class, 'x2b8uid') and "
        "contains(@class, 'x4zkp8e') and "
        "contains(@class, 'xw06pyt') and "
        "contains(@class, 'x10wh9bi') and "
        "contains(@class, 'x1wdrske') and "
        "contains(@class, 'x8viiok') and "
        "contains(@class, 'x18hxmgj') and "
        "text()='No results']")))

        if no_result_text.text == "No results":
            print("No results for the hashtag.")
            driver.quit()
            return
    
    except Exception as e: 
        pass

    addHashtagToTheDatabase(hashtag)

    extracted_usernames = []
    sleep(5)

    picture1 = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, (
            "//div[contains(@class, '_aagw')]"
        ))
    )
)
    picture1.click()

    sleep(3)
    for i in range(3):
        sleep(5)
        #repeat the whole process 3 times, so that we ge ten most recent usernames under each hashtag
        username_prompt = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 
        "//a[contains(@class, 'x1i10hfl') and "
        "contains(@class, 'xjqpnuy') and "
        "contains(@class, 'xa49m3k') and "
        "contains(@class, 'xqeqjp1') and "
        "contains(@class, 'x2hbi6w') and "
        "contains(@class, 'xdl72j9') and "
        "contains(@class, 'x2lah0s') and "
        "contains(@class, 'xe8uvvx') and "
        "contains(@class, 'xdj266r') and "
        "contains(@class, 'x11i5rnm') and "
        "contains(@class, 'xat24cr') and "
        "contains(@class, 'x1mh8g0r') and "
        "contains(@class, 'x2lwn1j') and "
        "contains(@class, 'xeuugli') and "
        "contains(@class, 'x1hl2dhg') and "
        "contains(@class, 'xggy1nq') and "
        "contains(@class, 'x1ja2u2z') and "
        "contains(@class, 'x1t137rt') and "
        "contains(@class, 'x1q0g3np') and "
        "contains(@class, 'x1lku1pv') and "
        "contains(@class, 'x1a2a7pz') and "
        "contains(@class, 'x6s0dn4') and "
        "contains(@class, 'xjyslct') and "
        "contains(@class, 'x1ejq31n') and "
        "contains(@class, 'xd10rxx') and "
        "contains(@class, 'x1sy0etr') and "
        "contains(@class, 'x17r0tee') and "
        "contains(@class, 'x9f619') and "
        "contains(@class, 'x1ypdohk') and "
        "contains(@class, 'x1f6kntn') and "
        "contains(@class, 'xwhw2v2') and "
        "contains(@class, 'xl56j7k') and "
        "contains(@class, 'x17ydfre') and "
        "contains(@class, 'x2b8uid') and "
        "contains(@class, 'xlyipyv') and "
        "contains(@class, 'x87ps6o') and "
        "contains(@class, 'x14atkfc') and "
        "contains(@class, 'xcdnw81') and "
        "contains(@class, 'x1i0vuye') and "
        "contains(@class, 'xjbqb8w') and "
        "contains(@class, 'xm3z3ea') and "
        "contains(@class, 'x1x8b98j') and "
        "contains(@class, 'x131883w') and "
        "contains(@class, 'x16mih1h') and "
        "contains(@class, 'x972fbf') and "
        "contains(@class, 'xcfux6l') and "
        "contains(@class, 'x1qhh985') and "
        "contains(@class, 'xm0m39n') and "
        "contains(@class, 'xt0psk2') and "
        "contains(@class, 'xt7dq6l') and "
        "contains(@class, 'xexx8yu') and "
        "contains(@class, 'x4uap5') and "
        "contains(@class, 'x18d9i69') and "
        "contains(@class, 'xkhd6sd') and "
        "contains(@class, 'x1n2onr6') and "
        "contains(@class, 'x1n5bzlp') and "
        "contains(@class, 'xqnirrm') and "
        "contains(@class, 'xj34u2y') and "
        "contains(@class, 'x568u83') and "
        "@role='link' and "
        "@tabindex='0']" )))

        link_to_username = username_prompt.get_attribute('href') 
        #here, it prints it in the form of https://www.instagram.com/team_falchetta_/
        #the first 25 characters are the ig url, and I will just slice or slip that so I will use just the actual name

        actual_username = link_to_username.split('/')

        extracted_usernames.append(actual_username[3])
        #this just gives me the actual username 

        sleep(5)
        # next_arrow_button =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[12]/div[1]/div/div[3]/div/div/div/div/div[1]/div/div/div/button")))
        # next_arrow_button.click()
        actions = ActionChains(driver)
        actions.send_keys(Keys.RIGHT).perform()
        sleep(5)

    addUsernamesToTheDatabase(extracted_usernames)

    addAccountsAndHashtagsToCombinedTable(hashtag, extracted_usernames)

def check_if_logged_in(driver):
    try:
        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        print("User is not logged in, so first we need to log in.")
        return False
    except TimeoutException:
        print("User is logged in, so we will skip the login process.")
        return True

def log_in(driver):
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    username_field.send_keys(ig_account_username)

    sleep(3)

    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
    password_field.send_keys(ig_account_password)

    sleep(3)

    login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
    login_button.click()

    sleep(15) 

def hashtag_driver(hashtag):
    service1 = Service(ChromeDriverManager().install())  
    options1 = Options()
    options1.add_argument(f'--remote-debugging-port=9222')
    options1.add_argument(f'--user-data-dir=/Users/ajlakorman/selenium/ChromeProfile9222')

    driver = webdriver.Chrome(service=service1, options=options1)
    driver.maximize_window()

    insta_url = 'https://www.instagram.com/'
    driver.get(insta_url)

    sleep(3)

    check_login_results = check_if_logged_in(driver)

    if check_login_results == False:
        log_in(driver)

    sleep(3)

    searchHashtag(driver, hashtag)

def main(): 
    hashtag = input("Enter desired hashtag you want to search for: ") 
    hashtag_driver(hashtag)

if __name__ == '__main__':
    main()