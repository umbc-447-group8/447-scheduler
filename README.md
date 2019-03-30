# 447-scheduler
CMSC 447 Group 8 Project: Scheduling Program for John's Hopkins University

## Dependencies
* [Python3](https://www.python.org/downloads/)
* [pip](https://www.liquidweb.com/kb/install-pip-windows/)
* Flask (`pip install flask`)
* OR-Tools (`python -m pip install --user ortools`)

## Running the API server
1. Clone the repo
1. `cd api`
1. `python api.py`
1. Go to http://127.0.0.1:5000 to see homepage for the API
1. Go to http://127.0.0.1:5000/api/v1/employees to see a list of all employees 
1. Go to http://127.0.0.1:5000/api/v1/employees/{EMPLOYEE_ID} to see single employee

## Running the scheduler
1. Clone the repo
1. `cd scheduler`
1. `python scheduler.py > scheduler_log.txt`

### Some notes and TODO's for the scheduler:
* If you wish to add any changes to how it runs (like change the number of employees, weeks, etc), make these changes in the `scheduler_config.py` file in the same directory. This is where information will eventually be pulled in the end product.
* Once this is set up a bit more, moonlighters' availability will be added as requests, with a small weight so they will only be used if needed
* Right now static sample data is in `scheduler.py`, but once we get the database all set up, a way to pull from the DB and set it in the script will be implemented.
* Also right now, there is only one config for proof of concept purposes. Once we get more of the architecture set up, the config file will be generated based on whether this is scheduling for doctors or nurses
* For handling multiple locations, it may be best to conbine the cover demands for each and schedule in one go. That way, we don't have to check if an employee is already scheduled every time we find a viable schedule.
