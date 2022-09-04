import sqlite3
import questionary
from .database import get_periods, get_all_habit_name_and_id, default_habit_data
from .habit import Habit, Log
from .analytics import choice_for_periodicity
from .printers import (
    print_all_habits,
    print_check_off,
    print_longest_streak_of_given_habit,
    print_with_same_period,
    print_longest_streak_of_all,
    print_delete,
)

def show_habit_names_in_cli(db: sqlite3.Connection) -> list:
    """Function to call all stored habit_names and habit_ids and concatenate them for printing to the CLI.

    Args:
        db (sqlite3.Connection): Connection to Database

    Returns:
        list: List of strings of all stored name and id from connected database ['id - name']
    """

    # define choice_of_habits variable and assign it to a empty list:
    choice_of_habits = []

    # define list res and append to it habit_name and id:
    res = [row for row in get_all_habit_name_and_id(db)]

    # iterate over the length of res:
    for idx in range(len(res)):

        # assign the variables id and name and store to them the respective habit-id and habit-name
        id = str(get_all_habit_name_and_id(db)[idx][0])
        name = get_all_habit_name_and_id(db)[idx][1]

        # assign the variable id_name and assign it as "id - name"
        id_name = id + " - " + name

        # append the id_name to the list of choice_of_habits
        choice_of_habits.append(id_name)

    # append "back" to allow the user to go back to main menu:
    choice_of_habits.append("Back")

    # return list with id and habit:
    return choice_of_habits


def cli(db: sqlite3.Connection) -> None:
    """This function applies the Command Line Interface to let the user interact with the application.

    Args:
        db (sqlite3.Connection): Connected Database
    """

    # print the welcome screen:
    print("")
    print("=".center(71, "="))
    print(" Hello, welcome to your habit tracking app! ".center(70, "="))
    print("=".center(71, "="))

    # assign the variable main_menu and assign it to True:
    main_menu = True

    # if no data stored, ask the user to start from scratch or load data:
    if len(show_habit_names_in_cli(db)) == 1:
        choices = (["Start from scratch", "Load default data"])
        choice = questionary.select("There is no data so far. Do you want to start from scratch or load default data?", 
        choices=choices).ask()

        # loads default data
        if choice == "Load default data": default_habit_data(db)

        # exit application for user use ctrl+c
        elif choice == None: main_menu = False


    # while main_menu is True, show the main menu to let the user interact with the application:
    while main_menu:

        # ask the user for an action (at least one habit is stored):
        choices = (["Create a Habit", "Check Off", "Analyze", "Delete", "Exit"]

            # ask the user for an action (no habits stored so far):
            if len(show_habit_names_in_cli(db)) != 1
            else ["Create a Habit", "Info", "Exit"])
        choice = questionary.select("What do you want to do?", choices=choices).ask()

        # if user wants to create a habit, continue with asking for a habit name:
        if choice == "Create a Habit":
            habit_name = questionary.text(
                "What's the name of your habit?\n",
                # make sure the user inserts at least one character:
                validate=lambda text: True if len(text) > 0
                else "Cannot be empty, please insert a name for your habit.").ask()

            # if user didnt exit by shortcut (->None), continue with asking for a periodicity:
            if habit_name is not None:
                periods = questionary.select("How often do you like to do that habit?\n",
                    choices=choice_for_periodicity).ask()

                # if user didnt exit by shortcut (->None), continue with asking for a description:
                if periods is not None:
                    description = questionary.text(
                        "Give an description to your task (optional)\n").ask()

            # if user didnt exit by shortcut (->None), create a habit with the Habit-class and store it
            # with the method save():
            if habit_name and periods and description is not None:
                habit = Habit(
                    db=db,
                    habit_name=habit_name,
                    habit_periodicity=periods,
                    habit_description=description)
                habit.save()

                # Confirm to the user that the habit was stored:
                text = f'The habit "{habit_name}" has been stored.'
                print(text.center(71, "="))

        # if user wants to check off a habit, continue with showing the therefore possible habits and ids:
        elif choice == "Check Off":
            if len(show_habit_names_in_cli(db)) != 1:
                habit_name_and_id = questionary.select("Which habit do you want to check off?\n",
                    choices=show_habit_names_in_cli(db)).ask()

                # if user didnt exit by shortcut (->None) or select "Back"
                # create a log with the Log-Class and store it with the method save():
                if habit_name_and_id != None and habit_name_and_id != "Back":
                    habit_id, habit_name = habit_name_and_id.split(" - ")
                    log = Log(db, habit_id=habit_id, habit_name=habit_name)
                    log.save()

                    # Confirm to the user that the habit was checked off:
                    print_check_off(db, habit_name, habit_id)

        # if user wants to anaylze the habits, continue with showing the therefore possible actions:
        elif choice == "Analyze":

            choice = questionary.select("what do you want to analyze?",
                choices=[
                    "List all tracked habits",
                    "Habits with same periodicity",
                    "Longest streak of habit",
                    "Longest streak of all",
                    "Back"]).ask()

            # prints all tracked habits and continue after user presses enter:
            if choice == "List all tracked habits":
                print_all_habits(db)
                try:
                    input("Press enter to continue.")
                except KeyboardInterrupt:
                    print("\nYou have canceled by shortcut.\n\n")

            # ask user for periodicity:
            elif choice == "Habits with same periodicity":
                choice = questionary.select("which ones do you wanna see?", 
                choices=choice_for_periodicity).ask()

                # prints all accordingly tracked habits and continue after user presses enter:
                if choice != None: print_with_same_period(db, choice)

                # catch the error if the user cancels by shortcut:
                try:
                    input("Press enter to continue.")
                except KeyboardInterrupt:
                    print("\nYou have canceled by shortcut.\n\n")

            # if the user wants to see the longest streak, all habits with ids are shown:
            elif choice == "Longest streak of habit":
                habit_name_and_id = questionary.select("Which streak do you want to see?\n",
                    choices=show_habit_names_in_cli(db)).ask()

                # if user didnt exit by shortcut (->None) or selected "Back" the period of the chosen
                # habit will be retrieved and the longest streak will be shown to the user:
                if habit_name_and_id != "Back" and habit_name_and_id != None:
                    habit_id, _ = habit_name_and_id.split(" - ")
                    periods = get_periods(db, habit_id)
                    print_longest_streak_of_given_habit(db, habit_id)

                    # catch the error if the user cancels by shortcut:
                    try:
                        input("Press enter to continue.")
                    except KeyboardInterrupt:
                        print("\nYou have canceled by shortcut.\n\n")

            # shows the longest streak of all habits to the user:
            elif choice == "Longest streak of all":
                print_longest_streak_of_all(db)

                # catch the error if the user cancels by shortcut:
                try:
                    input("Press enter to continue.")
                except KeyboardInterrupt:
                    print("\nYou have canceled by shortcut.\n\n")

            # return to the main menu (if not set, pyinstaller throws an error..)
            main_menu = True


        # if user wants to delete date, continue with showing the therefore possible habits and ids:
        elif choice == "Delete":

            habit_name_and_id = questionary.select("Which habit do you want to delete?\n",
                choices=show_habit_names_in_cli(db)).ask()

            # if user didnt exit by shortcut (->None) or select "Back" continue with asking what the user wants to delete:
            if habit_name_and_id != None and habit_name_and_id != "Back":
                delete_bool = questionary.select("What do you wanna delete?\n",
                    choices=["All records", "Habit Log", "Back"]).ask()

                # split the habit id and name to single variables and assign them to Habit and Log classes:
                if delete_bool != "Back" and delete_bool != None:
                    habit_id, habit_name = habit_name_and_id.split(" - ")
                    habit = Habit(db, habit_id=habit_id)
                    log = Log(db, habit_id=habit_id)

                    # if user wants to delete all records, use methods delete() of classes Habit and Log respectively:
                    if delete_bool == "All records":
                        log.delete()
                        habit.delete()

                        # confirm to user the data was deleted:
                        print_delete(db, habit_name, True)

                    # if user wants to delete the habit log, use method delete() of the class Log:
                    elif delete_bool == "Habit Log":
                        log.delete()

                        # confirm to user the data was deleted:
                        print_delete(db, habit_name, False)

        # prints a short information, if the user hasn't created a habit yet.
        elif choice == "Info":
            print("=".center(71, "="))
            print("To see all the features, please create a habit first.".center(71, "="))
            print("=".center(71, "="))

            # catch the error if the user cancels by shortcut:
            try:
                input("Press enter to continue.")
            except KeyboardInterrupt:
                print("\nYou have canceled by shortcut.\n\n")

        # if user chooses Exit or use shortcut ctrl+c in the main menu, a goodbye message will be shown and the application will be closed:
        elif choice == "Exit" or choice == None:
            print("=".center(71, "="))
            print(" Bye, see you next time! ".center(69, "="))
            print("=".center(71, "="))
            main_menu = False
