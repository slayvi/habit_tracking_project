import sqlite3
from .database import (
    get_all_habits,
    get_habits_same_periods,
    get_habit_name,
    get_periods,
)
from .analytics import (
    calculation_of_streaks,
    convert_date_and_time_for_calculation,
    calculate_longest_streak_of_all,
)
from beautifultable import BeautifulTable


def print_check_off(db: sqlite3.Connection, habit_name: str, habit_id: int) -> None:
    """This function prints the confirmation for a check off of a habit into the command line interface in a clear manner.

    Args:
        db (sqlite3.Connection): Connection to Database
        habit_name (str): Name of the habit
        habit_id (int): ID of the habit
    """

    # create table and print it with a header and set the table to a consistent width matched with the questionary lib:
    table = BeautifulTable()
    table.columns.header = ["Checked of Habit", "Current Streak"]
    table.columns.width = 34

    # appends the respective habit name and current streak to the table as a row:
    table.rows.append([habit_name, calculation_of_streaks(db, habit_id, False)[0]])
    print(table)

    print("")

    # if status = 1, user checked off in time:
    if calculation_of_streaks(db, habit_id, False)[1] == 1:
        print(" Congratulations, you have completed the habit. ".center(71, "="))

    # if status = 2, user have checked off in the respective timespan already:
    elif calculation_of_streaks(db, habit_id, False)[1] == 2:
        print(" Good effort, but you have already ".center(71, "="))
        print(" completed the habit in the given time period. ".center(71, "="))

    # if status = 3, user have broken the habit:
    elif calculation_of_streaks(db, habit_id, False)[1] == 3:
        print(" Unfortunately you have broken the habit.... ".center(71, "="))
        print(" Stay tuned! ".center(71, "="))

    print("")


def print_all_habits(db: sqlite3.Connection) -> None:
    """This function prints the name, description and created time of all habits into the command line interface in a clear manner.

    Args:
        db (sqlite3.Connection): Connection to Database
    """

    print("=".center(71, "="))
    print("These are all your habits:".center(71, "="))

    # creates table with habit name, description and created time as header
    table = BeautifulTable()
    table.columns.header = [
        "Habit Name",
        "Description",
        "Created"]

    # iterates over the length of the habit stored in the connected database and
    # append the data to the table
    for idx in range(len(get_all_habits(db))):
        table.rows.append([
                get_all_habits(db)[idx][1],
                get_all_habits(db)[idx][3],
                get_all_habits(db)[idx][4],])
    print(table)
    print("=".center(71, "="))


def print_with_same_period(db: sqlite3.Connection, periodicity: str) -> None:
    """This function prints the name, description and created time of all habits with the same 
    periodicity into the command line interface in a clear manner.

    Args:
        db (sqlite3.Connection): Connection to Database
        periodicity (str): Periodicity (daily, weekly, monthly)

    """

    print("=".center(71, "="))
    print("\nYour", periodicity, "habits:\n")

    # creates table with habit name, description and created time as header
    table = BeautifulTable()
    table.columns.header = [
        "Habit Name",
        "Description",
        "Created"]

    # iterates over the length of the habits with the same periodicity stored in the
    # connected database and appends the respective data to the table
    for idx in range(len(get_habits_same_periods(db, periodicity))):
        table.rows.append([
                get_habits_same_periods(db, periodicity)[idx][0],
                get_habits_same_periods(db, periodicity)[idx][1],
                get_habits_same_periods(db, periodicity)[idx][2],])
    print(table)
    print("=".center(71, "="))


def print_longest_streak_of_given_habit(db: sqlite3.Connection, habit_id: int) -> None:
    """This function prints the name, longest streak and the last time the habit was 
    checked off into the command line interface in a clear manner.

    Args:
        db (sqlite3.Connection): Connection to Database
        habit_id (int): ID of the habit 
    """

    # try to call the functions
    try:
        # define the variable and store the maximum streaks of the respective habit
        calculated_streak = calculation_of_streaks(db, habit_id, True)[0]

        # define the variable and store the habit name based on the habit id
        habit_name = get_habit_name(db, habit_id)

        # define the variable and store the last checked off date as a string
        last_checked = str(convert_date_and_time_for_calculation(db, habit_id).pop())

        periodicity = get_periods(db, habit_id)

        # check if the habit log is not empty
        if calculated_streak != 0:

            # creates table with habit name, longest streak and the last time the habit was checked off
            table = BeautifulTable()
            table.columns.header = [
                "Habit Name",
                "Longest Streak",
                "Last time checked off",
            ]

            # append the data to the table and print it with a note of the current streak
            table.rows.append([habit_name, calculated_streak, last_checked])
            print(table)
            if periodicity == "daily":
                print(
                    f"You have reached a {calculated_streak} day strike in your habit {get_habit_name(db, habit_id)}."
                )
            elif periodicity == "weekly":
                print(
                    f"You have reached a {calculated_streak*7} day strike in your habit {get_habit_name(db, habit_id)}."
                )
            elif periodicity == "monthly":
                print(
                    f"You have reached a {calculated_streak} month strike in your habit {get_habit_name(db, habit_id)}."
                )

        # if variable calculated_streak == -1, the habit log database has no logged data for the respective habit
        else:
            print("=".center(71, "="))
            print(
                "You haven't checked off that habit already, so there's nothing to show."
            )
            print("=".center(71, "="))

    # catch a type error, if a habit which isn't stored in the database is called
    except TypeError:
        print("=".center(71, "="))
        print("You haven't created the habit already, so there's nothing to show.")
        print("=".center(71, "="))


def print_longest_streak_of_all(db: sqlite3.Connection) -> None:
    """This function prints the name, longest streak and the last time the habit was 
    checked off into the command line interface in a clear manner of all habits with the longest streak.

    Args:
        db (sqlite3.Connection): Connection to Database
    """
    # define the variable and assign the length of the list to it
    len_for_iterate = len(calculate_longest_streak_of_all(db)[0])

    # creates table with habit name, longest streak and last time the respective habits were checked off as header
    table = BeautifulTable()
    table.columns.header = [
        "Habit Name",
        "Longest Streak",
        "Last time checked off"]

    print("=".center(71, "="))
    print("\nThe data of the longest streak of all your habits:\n")

    # define the variable and assign the longest streak as int to it
    longest_streak = calculate_longest_streak_of_all(db)[1]

    # Confirm that there is a habit log already:
    if longest_streak != 0:
        # iterate over the length of the list and update the variable for id, name and last checkoff-time
        # append the respective data to the rows and print the table
        for _ in range(len_for_iterate):
            habit_id = calculate_longest_streak_of_all(db)[0][_]
            habit_name = get_habit_name(db, habit_id)
            last_checked = str(
                convert_date_and_time_for_calculation(db, habit_id).pop()
            )
            table.rows.append([habit_name, longest_streak, last_checked])
        print(table)

    # if there isn't any habit log already, the user will see the following message:
    else:
        print("=".center(71, "="))
        print("You haven't checked off any habit already, so there's nothing to show.")
        print("=".center(71, "="))


def print_delete(db: sqlite3.Connection, habit_name: str, delete_bool: bool) -> None:
    """This function prints the name, longest streak and the last time the habit was 
    checked off into the command line interface in a clear manner of all habits with the longest streak.

    Args:
        db (sqlite3.Connection): Connection to Database
        delete_bool (bool): if True: deletes all, if False: deletes just the log
    """
    
    # creates table with habit name, longest streak and last time the respective habits were checked off as header:
    print("=".center(71, "="))
    if delete_bool:
        print(f"All data of habit {habit_name} was deleted.")
    else:
        print(f"All log data of habit {habit_name} was deleted.")
    print("=".center(71, "="))

    # catch the error if the user cancels by shortcut:
    try:
        input("Press enter to continue.")
    except KeyboardInterrupt:
        print("\nYou have canceled by shortcut.\n\n")
