import os
import sys
_relative_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_relative_path)

from test_database_setup import TestApplication
import unittest
from application.analytics import (
    convert_date_and_time_for_calculation,
    calc_streak_daily,
    calc_streak_weekly,
    calc_streak_monthly,
    calculation_of_streaks,
    calculate_longest_streak_of_all,
)
from application.database import (
    create_connection,
    get_all_habits,
    get_all_habit_name_and_id,
    get_habits_same_periods,
    get_habit_name,
    get_periods,
    get_all_log_data,
)
from application.cli import show_habit_names_in_cli
from datetime import datetime

# setup the test database:
TestApplication.setUp(unittest.TestCase)


class TestAnalyze(TestApplication):
    
    def test_database_entrys(self):
        """Test the module database with it's functions, to make sure the database entries are queried the right way.
        """
        # create connection
        self.db = create_connection("UTest.db")

        #test if all 5 default habits are stored within the database:
        self.assertEqual(len(get_all_habits(self.db)), 5)
        
        # tests if the default habits are stored in the right order:
        self.assertEqual(
            get_all_habit_name_and_id(self.db),
            [
                [1, "Study"],
                [2, "Sleep more than 8 hours"],
                [3, "Cleaning Coffee Machine"],
                [4, "Work Out"],
                [5, "Visit Family"],
            ],
        )

        # tests the function get_habits_same_periods for daily default habits:
        self.assertEqual(
            get_habits_same_periods(self.db, "daily"),
            [
                ("Study", "Study for University", "2021-11-11 00:00:00"),
                ("Sleep more than 8 hours", "", "2021-11-11 00:00:00"),
            ],
        )

        # tests the function get_habits_same_periods for weekly default habits:
        self.assertEqual(
            get_habits_same_periods(self.db, "weekly"),
            [
                ("Cleaning Coffee Machine", "", "2021-11-11 00:00:00"),
                ("Work Out", "Functional Fitness", "2021-11-11 00:00:00"),
            ],
        )

        # tests the function get_habits_same_periods for monthly default habit:
        self.assertEqual(
            get_habits_same_periods(self.db, "monthly"),
            [("Visit Family", "", "2021-11-11 00:00:00")],
        )


        # tests the function get_habit_name for recieving the right name for habit_id:
        self.assertEqual(get_habit_name(self.db, 1), "Study")
        self.assertEqual(get_habit_name(self.db, 3), "Cleaning Coffee Machine")
        self.assertEqual(get_habit_name(self.db, 5), "Visit Family")

        # tests the function get_periods for recieving the right periodicity for habit_id:
        self.assertEqual(get_periods(self.db, 1), "daily")
        self.assertEqual(get_periods(self.db, 3), "weekly")
        self.assertEqual(get_periods(self.db, 5), "monthly")

        # tests if all default data is in test database:
        self.assertEqual(len(get_all_log_data(self.db, 4)), 11)

        # checks if first entry of database (habit_log) is callable:
        self.assertIn(
            (1, 1, "Study", "2021-12-02 14:56:34"), get_all_log_data(self.db, 1)
        )

        # checks if last entry of database (habit_log) is callable:
        self.assertIn(
            (81, 5, "Visit Family", "2022-02-04 03:11:09"), get_all_log_data(self.db, 5)
        )

        # tests if the function show_habit_names_in_cli is working accordingly:
        self.assertEqual(
            show_habit_names_in_cli(self.db),
            [
                "1 - Study",
                "2 - Sleep more than 8 hours",
                "3 - Cleaning Coffee Machine",
                "4 - Work Out",
                "5 - Visit Family",
                "Back",
            ],
        )

    def test_calculte(self):
        """Test the module analyze with it's functions, to make sure that the functions calculate correctly.
        """

        # tests if the convert_date_and_time_for_calculation returns datetime-type:
        self.assertEqual(
            type(convert_date_and_time_for_calculation(self.db, 1)[0]), datetime
        )
        self.assertEqual(
            type(convert_date_and_time_for_calculation(self.db, 3)[3]), datetime
        )

        # checks if first date of the calculation list is callable (startdate far in the past):
        self.assertIn(
            datetime(1990, 4, 3, 0, 0, 1),
            convert_date_and_time_for_calculation(self.db, 1),
        )

        # checks if last date of the calculation list is callable (last inserted timestamp of the test-database):
        self.assertIn(
            datetime.fromtimestamp(1641038417),
            convert_date_and_time_for_calculation(self.db, 1),
        )
        self.assertIn(
            datetime.fromtimestamp(1642057869),
            convert_date_and_time_for_calculation(self.db, 4),
        )

        # create caches for the following calculations: 
        parse_date_daily_obsolete_checkoffs = convert_date_and_time_for_calculation(self.db, 1)
        parse_date_daily_break_habit = convert_date_and_time_for_calculation(self.db, 2)
        parse_date_weekly_obsolete_checkoffs = convert_date_and_time_for_calculation(self.db, 3)
        parse_date_weekly_break_habit = convert_date_and_time_for_calculation(self.db, 4)
        parse_date_monthly = convert_date_and_time_for_calculation(self.db, 5)

        # checks if daily max_count is calculated right with data with obsolete checkoffs:
        self.assertEqual(calc_streak_daily(self.db, 1, parse_date_daily_obsolete_checkoffs, True)[0], 26)

        # checks if daily max_count is calculated right with data with breaking the habit:
        self.assertEqual(calc_streak_daily(self.db, 2, parse_date_daily_break_habit, True)[0], 9)

        # checks if daily current count is calculated right with data with obsolete checkoffs:
        self.assertEqual(calc_streak_daily(self.db, 1, parse_date_daily_obsolete_checkoffs, False)[0], 26,)

        # checks if daily current count is calculated right with data with breaking the habit:
        self.assertEqual(calc_streak_daily(self.db, 2, parse_date_daily_break_habit, False)[0], 4,)

        # checks if max count is calculated right with weekly habits with obsolete checkoffs:
        self.assertEqual(calc_streak_weekly(self.db, 3, parse_date_weekly_obsolete_checkoffs, True)[0],7)

        # checks if current count is calculated right with weekly habits with obsolete checkoffs:
        self.assertEqual(calc_streak_weekly(self.db, 3, parse_date_weekly_obsolete_checkoffs, False)[0],7,)

        # checks if max count is calculated right with weekly habits with breaking the habit:
        self.assertEqual(calc_streak_weekly(self.db, 4, parse_date_weekly_break_habit, True)[0], 5)

        # checks if current count is calculated right with weekly habits with breaking the habit:
        self.assertEqual(calc_streak_weekly(self.db, 4, parse_date_weekly_break_habit, False)[0], 2)

        # checks if current count is calculated right with monthly habits:
        self.assertEqual(calc_streak_monthly(self.db, 5, parse_date_monthly, False)[0], 1)

        # checks if max count is calculated right with monthly habits:
        self.assertEqual(calc_streak_monthly(self.db, 5, parse_date_monthly, True)[0], 4)

        # checks if function calculation_of_streaks and the respective calculation equals the same 
        self.assertEqual(calculation_of_streaks(self.db, 1, True)[0], calc_streak_daily(self.db, 1, parse_date_daily_obsolete_checkoffs, True)[0])
        self.assertEqual(calculation_of_streaks(self.db, 3, False)[0], calc_streak_weekly(self.db, 3, parse_date_weekly_obsolete_checkoffs, False)[0])
        self.assertEqual(calculation_of_streaks(self.db, 5, True)[0], calc_streak_monthly(self.db, 5, parse_date_monthly, True)[0])


        # checks the status of the checkoff:
        self.assertEqual(calculation_of_streaks(self.db, 1, False)[1], 1)
        self.assertEqual(calculation_of_streaks(self.db, 3, False)[1], 2)
        self.assertEqual(calculation_of_streaks(self.db, 5, False)[1], 3)

        # checks if longest_streak_calculation is the same as the maximum streak
        self.assertEqual(calculate_longest_streak_of_all(self.db),
            ([1],
                calc_streak_daily(
                    self.db, 1, parse_date_daily_obsolete_checkoffs, True
                )[0],
            ),
        )


# close and delete the test database
TestApplication.tearDown(unittest.TestCase)


if __name__ == "__main__":
    unittest.main()
