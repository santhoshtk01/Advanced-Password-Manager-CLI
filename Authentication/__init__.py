import sqlite3

cursor = None
connection = None


# Function to create the initial schema of the Database
def createSchema() -> None:
    """Create the initial schema of the Database if exist already."""
    query = (
        "CREATE TABLE IF NOT EXISTS "
        "userCredentials(userId INTEGER PRIMARY KEY,"
        "username VARCHAR(20) UNIQUE,"
        "gmail VARCHAR NOT NULL, "
        "password BLOB NOT NULL,"
        "totpURL TEXT NOT NULL DEFAULT 'null');"
    )
    cursor.execute(query)
    print("Initial schema created successfully..")


def establishConnection() -> sqlite3.Cursor:
    global cursor, connection
    # TODO : Setup logging if DB not connected.
    # Connect with the Database and handle the exception if occurs.

    if cursor is None:
        try:
            connection = sqlite3.connect("/home/santhoshtk/Music/Advanced-Password-Manager-CLI/Authentication/users.db")
            print("Database connection successful..")
            cursor = connection.cursor()
            createSchema()
        except Exception as error:
            print(error)

    return cursor


# Function to commit the changes to the Database.
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