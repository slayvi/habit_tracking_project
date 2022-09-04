# Habit Tracking Application

## Installation

### Prepare your environment for the use of the Application

For stable usage of the application, **python version 3.10.4** is recommended. Install python from the [official website](https://www.python.org/). Check your python version with entering your command promt and execute the following command:

```python
python --version 
```

It is recommended to use a customized environment to ensure full functionality, e.g. with the distribution anaconda, which can be downloaded [here](https://www.anaconda.com/products/distribution).

Install the required packages with the following command in your command line interface (For more information about pip, please check the [pip documentation](https://pip.pypa.io/en/latest/user_guide/)):

```python
pip install -r requirements.txt 
```

&nbsp;

## Use of the Application

First download the code by either downloading the .zip-File or clone it via the command promt. For more information about the later please check the [github docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

To run the application, either open the project with a python-IDE and run the file *main.py* or enter the following in the command prompt:

```python
python main.py 
```

&nbsp;

## Introduction to the Menu

After following the steps above, you should be greeted with the following screen, which is the main menu of the application:

![](/pictures/main.gif)

From here on, you can create new habits, check your existing habits off, analyse your habits and delete data if you want. To navigate through the application, please use your *up* and *down* keys as well as the *Enter button*.
If you want to close the application, either move the cursor to **Exit** and press *Enter*, or use the shortcut *Ctrl+C*.

&nbsp;

### Create New Habits

If you want to create new habits, select **Create a Habit** in the main menu. The following step through will show you what to consider.

![](/pictures/create.gif)

First enter a name for your habit.
The application will remind you of entering at least one character:
After confirming your habit name with the *Enter* key, you can select a periodicity of the habit from daily, weekly and monthly. 
Then you can add a description to your habit, which is optional. Finally press *Enter* and return to the main menu.

&nbsp;

### Check off habits

If you want to log your habits after you completed them, select **Check off** in the main menu.
You will see all of your tracked habits after that, where you can select the one you want to checkoff using your *arrow keys*
and confirm with *Enter*. The current time of logging will be stored in the database and you will be informed about the current
status - if you have completed the habit, have already done it in the expecting time period or if you broke the habit.

For more information about checking off in time please check the section **How to succeed in streaks**.

![](/pictures/checkoff.gif)

&nbsp;

### Analyze your habits

To analyze your habits, select **Analyze** in the main menu. Here you have the choice of different options:

* List all tracked habits - prints all habits with Name, Description and time when created to the screen.
* Habits with same periodicity - select a periodicity and the application will show you all habits with the respective periodicity with Name, Description and time when created to the screen.
* Longest streak of habit - you can select one of your habits to see the longest streak so far of it. The screen will show the Name, the longest streak and the last time you checked the habit off.
* Longest streak of all - prints the longest streak of all your habits with name, longest streak and the time it was last checked off (more than one longest streak is possible).

![](/pictures/analyze.gif)

&nbsp;

### Delete your Data

If you want to delete some of your data, select **Delete** in the main menu.
There will be a list of all your currently stored habit. Select one with your *arrow keys* and the *enter button*. You can choose
whether you want to delete all records of the habit (the habit itself along with all the logged data), or only the habit log.

![](/pictures/delete.gif)

&nbsp;

### Exit

To close the application, either use the shortcut *Ctrl+C* or select **Exit** and press *enter*.

&nbsp;

## How to succeed in streaks

To get a first streak, just check off your habit at any time.
To get a more-day / more-week / more-month streak, consider the following:

* **Daily streaks:** To increase streaks of daily habits, check off your habit on consecutive days from 00:00 to 23:59. Between two checkoff, there has to be a timespan of at least 4 hours.
* **Weekly streaks:** To increase streaks of weekly habits, check off your habit every calendar week from monday 00:00 to sunday 23:59. Between two checkoff, there has to be a timespan of at least 4 hours.
* **Monthly streaks:** To increase streaks of monthly habits, check off your habit from the first day of the month 00:00 to the last day of the respective month 23:59. Between two checkoff, there has to be a timespan of at least 4 hours.

&nbsp;

## Testing the Application

To test the application, change in the directory **unittest** and run **test_analyze.py** for testing the analyze-functions and **test_habit.py** for testing the methods of the class.
