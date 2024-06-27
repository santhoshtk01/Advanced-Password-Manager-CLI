import sqlite3

DBPATH = "/home/santhoshtk/Music/Advanced-Password-Manager-CLI/Manager/userPasswords.db"

cursor = None
connection = None


def createSchema():
    # Query for passwords table.
    query = (
        "CREATE TABLE IF NOT EXISTS passwords("
        "password_id INTEGER PRIMARY KEY,"
        "website_name TEXT,"
        "username TEXT,"
        "password BLOB NOT NULL,"
        "description VARCHAR(150),"
        "url TEXT,"
        "breached INTEGER NOT NULL DEFAULT 0,"
        "userId INTEGER);"
    )
    cursor.execute(query)

    # Query to maintain authenticated users.
    query = (
        "CREATE TABLE IF NOT EXISTS loggedInUsers("
        "userId INTEGER PRIMARY KEY,"
        "username TEXT NOT NULL,"
        "authenticated INTEGER NOT NULL DEFAULT 0,"
        "encryptionKey BLOB NOT NULL);"
    )
    cursor.execute(query)

    # Query for password change history table.
    query = (
        "CREATE TABLE IF NOT EXISTS changeHistory("
        "change_id INTEGER PRIMARY KEY,"
        "password_id INTEGER NOT NULL,"
        "date_changed TEXT NOT NULL,"
        "password BLOB NOT NULL,"
        "FOREIGN KEY(password_id) REFERENCES passwords(password_id));"
    )
    cursor.execute(query)


def establishConnection() -> sqlite3.Cursor:
    global cursor, connection

    if cursor is None:
        # Establish a new connection with the Database
        try:
            connection = sqlite3.connect(DBPATH, check_same_thread=False)
            cursor = connection.cursor()
            createSchema()
        except Exception as error:
            print(error)

    return cursor


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


establishConnection()
