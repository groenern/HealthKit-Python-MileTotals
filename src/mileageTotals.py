from tabulate import tabulate
import sys
from Workout import Workout
from WorkoutUtility import WorkoutUtility
from XMLParser import XMLParser

def checkCommandLineArg():
    if len(sys.argv) < 2:
        print("Please provide the file name as command line argument.")
        sys.exit(1)

    return sys.argv[1]
    
def main():
    # Get Filename from sysargs and parse xml data
    fileName = checkCommandLineArg() 
    runs, walks = XMLParser(fileName).parse()

    # create workout utility
    workUtility = WorkoutUtility()
    
    # populate our working data
    totalRunningMiles, totalRunningCalories, runWeeklyTotals = workUtility.calculateWeeklyTotals(runs)
    totalRunningMiles = round(totalRunningMiles, 2)
    totalRunningCalories = round(totalRunningCalories, 2)

    totalWalkingMiles, totalWalkingCalories, walkWeeklyTotals = workUtility.calculateWeeklyTotals(walks)
    totalWalkingMiles = round(totalWalkingMiles, 2)
    totalWalkingCalories = round(totalWalkingCalories, 2)

    # create table with all data
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

    # print walking and running totals
    print(f'\nTotal Running Miles: {totalRunningMiles}\nTotal Active Calories: {totalRunningCalories}')
    print(f'\nTotal Walking Miles: {totalWalkingMiles}\nTotal Active Calories: {totalWalkingCalories}')

    # print total miles and calories
    totalMiles = round(totalRunningMiles + totalWalkingMiles, 2)
    totalCalories = round(totalRunningCalories + totalWalkingCalories, 2)

    print(f'\nTotal Miles: {totalMiles}\nTotal Active Calories: {totalCalories}')

if __name__ == '__main__':
    main()