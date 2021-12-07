import mysql.connector
from mysql.connector import Error
import os



def create_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv("AWS_TC_DB_MYSQL_HN"),
            user= os.getenv("AWS_TC_DB_MYSQL_UN"),
            passwd=os.getenv("AWS_TC_DB_MYSQL_PW")

        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


"""connection = create_connection("localhost", "root", "")"""