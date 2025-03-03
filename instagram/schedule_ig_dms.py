import mysql.connector
from dotenv import load_dotenv



load_dotenv("../.env")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MySQLdatabasepass123!",
    database="sdp_project"
)

mydb.autocommit = True

mycursor = mydb.cursor()

def schedule_instagram_messages():
    query = "SET SQL_SAFE_UPDATES = 0; "
    mycursor.execute(query)

    query = "UPDATE users_dms SET status =  'Scheduled'"
    mycursor.execute(query)

    query = "SELECT * FROM users_dms"
    mycursor.execute(query)
    result = mycursor.fetchall()
    return result


    
def main():

    print(schedule_instagram_messages())
    print("Instagram DMs status successfully set to Scheduled.")

if __name__ == "__main__":

    main()
