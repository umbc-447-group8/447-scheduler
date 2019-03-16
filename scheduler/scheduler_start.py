from __future__ import division
from __future__ import print_function
from ortools.sat.python import cp_model

###To start, we should focus on being able to fill quotas for doctors and PAs.
###We could possibly use the same algo for doctors and PAs, but it might be easier to have two seperate
###algorithms for each as they have different variable constraints
###Perhaps include classes for Doctors and PAs
###Main can be changed to just call the functions


def solve(shift_requests, num_employees, num_shifts, num_days):
    all_employees = range(num_employees)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    # Creates the model.
    ###This : https://developers.google.com/optimization/cp/cp_solver helps show what a cp_model is and what it's functions do
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: employee 'n' works shift 's' on day 'd'.
    ###This also has to be able to be modified to satisfy the # of shifts
    shifts = {}
    for n in all_employees:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d,
                        s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    # Each shift is assigned to exactly one employee in .
    ###This is again a place where we can change the amount of employees/doctors working during one shift
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_employees) == 1)

    # Each employee works at most one shift per day.
    ###Should hold true
    ###Can also check so that no doctor works a full week, or night-day
    for n in all_employees:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)

    # min_shifts_assigned is the largest integer such that every employee can be
    # assigned at least that number of shifts.
    ###Depending on constraints, employees might not have to work a certain amount of shifts,
    ###Here would be a good place to instead track if a employee has made a quoto or not, and adjust the schedule accordingly
    min_shifts_per_employee = (num_shifts * num_days) // num_employees
    max_shifts_per_employee = min_shifts_per_employee + 1
    for n in all_employees:
        num_shifts_worked = sum(
            shifts[(n, d, s)] for d in all_days for s in all_shifts)
        model.Add(min_shifts_per_employee <= num_shifts_worked)
        model.Add(num_shifts_worked <= max_shifts_per_employee)

    model.Maximize(
        sum(shift_requests[n][d][s] * shifts[(n, d, s)] for n in all_employees
            for d in all_days for s in all_shifts))
    

    # Creates the solver and solve.
    ###It seems like .Solve() handles finding the best solution
    solver = cp_model.CpSolver()
    solver.Solve(model)
    for d in all_days:
        print('Day', d)
        for n in all_employees:
            for s in all_shifts:
                if solver.Value(shifts[(n, d, s)]) == 1:
                    if shift_requests[n][d][s] == 1:
                        print('employee', n, 'works shift', s, '(requested).')
                    else:
                        print('employee', n, 'works shift', s, '(not requested).')
        print()

    ###If there are no moonlighters, try another solution. 

    # Statistics.
    print()
    print('Statistics')
    print('  - Number of shift requests met = %i' % solver.ObjectiveValue(),
          '(out of', num_employees * min_shifts_per_employee, ')')
    print('  - wall time       : %f s' % solver.WallTime())


def main():
    # This program tries to find an optimal assignment of employees to shifts
    # (3 shifts per day, for 7 days), subject to some constraints (see below).
    # Each employee can request to be assigned to specific shifts.
    # The optimal assignment maximizes the number of fulfilled shift requests.

    ###These can be user defined variables that will be saved.
    ###Also include places where the days can be split up, such as 8 hour shifts during weekdays and 12 hour during weekends.
    ###Could ask for which days have how many x hour shifts and can be calculated after that.
    ###IMPORTANT: Keep track of the # of weeks in a month and how the weeks are filled. 
    num_employees = 5
    num_shifts = 3
    num_days = 7
    all_employees = range(num_employees)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    ###This could be expanded to go from 0 - 10, 0 being no request, and 10 being a high priority request/ non-negotiable
    ##Also user definable
    shift_requests_raw = [[[0, 0, 2], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 4], [0, 3, 0], [0, 0, 2]],
                          [[0, 0, 0], [0, 0, 0], [0, 2, 0], [0, 3, 0], [3, 0, 0], [0, 0, 0], [0, 0, 2]],
                          [[0, 4, 0], [0, 5, 5], [5, 0, 0], [2, 5, 0], [5, 0, 5], [0, 1, 0], [0, 0, 0]],
                          [[0, 0, 1], [0, 0, 0], [2, 0, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, 0]],
                          [[0, 0, 0], [0, 0, 1], [0, 2, 0], [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 0]]]
    
    shift_requests = shift_requests_raw

    for n in all_employees:
        for d in all_days:
            for s in all_shifts:
                if s > 1:
                    shift_requests[n][d][s] = 0
    
    solve(shift_requests, num_employees, num_shifts, num_days)
    


if __name__ == '__main__':
    main()
