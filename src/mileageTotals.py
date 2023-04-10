import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import sys

class Workout:
    def __init__(self, workoutElement):
        # parse directly 
        self.workoutActivityType = workoutElement.get('workoutActivityType')
        self.duration = workoutElement.get('duration')
        self.durationUnit = workoutElement.get('durationUnit')
        self.creationDate = workoutElement.get('creationDate')

        # Metadata Entires
        self.indoorWorkout = None
        self.weatherTemperature = None
        self.weatherHumidity = None
        self.elevationAscended = None

        # Workout Statistics
        self.totalDistance = None
        self.totalDistanceUnit = None
        self.totalActiveEnergy = None
        self.totalActiveEnergyUnit = None

        metadataEntries = workoutElement.findall('.//MetadataEntry')
        for entry in metadataEntries:
            if entry.get('key') == 'HKIndoorWorkout':
                self.indoorWorkout = entry.get('value')
            elif entry.get('key') == 'HKWeatherTemperature':
                self.weatherTemperature = entry.get('value')
            elif entry.get('key') == 'HKWeatherHumidity':
                self.weatherHumidity = entry.get('value')
            elif entry.get('key') == 'HKElevationAscended':
                self.elevationAscended = entry.get('value')

        workoutStatistics = workoutElement.findall('.//WorkoutStatistics')
        for entry in workoutStatistics:
            if entry.get('type') == "HKQuantityTypeIdentifierActiveEnergyBurned":
                self.totalActiveEnergy = entry.get('sum')
                self.totalActiveEnergyUnit = entry.get('unit')
            elif entry.get('type') == "HKQuantityTypeIdentifierDistanceWalkingRunning":
                self.totalDistance = entry.get('sum')
                self.totalDistanceUnit = entry.get('unit')


    def __str__(self):
        if self.indoorWorkout:
            return f'{self.workoutActivityType}, Indoor: {self.indoorWorkout}, Duration: {self.duration} {self.durationUnit}, Distance: {self.totalDistance} {self.totalDistanceUnit}, Energy Burned: {self.totalActiveEnergy} {self.totalActiveEnergyUnit}, Created on: {self.creationDate}'
        else:
            return f'{self.workoutActivityType}, Duration: {self.duration} {self.durationUnit}, Distance: {self.totalDistance} {self.totalDistanceUnit}, Energy Burned: {self.totalActiveEnergy} {self.totalActiveEnergyUnit}, Created on: {self.creationDate}, Elevation Ascended: {self.elevationAscended}, Temperature: {self.weatherTemperature}, Humidity: {self.weatherHumidity}'

# Group workouts by week starting on sunday
def groupByWeek(workouts):
    weekGroups = {}
    start_date = datetime.strptime(workouts[0].creationDate, '%Y-%m-%d %H:%M:%S %z')
    week_start = start_date - timedelta(days=start_date.weekday())
    for workout in workouts:
        creationDate = datetime.strptime(workout.creationDate, '%Y-%m-%d %H:%M:%S %z')
        weekNumber = (creationDate - week_start).days // 7 + 1
        if weekNumber not in weekGroups:
            weekGroups[weekNumber] = []
        weekGroups[weekNumber].append(workout)
    return weekGroups

# Calculate weekly totals with percent change from previous week
def calculateWeeklyTotals(workouts):
    weeklyTotals = {}
    totalMiles = 0
    totalCalories = 0
    
    for weekNumber, weekWorkouts in groupByWeek(workouts).items():
        weekStart = min(weekWorkouts, key=lambda workout: datetime.strptime(workout.creationDate, '%Y-%m-%d %H:%M:%S %z')).creationDate
        weekEnd = max(weekWorkouts, key=lambda workout: datetime.strptime(workout.creationDate, '%Y-%m-%d %H:%M:%S %z')).creationDate

        # Format to easy output string without hour (YYYY-MM-DD)
        formattedStart = datetime.strptime(weekStart, '%Y-%m-%d %H:%M:%S %z').strftime('%Y-%m-%d')
        formattedEnd = datetime.strptime(weekEnd, '%Y-%m-%d %H:%M:%S %z').strftime('%Y-%m-%d')

        
        weeklyTotalDistance = sum(float(workout.totalDistance) for workout in weekWorkouts if workout.totalDistance)
        weeklyTotalActiveEnergy = sum(float(workout.totalActiveEnergy) for workout in weekWorkouts if workout.totalActiveEnergy)
        weeklyTotals[weekNumber] = {
            'start': formattedStart,
            'end': formattedEnd,
            'totalDistance': round(weeklyTotalDistance, 2),
            'totalDistanceUnit': weekWorkouts[0].totalDistanceUnit if weekWorkouts else 'N/A',
            'totalActiveEnergy': round(weeklyTotalActiveEnergy, 2),
            'totalActiveEnergyUnit': weekWorkouts[0].totalActiveEnergyUnit if weekWorkouts else 'N/A',
        }
        
        totalMiles += weeklyTotalDistance
        totalCalories += weeklyTotalActiveEnergy
        
        if weekNumber == 1:
            weeklyTotals[weekNumber]['percentChange'] = 'N/A'
        else:
            previousWeekTotalDistance = weeklyTotals[weekNumber-1]['totalDistance']
            percentChange = (weeklyTotalDistance - previousWeekTotalDistance) / previousWeekTotalDistance * 100
            weeklyTotals[weekNumber]['percentChange'] = f'{percentChange:.2f}%'
            
    return totalMiles, totalCalories, weeklyTotals

import xml.etree.ElementTree as ET

def main():
    # Read command line for file path
    if len(sys.argv) < 2:
        print("Please provide the file name as command line argument.")
        sys.exit(1)
    fileName = sys.argv[1]

    # Parse the XML file
    tree = ET.parse(fileName)
    root = tree.getroot()

    # Find all Workout elements and create a Workout object for each one
    runs = []
    walks = []
    for workout in root.findall('.//Workout'):
        workoutType = workout.get('workoutActivityType')
        if workoutType == 'HKWorkoutActivityTypeRunning':
            runs.append(Workout(workout))
        elif workoutType == 'HKWorkoutActivityTypeWalking':
            walks.append(Workout(workout))

    # Print weekly totals for runs
    totalRunningMiles, totalRunningCalories, runWeeklyTotals = calculateWeeklyTotals(runs)
    totalRunningMiles = round(totalRunningMiles, 2)
    totalRunningCalories = round(totalRunningCalories, 2)

    print('Runs Weekly Totals:')
    for weekNumber, weeklyTotal in runWeeklyTotals.items():
        print(f'Week {weekNumber} ({weeklyTotal["start"]} to {weeklyTotal["end"]}): {weeklyTotal["totalDistance"]} {weeklyTotal["totalDistanceUnit"]} total distance, {weeklyTotal["totalActiveEnergy"]} {weeklyTotal["totalActiveEnergyUnit"]} total active energy, {weeklyTotal["percentChange"]} change from previous week')

    # Print weekly totals for walks
    totalWalkingMiles, totalWalkingCalories, walkWeeklyTotals = calculateWeeklyTotals(walks)
    totalWalkingMiles = round(totalWalkingMiles, 2)
    totalWalkingCalories = round(totalWalkingCalories, 2)

    print('Walks Weekly Totals:')
    for weekNumber, weeklyTotal in walkWeeklyTotals.items():
        print(f'Week {weekNumber} ({weeklyTotal["start"]} to {weeklyTotal["end"]}): {weeklyTotal["totalDistance"]} {weeklyTotal["totalDistanceUnit"]} total distance, {weeklyTotal["totalActiveEnergy"]} {weeklyTotal["totalActiveEnergyUnit"]} total active energy, {weeklyTotal["percentChange"]} change from previous week')

    print(f'\nTotal Running Miles: {totalRunningMiles}\nTotal Running Active Calories: {totalRunningCalories}')
    print(f'\nTotal Walking Miles: {totalWalkingMiles}\nTotal Walking Active Calories: {totalRunningCalories}')

    totalMiles = round(totalRunningMiles + totalWalkingMiles, 2)
    totalCalories = round(totalRunningCalories + totalWalkingCalories, 2)

    print(f'\nTotal  Miles: {totalMiles}\nTotal Active Calories: {totalCalories}')

if __name__ == '__main__':
    main()