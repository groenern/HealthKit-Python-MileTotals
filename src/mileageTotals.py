from tabulate import tabulate
import sys
import datetime
from util.WorkoutUtility import WorkoutUtility
from util.XMLParser import XMLParser 
from model.Workout import Workout
from util.GoogleHandler import GoogleHandler

def checkCommandLineArg():
    if len(sys.argv) < 2:
        #print("Please provide the file name as command line argument.")
        #sys.exit(1)
        return "export.xml" ## DELETE LATER

    return sys.argv[1]

def populateData():
    # Get Filename from sysargs and parse xml data
    fileName = checkCommandLineArg() 
    xmlObject = XMLParser(fileName)
    xmlObject.parse()

    # create workout utility
    workUtility = WorkoutUtility()
    
    # populate our working data
    workouts = xmlObject.getWorkouts()
    runs, walks = xmlObject.getRunsWalks()
    runWeeklyTotals = workUtility.calculateWeeklyTotals(runs)
    walkWeeklyTotals = workUtility.calculateWeeklyTotals(walks)

    # get rows and cols -> didn't want to create second utility object
    rowWidth, colLength = workUtility.calcRowsCols(workouts=workouts)

    return workouts, runs, walks, runWeeklyTotals, walkWeeklyTotals, rowWidth, colLength

def printTable(runWeeklyTotals, walkWeeklyTotals):
    data = []
    for weekNumber in runWeeklyTotals:
        if weekNumber not in walkWeeklyTotals:
            walkWeeklyTotals[weekNumber] = {'start': '-', 'end': '-', 'totalDistance': 0, 'totalDistanceUnit': '-', 'totalActiveEnergy': 0, 'totalActiveEnergyUnit': '-', 'percentChange': '-'}
        data.append([
            f'{weekNumber}',
            f"{runWeeklyTotals[weekNumber]['totalDistance']} {runWeeklyTotals[weekNumber]['totalDistanceUnit']}",
            runWeeklyTotals[weekNumber]['totalActiveEnergy'],
            f"{walkWeeklyTotals[weekNumber]['totalDistance']} {walkWeeklyTotals[weekNumber]['totalDistanceUnit']}",
            walkWeeklyTotals[weekNumber]['totalActiveEnergy'],
            runWeeklyTotals[weekNumber]['percentChange'],
            walkWeeklyTotals[weekNumber]['percentChange'],
        ])

    # print table
    headers = ['Week', 'Run Distance', 'Run Calories', 'Walk Distance', 'Walk Calories', 'Run Distance % Change', 'Walk Distance % Change']
    print(tabulate(data, headers=headers, tablefmt='grid'))

def main():
    workouts, runs, walks, runWeeklyTotals, walkWeeklyTotals, rowWidth, colLength = populateData()

    # printTable(runWeeklyTotals, walkWeeklyTotals)

    # set up googlehandler and connect
    email = 'romangroenewold@gmail.com'
    credentials = 'credentials.json'
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    spreadsheet = 'Apple_Watch_Spreadsheet_Data_{}'.format(today)
    myGoogleHandler = GoogleHandler(email, credentials,spreadsheet)
   
    # create "workouts" worksheet
    myGoogleHandler.createWorksheet("Workouts", rowWidth, colLength)
    # populates "workouts" worksheet
    myGoogleHandler.populateWorksheet("Workouts", workouts)

    print(myGoogleHandler.__str__())

if __name__ == '__main__':
    main()