# Copyright 2010-2018 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Creates a shift scheduling problem and solves it."""

from __future__ import print_function

import argparse

# Scheduler configurations
import scheduler_config

from ortools.sat.python import cp_model
from google.protobuf import text_format

# Utility functions for solver in scheduler_functions.py
from scheduler_functions import negated_bounded_span
from scheduler_functions import add_soft_sequence_constraint
from scheduler_functions import add_soft_sum_constraint

PARSER = argparse.ArgumentParser()
PARSER.add_argument(
    '--output_proto',
    default="",
    help='Output file to write the cp_model'
    'proto to.')
PARSER.add_argument('--params', default="", help='Sat solver parameters.')


def solve_shift_scheduling(params, output_proto, num_employees, num_weeks, shifts, fixed_assignments, requests, shift_constraints,
                             weekly_sum_constraints, penalized_transitions, weekly_cover_demands, excess_cover_penalties):
    """Solves the shift scheduling problem."""

    num_days = num_weeks * 7
    num_shifts = len(shifts)

    model = cp_model.CpModel()

    work = {}
    for e in range(num_employees):
        for s in range(num_shifts):
            for d in range(num_days):
                work[e, s, d] = model.NewBoolVar('work%i_%i_%i' % (e, s, d))

    # Linear terms of the objective in a minimization context.
    obj_int_vars = []
    obj_int_coeffs = []
    obj_bool_vars = []
    obj_bool_coeffs = []

    # Exactly one shift per day.
    for e in range(num_employees):
        for d in range(num_days):
            model.Add(sum(work[e, s, d] for s in range(num_shifts)) == 1)

    # Fixed assignments.
    for e, s, d in fixed_assignments:
        model.Add(work[e, s, d] == 1)

    # Employee requests
    for e, s, d, w in requests:
        obj_bool_vars.append(work[e, s, d])
        obj_bool_coeffs.append(w)

    # Shift constraints
    for ct in shift_constraints:
        shift, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost = ct
        for e in range(num_employees):
            works = [work[e, shift, d] for d in range(num_days)]
            variables, coeffs = add_soft_sequence_constraint(
                model, works, hard_min, soft_min, min_cost, soft_max, hard_max,
                max_cost, 'shift_constraint(employee %i, shift %i)' % (e,
                                                                       shift))
            obj_bool_vars.extend(variables)
            obj_bool_coeffs.extend(coeffs)

    # Weekly sum constraints
    for ct in weekly_sum_constraints:
        shift, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost = ct
        for e in range(num_employees):
            for w in range(num_weeks):
                works = [work[e, shift, d + w * 7] for d in range(7)]
                variables, coeffs = add_soft_sum_constraint(
                    model, works, hard_min, soft_min, min_cost, soft_max,
                    hard_max, max_cost,
                    'weekly_sum_constraint(employee %i, shift %i, week %i)' %
                    (e, shift, w))
                obj_int_vars.extend(variables)
                obj_int_coeffs.extend(coeffs)

    # Penalized transitions
    for previous_shift, next_shift, cost in penalized_transitions:
        for e in range(num_employees):
            for d in range(num_days - 1):
                transition = [
                    work[e, previous_shift, d].Not(),
                    work[e, next_shift, d + 1].Not()
                ]
                if cost == 0:
                    model.AddBoolOr(transition)
                else:
                    trans_var = model.NewBoolVar(
                        'transition (employee=%i, day=%i)' % (e, d))
                    transition.append(trans_var)
                    model.AddBoolOr(transition)
                    obj_bool_vars.append(trans_var)
                    obj_bool_coeffs.append(cost)

    # Cover constraints
    for s in range(1, num_shifts):
        for w in range(num_weeks):
            for d in range(7):
                works = [work[e, s, w * 7 + d] for e in range(num_employees)]
                # Ignore Off shift.
                min_demand = weekly_cover_demands[d][s - 1]
                worked = model.NewIntVar(min_demand, num_employees, '')
                model.Add(worked == sum(works))
                over_penalty = excess_cover_penalties[s - 1]
                if over_penalty > 0:
                    name = 'excess_demand(shift=%i, week=%i, day=%i)' % (s, w,
                                                                         d)
                    excess = model.NewIntVar(0, num_employees - min_demand,
                                             name)
                    model.Add(excess == worked - min_demand)
                    obj_int_vars.append(excess)
                    obj_int_coeffs.append(over_penalty)

    # Objective
    model.Minimize(
        sum(obj_bool_vars[i] * obj_bool_coeffs[i]
            for i in range(len(obj_bool_vars)))
        + sum(obj_int_vars[i] * obj_int_coeffs[i]
              for i in range(len(obj_int_vars))))

    if output_proto:
        print('Writing proto to %s' % output_proto)
        with open(output_proto, 'w') as text_file:
            text_file.write(str(model))

    # Solve the model.
    solver = cp_model.CpSolver()
    if params:
        text_format.Merge(params, solver.parameters)
    solution_printer = cp_model.ObjectiveSolutionPrinter()
    status = solver.SolveWithSolutionCallback(model, solution_printer)

    # Print solution.
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print()
        header = '          '
        for w in range(num_weeks):
            header += 'M T W T F S S '
        print(header)
        for e in range(num_employees):
            schedule = ''
            for d in range(num_days):
                for s in range(num_shifts):
                    if solver.BooleanValue(work[e, s, d]):
                        schedule += shifts[s] + ' '
            print('worker %i: %s' % (e, schedule))
        print()
        print('Penalties:')
        for i, var in enumerate(obj_bool_vars):
            if solver.BooleanValue(var):
                penalty = obj_bool_coeffs[i]
                if penalty > 0:
                    print('  %s violated, penalty=%i' % (var.Name(), penalty))
                else:
                    print('  %s fulfilled, gain=%i' % (var.Name(), -penalty))

        for i, var in enumerate(obj_int_vars):
            if solver.Value(var) > 0:
                print('  %s violated by %i, linear penalty=%i' %
                      (var.Name(), solver.Value(var), obj_int_coeffs[i]))

    print()
    print('Statistics')
    print('  - status          : %s' % solver.StatusName(status))
    print('  - conflicts       : %i' % solver.NumConflicts())
    print('  - branches        : %i' % solver.NumBranches())
    print('  - wall time       : %f s' % solver.WallTime())


def main(args):
    
    #TODO: Generate fixed assignments and requests from DB once it's set up.
    
    # Fixed assignment: (employee, shift, day).
    # This fixes the first 2 days of the schedule.
    fixed_assignments = [
        (0, 0, 0),
        (1, 0, 0),
        (2, 1, 0),
        (3, 0, 0),
        (4, 2, 0),
        (5, 0, 0),
        (6, 0, 3),
        (7, 3, 0),
        (0, 0, 1),
        (1, 1, 1),
        (2, 0, 1),
        (3, 0, 1),
        (4, 2, 1),
        (5, 0, 1),
        (6, 0, 1),
        (7, 3, 1),
    ]


    #TODO: For moonlighters, we can just add all of their availabilities as requests here,
    #   just add a weight so they're only used when needed (maybe -3)
    
    # Request: (employee, shift, day, weight)
    # A negative weight indicates that the employee desire this assignment.
    requests = [
        # Employee 3 wants the first Saturday off.
        (3, 0, 5, -2),
        # Employee 5 wants a night shift on the second Thursday.
        (5, 3, 10, -2),
        # Employee 2 does not want a night shift on the third Friday.
        (2, 3, 4, 4)
    ]
    
    # Data from ./scheduler_config.py
    num_employees = scheduler_config.num_employees
    num_weeks = scheduler_config.num_weeks
    shifts = scheduler_config.shifts
    shift_constraints = scheduler_config.shift_constraints
    weekly_sum_constraints = scheduler_config.weekly_sum_constraints
    penalized_transitions = scheduler_config.penalized_transitions
    weekly_cover_demands = scheduler_config.weekly_cover_demands
    excess_cover_penalties = scheduler_config.excess_cover_penalties

    # Solve with requests and config
    solve_shift_scheduling(args.params, args.output_proto, num_employees, num_weeks, shifts, fixed_assignments, requests, shift_constraints,
                             weekly_sum_constraints, penalized_transitions, weekly_cover_demands, excess_cover_penalties)


if __name__ == '__main__':
    main(PARSER.parse_args())