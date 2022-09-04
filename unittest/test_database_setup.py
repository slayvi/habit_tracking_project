import os
import sys
_relative_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(_relative_path)

import unittest
from application.database import create_connection
from datetime import datetime
import os
from application.habit import Habit

class TestApplication(unittest.TestCase):
    """Class for Testing the Database, Habit-class and Log-class. 
    Test data is generated for December 2021, to make sure the application is running not even 
    when considering a new month, but also a new year.

    """

    def setUp(self) -> None:
        """
        Setup a temporary database 
        """

        # creating connection to testdatabase
        self.db = create_connection("UTest.db")
        cur = self.db.cursor()

        # insert test data
        test_habit_study = Habit(self.db, habit_name="Study", habit_periodicity="daily", habit_description="Study for University", habit_created=datetime.fromtimestamp(1636585200))
        test_habit_sleep = Habit(self.db, habit_name="Sleep more than 8 hours", habit_periodicity="daily", habit_description="", habit_created=datetime.fromtimestamp(1636585200))
        test_habit_clean = Habit(self.db, habit_name="Cleaning Coffee Machine", habit_periodicity="weekly", habit_description="", habit_created=datetime.fromtimestamp(1636585200))
        test_habit_workout = Habit(self.db, habit_name="Work Out", habit_periodicity="weekly", habit_description="Functional Fitness", habit_created=datetime.fromtimestamp(1636585200))
        test_habit_family = Habit(self.db, habit_name="Visit Family", habit_periodicity="monthly", habit_description="", habit_created=datetime.fromtimestamp(1636585200))

        # save habit data to test database:
        test_habit_study.save()
        test_habit_sleep.save()
        test_habit_clean.save()
        test_habit_workout.save()
        test_habit_family.save()

        # creating test log_data
        test_habit_logs = [
            ("1", "Study", datetime.fromtimestamp(1638453394),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1638543394),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1638629794),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1638888994),),  # count = 1
            ("1", "Study", datetime.fromtimestamp(1638978994),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1639004194),),  # obsolete checkoff
            ("1", "Study", datetime.fromtimestamp(1639058194),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1639144594),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1639245394),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1639338994),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1639436194),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1639439794),),  # obsolete checkoff
            ("1", "Study", datetime.fromtimestamp(1639497394),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1639583794),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1639662994),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1639734000),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1639820400),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1639929300),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1640037300),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1640041260),),  # obsolete checkoff
            ("1", "Study", datetime.fromtimestamp(1640088060),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1640174460),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1640268060),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1640350860),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1640437260),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1640516700),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1640595900),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1640646300),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1640670137),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1640760137),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1640836817),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1640865617),),  # obsolete checkoff
            ("1", "Study", datetime.fromtimestamp(1640865645),),  # obsolete checkoff
            ("1", "Study", datetime.fromtimestamp(1640948417),),  # count +1
            ("1", "Study", datetime.fromtimestamp(1641038417),),  # count +1
            # count_current == 26, count_max == 26
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1638532845),),  # count =1 Friday, 3. December 2021 12:00:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1638619245),),  # count +1 Saturday, 4. December 2021 12:00:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1638705645),),  # count +1 Sunday, 5. December 2021 12:00:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1638954045),),  # count =1 Wednesday, 8. December 2021 09:00:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1639296045),),  # count =1 Sunday, 12. December 2021 08:00:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1639649145),),  # count =1 Thursday, 16. December 2021 10:05:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1639739145),),  # count +1 Friday, 17. December 2021 11:05:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1639825545),),  # count +1 Saturday, 18. December 2021 11:05:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1639904745),),  # count +1 Sunday, 19. December 2021 09:05:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1639983945),),  # count +1 Monday, 20. December 2021 07:05:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1640066745),),  # count +1 Tuesday, 21. December 2021 06:05:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1640153145),),  # count +1 Wednesday, 22. December 2021 06:05:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1640232345),),  # count +1 Thursday, 23. December 2021 04:05:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1640318745),),  # count +1 Friday, 24. December 2021 04:05:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1640844345),),  # count =1 Thursday, 30. December 2021 06:05:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1640948745),),  # count +1 Friday, 31. December 2021 11:05:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1641009945),),  # count +1 Saturday, 1. January 2022 04:05:45
            ("2", "Sleep more than 8 hours", datetime.fromtimestamp(1641103545),),  # count +1 Sunday, 2. January 2022 06:05:45
            # count_max == 9, count_currrent == 4

            ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1638249069),),  # count =1 Tuesday, 30. November 2021 05:11:09
            ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1638943869),),  # count +1 Wednesday, 8. December 2021 06:11:09
            ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1639289469),),  # obsolete checkoff Sunday, 12. December 2021 06:11:09
            ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1639548669),),  # count +1 Wednesday, 15. December 2021 06:11:09
            ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1639635069),),  # obsolete checkoff Thursday, 16. December 2021 06:11:09
            ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1639725069),),  # obsolete checkoff Friday, 17. December 2021 07:11:09
            ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1639811469),),  # obsolete checkoff Saturday, 18. December 2021 07:11:09
            ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1640157069),),  # count +1 Wednesday, 22. December 2021 07:11:09
            ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1640675469),),  # count +1 Tuesday, 28. December 2021 07:11:09
            ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1641366669),),  # count +1 Wednesday, 5. January 2022 07:11:09
            ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1642057869),),  # count +1 Wednesday, 5. January 2022 07:11:09
            ("3", "Cleaning Coffee Machine", datetime.fromtimestamp(1642060800), ),  # count +1 Thursday, 13. January 2022 08:00:00
            # max_count == 7, current_count == 7

            ("4", "Work Out", datetime.fromtimestamp(1638169869),),  # count = 1 Monday, 29. November 2021 07:11:09
            ("4", "Work Out", datetime.fromtimestamp(1638429069),),  # count + 1 Thursday, 2. December 2021 07:11:09
            ("4", "Work Out", datetime.fromtimestamp(1638688269),),  # obsolete checkoff Sunday, 5. December 2021 07:11:09
            ("4", "Work Out", datetime.fromtimestamp(1640243469),),  # count = 1 Thursday, 23. December 2021 07:11:09
            ("4", "Work Out", datetime.fromtimestamp(1641453069),),  # count = 1 Thursday, 6. January 2022 07:11:09
            ("4", "Work Out", datetime.fromtimestamp(1642057869),),  # count +1 Thursday, 13. January 2022 07:11:09
            ("4", "Work Out", datetime.fromtimestamp(1642587705),),  # count +1 Wednesday, 19. January 2022 10:21:45
            ("4", "Work Out", datetime.fromtimestamp(1643365305),),  # count +1 Friday, 28. January 2022 10:21:45
            ("4", "Work Out", datetime.fromtimestamp(1643797305),),  # count +1 Wednesday, 2. February 2022 10:21:45
            ("4", "Work Out", datetime.fromtimestamp(1645006905),),  # count =1 Wednesday, 16. February 2022 10:21:45
            ("4", "Work Out", datetime.fromtimestamp(1645525305),),  # count +1 Tuesday, 22. February 2022 10:21:45
            # max_count == 5, current_count == 2

            ("5", "Visit Family", datetime.fromtimestamp(1638263469),),  # count =1 Tuesday, 30. November 2021 09:11:09
            ("5", "Visit Family", datetime.fromtimestamp(1638843069),),  # count +1 Tuesday, 7. December 2021 02:11:09
            ("5", "Visit Family", datetime.fromtimestamp(1640225469),),  # checkoff obsolete Thursday, 23. December 2021 02:11:09
            ("5", "Visit Family", datetime.fromtimestamp(1642846905),),  # count +1 Saturday, 22. January 2022 10:21:45
            ("5", "Visit Family", datetime.fromtimestamp(1643940669),),  # count +1 Friday, 4. February 2022 02:11:09
            ("5", "Visit Family", datetime.fromtimestamp(1649582505),),  # count =1 Sunday, 10. April 2022 09:21:45
            ("5", "Visit Family", datetime.fromtimestamp(1653729705),),  # count +1 Saturday, 28. May 2022 09:21:45
            ("5", "Visit Family", datetime.fromtimestamp(1653902505),),  # checkoff obsolete Monday, 30. May 2022 09:21:45
            ("5", "Visit Family", datetime.fromtimestamp(1656667305),),  # count =1 Friday, 1. July 2022 09:21:45

            # max_count == 4, current_count == 1
        ]

        cur.executemany("INSERT INTO habit_log VALUES (NULL, ?, ?, ?)", test_habit_logs)
        self.db.commit()


    def tearDown(self):
        """
        Delete the database after testing was successful.
        """
        self.db.close()
        os.remove("UTest.db")


if __name__ == "__main__":
    unittest.main()
