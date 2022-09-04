from datetime import timedelta, datetime
import sqlite3
from .database import get_all_log_data, get_periods, get_all_habits

# define the list with different periodicites and assign it with the default values
choice_for_periodicity = ["daily", "weekly", "monthly"]

# define the timespan in hours which has to be between two checkoffs and assign it with default 4 hours
delta_hour_daily = delta_hour_weekly = delta_hour_monthly = 4


def convert_date_and_time_for_calculation(db: sqlite3.Connection, habit_id: int) -> list:
    """This function converts the data from a specific Habit id of the connected database (habit_log) from a string into a datetime-format. 
    The respective data in datetime-format will be stored in a list, which will be returned by the function. 
    To improve calculation, a datetime way back in the past is stored in the first index.

    Parameters:
        db (sqlite3.Connection): Connection to Database
        habit_id (int) : id of the individual habit

    Returns:
        list: A list with the Data of the connected database (habit_log) in Datetime-Format [datetime.datetime(YYYY, MM, DD, hh, mm)]
    """

    # define variable (list) and store all log data in it:
    check_streak = get_all_log_data(db, habit_id)

    # define variable for formatting the date to be stored in the list:
    date_formatter = "%Y-%m-%d %X"

    # define variable and appends datetime far in the past to the list:
    date_start = datetime.fromtimestamp(639093601)
    date_list_calculate = [date_start]

    # convert string data of the habit_logs in datetime-format and appends it to the list:
    for i in check_streak:
        date_string = i[3]
        date_original = datetime.strptime(date_string, date_formatter)
        date_list_calculate.append(date_original)

    # returns the list:
    return date_list_calculate


def calc_streak_daily(
    db: sqlite3.Connection,
    habit_id: int,
    parse_date: list,
    bool_max_count: bool,
    delta_hours=delta_hour_daily,
) -> int:
    """This function calculates the respective streaks for daily habits. 
        The calculation consideres checked off in time if the checkoff is on the next day and a timespan greater than delta_hours is 
        between the checkoffs (status=1). If there isn't a difference of delta_hours between two checkoffs or the checkoffs happen the
        same day, the habit is considered to be already checked off in the respective timespan (status=2). If none of the above, the
        habit is considered to be broken (status=3). The status will be returned with the current strike (bool_max_count=False). 
        With bool_max_count=True, the maximum streak will be returned only.

    Args:
        db (sqlite3.Connection): Connection to Database
        habit_id (int): id of the individual habit
        parse_date (list): list of the log_data in datetime format
        bool_max_count (bool): if True: Function will return the maximum streak, if False: Function will return current streak
        delta_hours (int, optional): Time between the respective checkoffs to be considered as a streak in hours. Defaults to delta_hour_daily.

    Returns:
        int: maximum of streaks if bool_max_count == True, else current streak and status
    """

    # define count variable (current count) and count_max (maximum count) and assign them to 0:
    count = count_max = 0

    # define status variable and assign it to 0 to later check the status of the checkoff (done in time / obsolete / broken the habit):
    status = 0

    # get the log data from the database of a certain habit for further calculation:
    dataset_of_habit_log = get_all_log_data(db, habit_id)

    # define the starting date and set it to the first index of the list parse_date (a datetime far in the past):
    starting_date = parse_date[0]

    # iterates over the length of the dataset of habit logs:
    for idx in range(len(dataset_of_habit_log)):

        # checks if checkoff is on the day after the last checkoff and delta_hours hours are between the checkoffs:
        if parse_date[idx + 1].date() - starting_date.date() == timedelta(
            days=1
        ) and parse_date[idx + 1] - starting_date >= timedelta(hours=delta_hours):

            # increase counter by 1:
            count += 1
            # set status to 1 (checked off in time):
            status = 1

            # set starting_date to the datetime of the next index:
            starting_date = parse_date[idx + 1]

        # checks if there are less than delta_hours hours between the checkoffs or if its still the same day:
        elif parse_date[idx + 1] - starting_date < timedelta(hours=4) or parse_date[
            idx + 1
        ].date() - starting_date.date() == timedelta(days=0):

            # set status to 2 (checked off already in expected time):
            status = 2

        # else the habit was broken:
        else:

            # set count back to 1:
            count = 1

            # set status to 3 (broken the habit):
            status = 3 if starting_date != parse_date[0] else 1

            # set starting_date to the datetime of the next index:
            starting_date = parse_date[idx + 1]

        # checks if current count is greater equal the maximum count, if so, update the max_count value:
        if count >= count_max:
            count_max = count

    # returns the maximum streak or the current count and status, depending on the bool_max_count value:
    return count_max if bool_max_count == True else count, status


def calc_streak_weekly(
    db: sqlite3.Connection,
    habit_id: int,
    parse_date: list,
    bool_max_count: bool,
    delta_hours=delta_hour_weekly,
) -> int:
    """This function calculates the respective streaks for weekly habits.  
        The calculation consideres checked off in time if the checkoff is in the next calendar week and a timespan 
        greater than delta_hours is between the checkoffs (status=1). If there isn't a difference of delta_hours between two 
        checkoffs or the checkoffs happen the same calendar week, the habit is considered to be already checked off in the 
        respective timespan (status=2). If none of the above, the habit is considered to be broken (status=3). 
        The status will be returned with the current strike (bool_max_count=False). 
        With bool_max_count=True, the maximum streak will be returned only.


    Args:
        db (sqlite3.Connection): Connection to Database
        habit_id (int): id of the individual habit
        parse_date (list): list of the log_data in datetime format
        bool_max_count (bool): if True: Function will return the maximum streak, if False: Function will return current streak
        delta_hours (int, optional): Time between the respective checkoffs to be considered as a streak in hours. Defaults to delta_hour_weekly.
        
    Returns:
        int: maximum of streaks if bool_max_count == True, else current streak and status
    """

    # define count variable (current count) and count_max (maximum count) and assign them to 0:
    count = count_max = 0

    # define status variable and assign it to 0 to later check the status of the checkoff (done in time / obsolete / broken the habit):
    status = 0

    # get the log data from the database of a certain habit for further calculation:
    dataset_of_habit_log = get_all_log_data(db, habit_id)

    # define the starting date and set it to the first index of the list parse_date (a datetime far in the past):
    starting_date = parse_date[0]

    # iterates over the length of the dataset of habit logs:
    for idx in range(len(dataset_of_habit_log)):

        # checks if year of staring_date is equal the year of the next checkoff:
        if starting_date.year == parse_date[idx + 1].year:

            # checks if the week between the two checkoffs has changed, if so, it is considered to be already logged for the period:
            if (
                starting_date.isocalendar().week
                == parse_date[idx + 1].isocalendar().week
            ):

                # set status to 2 (checked off already in expected time):
                status = 2

            # checks if the week of checkoff is +1 after the last checkoff and if there are less than delta_hours hours between the checkoffs:
            elif starting_date.isocalendar().week + 1 == parse_date[
                idx + 1
            ].isocalendar().week and parse_date[idx + 1] - starting_date >= timedelta(
                hours=delta_hours
            ):

                # increase counter by 1:
                count += 1

                # set status to 1 (checked off in time):
                status = 1

                # set starting_date to the datetime of the next index:
                starting_date = parse_date[idx + 1]

            # checks if week of checkoff +1 is smaller than last checkoff, therefore broke the habit:
            elif (
                starting_date.isocalendar().week + 1
                < parse_date[idx + 1].isocalendar().week
            ):
                # set count back to 1:
                count = 1

                # set status to 3 (broken the habit):
                status = 3 if starting_date != parse_date[0] else 1

                # set starting_date to the datetime of the next index:
                starting_date = parse_date[idx + 1]

        # checks if year of starting_date +1 is equal the year of the next checkoff (necessary if new year starts):
        elif starting_date.year + 1 == parse_date[idx + 1].year:

            # checks if last and next checkoff are in the same week (if so, checkoff is obsolete):
            if (
                starting_date.isocalendar().week
                == parse_date[idx + 1].isocalendar().week
            ):
                # set status to 2 (checked off already in expected time):
                status = 2

            # checks if week of next checkoff is 1 (therefore a new year has started) and there
            # are less than delta_hours hours between the checkoffs
            # also checks if starting week plus a timedelta of 7 days is the next week
            # (considered to be fail safe if a year has different number of weeks (52, 53 e.g)):
            elif (
                parse_date[idx + 1].isocalendar().week == 1
                and parse_date[idx + 1] - starting_date >= timedelta(hours=delta_hours)
                and (starting_date + timedelta(days=7)).isocalendar().week
                == parse_date[idx + 1].isocalendar().week
            ):

                # increase count by 1:
                count += 1

                # set status to 1 (checked off in time):
                status = 1

                # set starting_date to the datetime of the next index:
                starting_date = parse_date[idx + 1]

            # else considered as breaking the habit:
            else:

                # set count back to 1:
                count = 1

                # set status to 3 (broken the habit):
                status = 3 if starting_date != parse_date[0] else 1

                # set starting_date to the datetime of the next index:
                starting_date = parse_date[idx + 1]

        # else considered as breaking the habit:
        else:

            # set count back to 1:
            count = 1

            # set status to 3 (broken the habit):
            status = 3 if starting_date != parse_date[0] else 1

            # set starting_date to the datetime of the next index:
            starting_date = parse_date[idx + 1]

        # checks if current count is greater equal the maximum count, if so, update the max_count value:
        if count >= count_max:
            count_max = count

    # returns the maximum streak or the current count and status, depending on the bool_max_count value:
    return count_max if bool_max_count == True else count, status


def calc_streak_monthly(
    db: sqlite3.Connection,
    habit_id: int,
    parse_date: list,
    bool_max_count: bool,
    delta_hours=delta_hour_monthly,
) -> int:
    """This function calculates the respective streaks for mothly habits. 
        The calculation consideres checked off in time if the checkoff is in the next month and a timespan 
        greater than delta_hours is between the checkoffs (status=1). If there isn't a difference of delta_hours between two 
        checkoffs or the checkoffs happen the same month, the habit is considered to be already checked off in the 
        respective timespan (status=2). If none of the above, the habit is considered to be broken (status=3). 
        The status will be returned with the current strike (bool_max_count=False). 
        With bool_max_count=True, the maximum streak will be returned only.


    Args:
        db (sqlite3.Connection): Connection to Database
        habit_id (int): id of the individual habit
        parse_date (list): list of the log_data in datetime format
        bool_max_count (bool): if True: Function will return the maximum streak, if False: Function will return current streak
        delta_hours (int, optional): Time between the respective checkoffs to be considered as a streak in hours. Defaults to delta_hour_monthly.
        
    Returns:
        int: maximum of streaks if bool_max_count == True, else current streak
    """
    # define count variable (current count) and count_max (maximum count) and assign them to 0:
    count = count_max = 0

    # define status variable and assign it to 0 to later check the status of the checkoff (done in time / obsolete / broken the habit):
    status = 0

    # get the log data from the database of a certain habit for further calculation:
    dataset_of_habit_log = get_all_log_data(db, habit_id)

    # define the starting date and set it to the first index of the list parse_date (a datetime far in the past):
    starting_date = parse_date[0]

    # iterates over the length of the dataset of habit logs:
    for idx in range(len(dataset_of_habit_log)):

        # checks if year of last and next checkoff is the same:
        if starting_date.year == parse_date[idx + 1].year:

            # checks if month of last checkoff +1 equals month of next checkoff and if there are less than delta_hours hours between the checkoffs:
            if parse_date[idx + 1].month == starting_date.month + 1 and parse_date[
                idx + 1
            ] - starting_date >= timedelta(hours=delta_hours):

                # increase counter by 1:
                count += 1

                # set status to 1 (checked off in time):
                status = 1

                # set starting_date to the datetime of the next index:
                starting_date = parse_date[idx + 1]

            # checks if month of next checkoff equals last checkoff, if so, it is considered to be already logged for the period:
            elif parse_date[idx + 1].month == starting_date.month:

                # set status to 2 (checked off already in expected time):
                status = 2

            # checks if month of next checkoff is greater than month of last checkoff + 1 (considered as habit broken):
            elif parse_date[idx + 1].month > starting_date.month + 1:

                # set status to 3 (broken the habit):
                status = 3 if starting_date != parse_date[0] else 1

                # set count back to 1:
                count = 1

                # set starting_date to the datetime of the next index:
                starting_date = parse_date[idx + 1]

        # checks if last checkoff year +1 is the year of the next checkoff and next month=January:
        elif (
            starting_date.year + 1 == parse_date[idx + 1].year
            and parse_date[idx + 1].month == 1
        ):

            # increase counter by 1
            count += 1

            # set status to 1 (checked off in time)
            status = 1

            # set starting_date to the datetime of the next index
            starting_date = parse_date[idx + 1]

        # checks if last checkoff year +1 is the year of the next checkoff and next month is not january:
        elif (
            starting_date.year + 1 == parse_date[idx + 1].year
            and parse_date[idx + 1].month != 1
        ):

            # set count back to 1:
            count = 1

            # set status to 3 (broken the habit):
            status = 3 if starting_date != parse_date[0] else 1

            # set starting_date to the datetime of the next index:
            starting_date = parse_date[idx + 1]

        # else set starting_date to the datetime of the next index and set count back to 1 (considered first checkoff):
        else:
            count = 1
            status = 1
            starting_date = parse_date[idx + 1]

        # checks if current count is greater equal the maximum count, if so, update the max_count value:
        if count >= count_max:
            count_max = count

    # returns the maximum streak or the current count and status, depending on the bool_max_count value:
    return count_max if bool_max_count == True else count, status


def calculation_of_streaks(db: sqlite3.Connection, habit_id: int, bool_max_count: bool) -> int:
    """A function to improve the arrangement of the program. Depending on the habit_id given as argumenent, the 
    streak is calculated via one of the functions for daily, weekly or monthly habits. 

    Args:
        db (sqlite3.Connection): Connection to Database
        habit_id (int): id of the individual habit
        bool_max_count (bool): if True: Function will return the maximum streak, if False: Function will return current streak

    Returns:
        int: maximum of streaks if bool_max_count == True, else current streak
    """

    # get the periodicity of the habit with habid_id from the connected database and store it in the variable periodicity
    periodicity = get_periods(db, habit_id)

    # define streak-variable and assign it to 0:
    respective_streak = 0

    # checks if periodicity of the habit is "daily", "weekly" or "monthly" and calculates according to the bool_max_count:
    # True: the maximum streak (respective_streak[0])
    # False: the current streak (respective_streak[0]) and the current status (respective_streak[1]):
    if periodicity == "daily":
        respective_streak = calc_streak_daily(
            db,
            habit_id,
            convert_date_and_time_for_calculation(db, habit_id),
            bool_max_count,
        )

    elif periodicity == "weekly":
        respective_streak = calc_streak_weekly(
            db,
            habit_id,
            convert_date_and_time_for_calculation(db, habit_id),
            bool_max_count,
        )

    elif periodicity == "monthly":
        respective_streak = calc_streak_monthly(
            db,
            habit_id,
            convert_date_and_time_for_calculation(db, habit_id),
            bool_max_count,
        )

    # returns the respective streak data (count, status).
    # If respective_streak[0] is 0, there hasn't been a habit logged of (return -1):
    return respective_streak[0], respective_streak[1] if respective_streak[0] != 0 else -1


def calculate_longest_streak_of_all(db: sqlite3.Connection) -> tuple:
    """This functions calculates the longest streak of all habits stored in the connected database. 
    Therefore the function calculation_of_streaks is called and executed for every habit.

    Args:
        db (sqlite3.Connection): Connection to Database

    Returns:
        tuple: habit_id (as list of ints) and maximum streak (as int) ([1],1)
    """

    # define count_max as variable with maximum streak and assign it to 0:
    count_max = 0

    # define list where the habit_ids with the maximum streaks are stored and assign it as empty list:
    habit_max_id = []

    # define list where the data of the habit is stored [(id, name, periodicity, description, created)]:
    complete_habit_data = get_all_habits(db)

    # iterates over the length of the dataset of all habits:
    for i in range(len(complete_habit_data)):

        # define variable count_max_individual with the maximum streak of the habit at index i:
        count_max_individual = calculation_of_streaks(
            db, complete_habit_data[i][0], True
        )[0]

        # checks if maximum streak of habit at index i is greater than maximum streak:
        if count_max_individual > count_max:

            # set value for maximum streak to maximum streak of habit at index i:
            count_max = count_max_individual

            # clear the list with the id of the maximum habits that is stored until now:
            habit_max_id.clear()

            # appends the current habit id to the list of id for maximum habits:
            habit_max_id.append(complete_habit_data[i][0])

        # checks if maximum streak of habit at index i is equal to the maximum streak:
        elif count_max_individual == count_max:

            # appends the current habit id to the list of id for maximum habits:
            habit_max_id.append(complete_habit_data[i][0])

    # returns the id of the maximum habit(s) as a list, and returns maximum count as int
    return habit_max_id, count_max
