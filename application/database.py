import sqlite3
from datetime import datetime
from .habit import Habit

def create_connection(name="main.db") -> sqlite3.Connection:
    """This function creates the database for the overall application with the library sqlite3.

    Args:
        name (str, optional): Name of the Database. Defaults to "main.db".

    Returns:
        sqlite3.Connection: Connection to the Database
    """

    # create a new database if not exists and open a database connection:
    db = sqlite3.connect(name)

    # call the create_tables function to create tables:
    create_tables(db)

    # return the database:
    return db


def create_tables(db: sqlite3.Connection) -> None:
    """This function creates the individual tables inside the connected sqlite3-database.

    Args:
        db (sqlite3.Connection): Connection to Database
    """

    # create a cursor:
    cur = db.cursor()

    # create table of habits:
    cur.execute(
        """CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        periodicity TEXT,
        description TEXT,
        created TEXT,
        UNIQUE(id))"""
    )

    # create table of habit log:
    cur.execute(
        """CREATE TABLE IF NOT EXISTS habit_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        habit_name TEXT,
        checkoff TEXT,
        UNIQUE(log_id),
        FOREIGN KEY (habit_id) REFERENCES habits(id))"""
    )
    db.commit()


def get_all_habits(db: sqlite3.Connection) -> list:
    """A function to load all data from the connected database.

    Args:
        db (sqlite3.Connection): Connection to Database

    Returns:
        list: List with all content of the habit table as tuple [(id, name, periodicity, description, created)]
    """

    cur = db.cursor()
    cur.execute("SELECT * FROM habits")
    return cur.fetchall()


def get_all_habit_name_and_id(db: sqlite3.Connection) -> list:
    """This function returns a list with all habit_names and habit_ids that are stored in the current connected database.

    Args:
        db (sqlite3.Connection): Connection to Database

    Returns:
        list: List of lists with name and id from connected database [[id, name]]
    """
    cur = db.cursor()
    cur.execute("SELECT id, name FROM habits")
    res = cur.fetchall()
    return [list(idx) for idx in res]


def get_habits_same_periods(db: sqlite3.Connection, periodicity: str) -> list:
    """Returns habit_names, habit_descriptions and created_time of all habits with requested periodicity.

    Args:
        db (sqlite3.Connection): Connection to Database
        periodicity (str): Periodicity inside the database as string

    Returns:
        list: Returns name, description and created of all habits with argument periodicity in [(name, description, created)].
    """
    cur = db.cursor()
    cur.execute(
        "SELECT name, description, created FROM habits WHERE periodicity=?",
        [periodicity])
    return cur.fetchall()


def get_habit_name(db: sqlite3.Connection, habit_id: int) -> str:
    """This function returns a single habit_name, when only the habid_id is known. The name is retrieved from the connected Database.

    Args:
        db (sqlite3.Connection): Connection to Database
        habit_id (int): id of the Habit inside the Database as int

    Returns:
        str: Name of a single habit as string
    """
    cur = db.cursor()
    cur.execute("SELECT name FROM habits WHERE id=?", [habit_id])
    return cur.fetchone()[0]


def get_periods(db: sqlite3.Connection, habit_id: int) -> str:
    """Function to recieve the periodicity of a individual habit from the database.

    Args:
        db (sqlite3.Connection): Connection to Database
        habit_id (int): id of the Habit inside the Database as int

    Returns:
        str: periodicity as string
    """
    cur = db.cursor()
    cur.execute("SELECT periodicity from habits WHERE id=?", [habit_id])
    return cur.fetchone()[0]


def get_all_log_data(db: sqlite3.Connection, habit_id: int) -> list:
    """Returns all stored habit_logs with selected habid_id from the connected database.

    Args:
        db (sqlite3.Connection): Connection to Database
        habit_id (int): id of the Habit inside the Database as int

    Returns:
        list: List of all habit_log data as tuples [(log_id, habit_id, habit_name, checkoff)]
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habit_log WHERE habit_id=?", [habit_id])
    return cur.fetchall()



def default_habit_data(db: sqlite3.Connection) -> None:
    """This function creates default habit data if the user intends to.

    Args:
        db (sqlite3.Connection): Connected Database
    """

    # Create default habits:
    test_habit_study = Habit(db, habit_name="Study", habit_periodicity="daily", habit_description="Study for University", habit_created=datetime.fromtimestamp(1636585200))
    test_habit_sleep = Habit(db, habit_name="Sleep more than 8 hours", habit_periodicity="daily", habit_description="", habit_created=datetime.fromtimestamp(1636585200))
    test_habit_clean = Habit(db, habit_name="Cleaning Coffee Machine", habit_periodicity="weekly", habit_description="", habit_created=datetime.fromtimestamp(1636585200))
    test_habit_workout = Habit(db, habit_name="Work Out", habit_periodicity="weekly", habit_description="Functional Fitness", habit_created=datetime.fromtimestamp(1636585200))
    test_habit_family = Habit(db, habit_name="Visit Family", habit_periodicity="monthly", habit_description="", habit_created=datetime.fromtimestamp(1636585200))

    # save habit data to database:
    test_habit_study.save()
    test_habit_sleep.save()
    test_habit_clean.save()
    test_habit_workout.save()
    test_habit_family.save()

    # connect cursor to database:
    cur = db.cursor()

    # creating default log_data:
    default_logs = [
        ("1", "Study", datetime.fromtimestamp(1638453394),),  
        ("1", "Study", datetime.fromtimestamp(1638543394),),  
        ("1", "Study", datetime.fromtimestamp(1638629794),),  
        ("1", "Study", datetime.fromtimestamp(1638888994),), 
        ("1", "Study", datetime.fromtimestamp(1638978994),),  
        ("1", "Study", datetime.fromtimestamp(1639004194),),  
        ("1", "Study", datetime.fromtimestamp(1639058194),),  
        ("1", "Study", datetime.fromtimestamp(1639144594),),  
        ("1", "Study", datetime.fromtimestamp(1639245394),),  
        ("1", "Study", datetime.fromtimestamp(1639338994),),  
        ("1", "Study", datetime.fromtimestamp(1639436194),),  
        ("1", "Study", datetime.fromtimestamp(1639439794),),  
        ("1", "Study", datetime.fromtimestamp(1639497394),),  
        ("1", "Study", datetime.fromtimestamp(1639583794),),  
        ("1", "Study", datetime.fromtimestamp(1639662994),),  
        ("1", "Study", datetime.fromtimestamp(1639734000),),  
        ("1", "Study", datetime.fromtimestamp(1639820400),),  
        ("1", "Study", datetime.fromtimestamp(1639929300),),  
        ("1", "Study", datetime.fromtimestamp(1640037300),),  
        ("1", "Study", datetime.fromtimestamp(1640041260),),  
        ("1", "Study", datetime.fromtimestamp(1640088060),),  
        ("1", "Study", datetime.fromtimestamp(1640174460),),  
        ("1", "Study", datetime.fromtimestamp(1640268060),),  
        ("1", "Study", datetime.fromtimestamp(1640350860),),  
        ("1", "Study", datetime.fromtimestamp(1640437260),),  
        ("1", "Study", datetime.fromtimestamp(1640516700),),  
        ("1", "Study", datetime.fromtimestamp(1640595900),),  
        ("1", "Study", datetime.fromtimestamp(1640646300),),  
        ("1", "Study", datetime.fromtimestamp(1640670137),),  
        ("1", "Study", datetime.fromtimestamp(1640760137),),  
        ("1", "Study", datetime.fromtimestamp(1640836817),),  
        ("1", "Study", datetime.fromtimestamp(1640865617),),  
        ("1", "Study", datetime.fromtimestamp(1640865645),),  
        ("1", "Study", datetime.fromtimestamp(1640948417),),  
        ("1", "Study", datetime.fromtimestamp(1641038417),),  

        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1638532845),),
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1638619245),), 
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1638705645),), 
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1638954045),),  
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1639296045),),  
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1639649145),),  
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1639739145),),  
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1639825545),),   
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1639904745),), 
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1639983945),),  
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1640066745),),  
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1640153145),),   
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1640232345),), 
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1640318745),),  
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1640844345),),  
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1640948745),), 
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1641009945),),  
        ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1641103545),),  

        ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1638249069),), 
        ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1638943869),),   
        ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1639289469),), 
        ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1639548669),), 
        ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1639635069),),  
        ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1639725069),),  
        ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1639811469),),  
        ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1640157069),),  
        ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1640675469),), 
        ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1641366669),),  
        ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1642057869),), 
        ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1642060800), ),  

        ("4", "Work Out", datetime.fromtimestamp(1638169869),), 
        ("4", "Work Out", datetime.fromtimestamp(1638429069),),  
        ("4", "Work Out", datetime.fromtimestamp(1638688269),), 
        ("4", "Work Out", datetime.fromtimestamp(1640243469),), 
        ("4", "Work Out", datetime.fromtimestamp(1641453069),),  
        ("4", "Work Out", datetime.fromtimestamp(1642057869),),   

        ("5", "Visit Family", datetime.fromtimestamp(1638263469),), 
        ("5", "Visit Family", datetime.fromtimestamp(1638843069),),  
        ("5", "Visit Family", datetime.fromtimestamp(1640225469),),
        ("5", "Visit Family", datetime.fromtimestamp(1643940669),), 

    ]

    # insert habit_log default data to database:
    cur.executemany("INSERT INTO habit_log VALUES (NULL, ?, ?, ?)", default_logs)
    db.commit()


