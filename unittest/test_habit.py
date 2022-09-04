import os
import sys
_relative_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_relative_path)

from application.habit import Habit
from test_database_setup import TestApplication
import unittest
from application.cli import show_habit_names_in_cli
from application.habit import Habit, Log
from datetime import datetime
from application.database import get_all_habits, get_all_log_data

TestApplication.setUp(unittest.TestCase)

class TestHabit(TestApplication):
    def test_habit_methods(self):

        self.assertEqual(len(get_all_habits(self.db)), 5)

        # creates temporary habit:
        temp_habit = Habit(self.db, habit_id=6, habit_name="Cleaning Bathroom", habit_periodicity="weekly", habit_description="", habit_created=datetime.fromtimestamp(1636585200))
        
        # test save-method of Habit and checks if saving was successful:
        temp_habit.save()
        self.assertEqual(len(get_all_habits(self.db)), 6)
        self.assertIn("6 - Cleaning Bathroom" ,show_habit_names_in_cli(self.db))

        # creates temporary log:
        temp_log = Log(self.db, habit_id = 6, log_date=datetime.fromtimestamp(639097260))

        # test save-method of Log and checks if saving was successful:
        self.assertEqual(len(get_all_log_data(self.db, 6)), 0)
        temp_log.save()
        self.assertEqual(len(get_all_log_data(self.db, 6)), 1)

        # test delete-method of Log and checks if deleting was successful:
        temp_log.delete()
        self.assertEqual(len(get_all_log_data(self.db, 6)), 0)

        # deletes temp_habit and checks if successful:
        temp_habit.delete()
        self.assertEqual(len(get_all_habits(self.db)), 5)


# close and delete the test database
TestApplication.tearDown(unittest.TestCase)

if __name__ == "__main__":
    unittest.main()
