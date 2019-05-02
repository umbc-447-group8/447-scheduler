# config.py
# This script takes in parameters, and updates the config as specified
# Usage: python ./config.py --numshifts [number of shifts] --numweeks [number of weeks] --numemployees [number of employees]
import scheduler_config
import argparse

parser = argparse.ArgumentParser(description='Process flags.')
parser.add_argument('--numshifts', dest='numshifts', help='the number of shifts in a day')
parser.add_argument('--numweeks', dest='numweeks', help='the number of weeks to generate the schedule')
parser.add_argument('--numemployees', dest='numemp', help='the number of employees for a schedule period')

args = parser.parse_args()
if args.numshifts:
    numShifts = int(args.numshifts)
if args.numweeks:
    numWeeks = int(args.numweeks)
if args.numemp:
    numEmp = int(args.numemp)

def setShifts(numShifts):
    if (numShifts+1) == len(scheduler_config.shifts):
        
        # Create new shifts array in scheduler_config
        shiftsArray = ['O']
        for i in range(numShifts):
           shiftsArray.append(str(i+1))
        #scheduler_config.shifts = shiftsArray

        # Create new penalized_transitions array in scheduler_config        
        penTransitions = []
        for i in range(1, numShifts+1):
            for k in range(i, numShifts+1):
                if i != k:
                    penTransitions.append((i, k, 0))
        penTransitions.append((numShifts, 1, 0))
        #scheduler_config.penalized_transitions = penTransitions
        
setShifts(numShifts)