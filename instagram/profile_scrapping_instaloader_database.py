import instaloader
import time
import logging
import mysql.connector
from datetime import date
from instaloader.exceptions import ProfileNotExistsException, ConnectionException

# Creating an instance of the Instaloader class
# quiet=True means when bot encounters error 401 or 404, it wont repeat behaviour

bot = instaloader.Instaloader(quiet=True)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQLdatabasepass123!",
    database="sdp_project"
)

def checkExistence(username):
    sql_query1 = "SELECT * FROM instagram_accounts WHERE username = %s"
    values = (username,)
    mycursor = mydb.cursor()
    mycursor.execute(sql_query1, values)
    result = mycursor.fetchone()
    return result is not None

def updateUser(username, stats):
    if not checkExistence(username):
        sql_query2 = "INSERT INTO instagram_accounts (username, stats, activity) VALUES (%s, %s, 'active')"
        values = (username, stats)
        message = f"Added new user: {username}"
    else:
        sql_query2 = "UPDATE instagram_accounts SET stats = %s WHERE username = %s"
        values = (stats, username)
        message = f"Updated user: {username}"
    print(message)
    mycursor = mydb.cursor()
    mycursor.execute(sql_query2, values)
    mydb.commit()

def scrapeData(username):
    current_date = date.today()
    try:
        profile = instaloader.Profile.from_username(bot.context, username)
        posts = profile.mediacount
        followers = profile.followers
        followings = profile.followees
        updateExistingUser(posts, followers, followings, username, current_date)
    except ProfileNotExistsException:
        setInvalidUser(username, current_date)
        print(f"Invalid username: {username}")
    except ConnectionException as e:
        setInvalidUser(username, current_date)
        print(f"Connection issue while accessing username '{username}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred for username '{username}': {e}")

def setInvalidUser(username, current_date):
    sql_query3 = "UPDATE instagram_accounts SET post_number = 0, followers_number = 0, followings_number = 0, date_and_time = %s, stats = 1, activity = %s WHERE username = %s"
    values = ( current_date,"Invalid Username", username)
    mycursor = mydb.cursor()
    mycursor.execute(sql_query3, values)
    mydb.commit()    
    print(f"Invalid username: {username}")


def updateExistingUser(posts, followers, following, username, current_date):
    sql_query3 = "UPDATE instagram_accounts SET post_number = %s, followers_number = %s, followings_number = %s, date_and_time = %s, stats = 1 WHERE username = %s"
    values = (posts, followers, following, current_date, username)
    mycursor = mydb.cursor()
    mycursor.execute(sql_query3, values)
    mydb.commit()
    print(f"Updated user: {username}")

def fetchUsernameDataFromDB():
    sql_query = "SELECT username, activity, stats FROM instagram_accounts"
    with mydb.cursor() as mycursor:
        mycursor.execute(sql_query)
        rows = mycursor.fetchall()
        return rows

def main():
    usernames_stats = fetchUsernameDataFromDB()
    #this count variable will be used create sleeps that mimic human behavior
    count = 0
  
    for username, activity, stats in usernames_stats:
        #this way it only checks for usernames whose activity status is not deleted
        if activity != 'deleted' or activity != 'Invalid username': 
            #These are random sleeps, to mimic human behavior
            if count > 0:
                if count % 35 == 0:  
                    time.sleep(9)  
                elif count % 5 == 0:
                    time.sleep(5)
                elif count % 7 == 0:
                    time.sleep(7)


            if stats == 1:
                updateUser(username, stats)
            elif stats == 0 or stats == None:
                scrapeData(username)
            else:
                print(f"Skipping username '{username}' due to unrecognized stats value: {stats}")


            time.sleep(3)
            #wait three seconds before moving on to the next username
            count += 1

    print("All records have been succesfully updated.")

if __name__ == '__main__':
    main()

