# ToDo List

## Refactoring project structure
- [ ] Look into potential ways to restructure the project to make it closer to industry standard, or at least more clear
- [ ] Change all functions that don't take args to be passed 'None"

## Docstring the code
- [x] Some code has docstrings, make sure all code has docstrings, even before further coding is done as to aid that further coding.

## Backfill Process
- [ ] Replace console message with a new Tkinter screen during backfill process to display a loading screen. 
- This has proven very difficult

- [ ] Look into using a more suitable data structure for storing dates that do not have data and are to-be filled

## Search Data Screen
- [x] Enhance historic dates display by presenting more information than just the close price.
- [ ] Add commas to relevant numbers.
- [ ] Include calculated data (e.g., percentage change since the last day) for historic dates.
- [ ] Implement search by metric functionality.
- [x] Improve error handling and messages for a better user experience on the search screen.

## Database Setup
- [ ] If feasable, reset the database and make sure to include 'low' data point to generate candlestick graphs (prerequisite for later todo)

## Graph Screen
- [ ] Add option to generate candlestick graphs (Prerequisite from database section must be fulfilled before this)
- [ ] Ensure that the system is able to handle duplicate companies being selected

## Sort Screen
- [ ] Add a check for if the sort save directory exists, and if it doesn't, create it
- [ ] Implement sorting by multiple metrics.
- [ ] Look into the system choosing the optimal sort method, instead of the user
- [ ] Develop quicksort and heapsort algorithms.
- [ ] In sort.py, check comment about using f string first. See if doable to clean up code

## Settings and Preferences
- [ ] Create a settings and preferences system to allow users to customize their experience.

## Web Scraping and Threshold System
- [ ] Integrate a web scraping feature.
- [ ] Implement a threshold system for relevant data.

## Auto Dependency Installing
- [ ] Identify all libraries used and depedencies
- [ ] Make a script that checks for them and auto installs as necessary

## Database Handling
- [ ] Change the redundant restating of call_all_companies and see if it can be imported
- [ ] Do same as above but with companies.py too
- [ ] Examine database scalability and make necessary changes (i.e. removing data more than 3 years old?)

## Reset screens
- [ ] Reset screens when the back button is pressed

## Adding new companies
- [ ] Investigate the possiblity of a feature that allows a user to add a new company to the database.

## Currency data
 - [ ] Investigate the possibility of storing currency data in the system