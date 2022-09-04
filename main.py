#####################################################################################
###############               Habit Tracking Application              ###############
###############                       Version 1.0                     ###############
###############                  Author: Slavka F.                    ###############
#####################################################################################
#                                                                                   #
#   To keep the code clearly arranged, the following modules were build.            #
#   They contain the following:                                                     #
#                                                                                   #
# - main.py         Module with which the application is to be started.             #
# - habit.py        This module contains the initialization of the classes Habit    #
#                   and Log as well as the the respective methods and attributes.   #
# - cli.py          In this module the CLI is initialized and adapted.              #
# - database.py     This module consists of several functions to manipulate the     #
#                   database and to retrieve data from the database.                #
# - analytics.py    In this module functions are implemented, which are needed      #
#                   within the application for the calculation of the habits.       #
# - printers.py     In this module the print functions are initiated, which         #
#                   provide for a clear arranged output in the console.             #
# - default.py      Provides default data for habits and habit logs                 #
#####################################################################################


from application.cli import cli
from application.database import create_connection

# if current file is this one, create a connection to the database and start the cli:
if __name__ == "__main__":
    db = create_connection()
    cli(db)
