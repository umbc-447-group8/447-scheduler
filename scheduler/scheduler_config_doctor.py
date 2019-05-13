# scheduler_config.py
# File that stores configurations for generating the schedule. Imported into scheduler.py.
#-N = Nursery location
def __init__(self):
        resp = request.get('http://127.0.0.1:5000/api/v1/employees')
        if resp.status_code != 200:
            # This means something went wrong.
            raise ApiError('GET /tasks/ {}'.format(resp.status_code))
        counter = 0
        for eOb in resp.json():
            counter += 1
        self.num_employees = counter
        
num_weeks = 13 #assuming quarterly
shifts = ['O', 'M-ER', 'A-ER', 'N-ER', 'M-N', 'A-N']

# Shift constraints on continuous sequence :
#     (shift, hard_min, soft_min, min_penalty,
#             soft_max, hard_max, max_penalty)
shift_constraints = [
    # One or two consecutive days of rest, this is a hard constraint.
    (0, 1, 1, 0, 2, 2, 0),
    # betweem 2 and 3 consecutive days of night shifts, 1 and 4 are
    # possible but penalized.
    (3, 1, 2, 20, 3, 4, 5),
]

# Weekly sum constraints on shifts days:
#     (shift, hard_min, soft_min, min_penalty,
#             soft_max, hard_max, max_penalty)
weekly_sum_constraints = [
    # Constraints on rests per week. At least 1 rest per week. At most 3 rests per week.
    (0, 1, 2, 7, 2, 3, 4),
    # # At least 1 night shift per week (penalized). At most 4 (hard).
    # (3, 0, 1, 3, 4, 4, 0),
]

# Penalized transitions:
#     (previous_shift, next_shift, penalty (0 means forbidden))
penalized_transitions = [
    # Morning to night is forbidden.
    (1, 3, 0),
    (4, 3, 0)
    # Morning to afternoon is forbidden.
    (1, 2, 0),
    (4, 5, 0),
    (4, 3, 0),
    (1, 5, 0)
    # Afternoon to night is forbidden.
    (2, 3, 0),
    (5, 3, 0),
    # Night to morning is forbidden.
    (3, 1, 0),
    (3, 4, 0),
]

# daily demands for work shifts (morning, afternon, night, morning @ nursery, afternoon @ nursery) for each day
# of the week starting on Monday.
# One location only needs to be covered during the day, hence the 2s in morning and afternoon
weekly_cover_demands = [
    (1, 1, 1, 1, 1),  # Monday
    (1, 1, 1, 1, 1),  # Tuesday
    (1, 1, 1, 1, 1),  # Wednesday
    (1, 1, 1, 1, 1),  # Thursday
    (1, 1, 1, 1, 1),  # Friday
    (1, 1, 1, 1, 1),  # Saturday
    (1, 1, 1, 1, 1),  # Sunday
]

# Penalty for exceeding the cover constraint per shift type.
excess_cover_penalties = (2, 2, 5)