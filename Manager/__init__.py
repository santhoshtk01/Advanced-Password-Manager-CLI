import sqlite3

cursor = None


def createSchema():

    # Query for passwords table.
    query = (
        "CREATE TABLE IF NOT EXISTS passwords("
         "password_id INTEGER PRIMARY KEY,"
         "website_name TEXT,"
         "username TEXT,"
         "password BLOB,"
         "description VARCHAR(150),"
         "url TEXT,"
         "auto_logout_time DATETIME,"
         "authenticated BOOLEAN,"
        "userId INTEGER);"
    )
    cursor.execute(query)

    # Query for password change history table.
    query = (
        "CREATE TABLE IF NOT EXISTS changeHistory("
         "change_id INTEGER PRIMARY KEY,"
         "password_id INTEGER NOT NULL,"
         "date_changed DATE NOT NULL,"
         "password TEXT,"
        "FOREIGN KEY(password_id) REFERENCES passwords(password_id));"
    )
    cursor.execute(query)


# Establish a new connection with the Database
try:
    connection = sqlite3.connect("userPasswords.db")
    cursor = connection.cursor()
    createSchema()
except Exception as error:
    print(error)


def commit(closeConnection: bool = False) -> None:
    """
    Commit the changes made to the database permanently.
    Args:
        closeConnection: Indicated whether to close the connection or not.
    """
    connection.commit()

    # Close the connection if `closeConnection` := True
    if closeConnection:
        connection.close()
