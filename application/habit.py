from datetime import datetime
import sqlite3


class Habit:
    """A class to represent a habit.

    Attributes
    ----------
    db : sqlite3.Connection
        Connection to the database
    habit_id : int
        id of the habit
    habit_name : str
        name of the habit
    habit_periodicity : str
        periodicity of the habit
    habit_description: str
        description of the habit
    habit_created: datetime
        time the habit was created

    Methods
    -------
    save():
        saves the habit to the connected database.
    delete():
        deletes the habit from the connected database.
    """
    
    def __init__(
        self,
        db:sqlite3.Connection,
        habit_id=None,
        habit_name="",
        habit_periodicity="",
        habit_description="",
        habit_created=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ):
        """Constructs all the necessary attributes for the Habit object.

        Args:
            db (sqlite3.Connection): Connection to Database
            habit_id (int): id of the habit
            habit_name (str, optional): name of the habit. Defaults to "".
            habit_periodicity (str, optional): periodicity of the habit. Defaults to "".
            habit_description (str, optional): description of the habit. Defaults to "".
            habit_created (datetime, optional): created time of the habit. Defaults to datetime.now().strftime("%Y-%m-%d %H:%M:%S").
        """
    
        self.db = db
        self.habit_id = habit_id
        self.habit_name = habit_name
        self.periodicity = habit_periodicity
        self.description = habit_description
        self.created = habit_created


    def save(self) -> None:
        """
        Saves the habit to the connected database.
        """

        cur = self.db.cursor()
        cur.execute(
            "INSERT INTO habits VALUES (NULL, ?, ?, ?, ?)",
            (self.habit_name, self.periodicity, self.description, self.created),)
        self.db.commit()


    def delete(self) -> None:
        """
        Deletes the habit from the connected database.
        """

        cur = self.db.cursor()
        cur.execute("DELETE FROM habits WHERE id=?", [self.habit_id])
        self.db.commit()



class Log(Habit):
    """A class to represent a Log and inherits from a Habit.

    Attributes
    ----------
    db : sqlite3.Connection
        Connection to the Database (inherit from class Habit)
    habit_id : int
        id of the habit (inherit from class Habit)
    habit_name : str
        name of the habit (inherit from class Habit)
    log_date: datetime
        time the habit was checked off

    Methods
    -------
    save():
        saves the log to the connected database.
    delete():
        deletes the log from the connected database.
    """

    def __init__(
        self,
        db: sqlite3.Connection,
        habit_id=None,
        habit_name="",
        log_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ):
        """Constructs all the necessary attributes for the Log object.

        Args:
            db (sqlite3.Connection): Connection to the Database
            habit_id (int, optional): id of the habit. Defaults to None.
            habit_name (str, optional): name of the habit. Defaults to "".
            log_date (datetime, optional): date and time of logging the respective habit. Defaults to datetime.now().strftime("%Y-%m-%d %H:%M:%S").
        """

        self.log_date = log_date

        # use parent class' Habit attributes and inherit them
        Habit.__init__(self, db, habit_id, habit_name)


    def save(self) -> None:
        """
        Saves a log to the connected database.
        """

        cur = self.db.cursor()
        cur.execute(
            "INSERT INTO habit_log VALUES (NULL, ?, ?, ?)",
            [self.habit_id, self.habit_name, self.log_date],
        )
        self.db.commit()


    def delete(self) -> None:
        """
        Deletes a log from the connected database.
        """

        cur = self.db.cursor()
        cur.execute("DELETE FROM habit_log WHERE habit_id=?", [self.habit_id])
        self.db.commit()
