import xml.etree.ElementTree as ET
from Workout import Workout

class XMLParser:
    def __init__(self, fileName):
        self.fileName = fileName
        
    def parse(self):
        tree = ET.parse(self.fileName)
        root = tree.getroot()

        # define empty runs and walks list to return
        runs = []
        walks = []

        # Find all Workout elements and create a Workout object for each one
        for workout in root.findall('.//Workout'):
            workoutType = workout.get('workoutActivityType')
            if workoutType == 'HKWorkoutActivityTypeRunning':
                runs.append(Workout(workout))
            elif workoutType == 'HKWorkoutActivityTypeWalking':
                walks.append(Workout(workout))

        return runs, walks