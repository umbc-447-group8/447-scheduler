# 447-scheduler
CMSC 447 Group 8 Project: Scheduling Program for John's Hopkins University

## Dependencies
* [Python2](https://www.python.org/downloads/)
* [pip](https://www.liquidweb.com/kb/install-pip-windows/)
* Flask (`pip install flask`)
* Flask (`pip install flask-restful`)
* Flask (`pip install flask-cors`)
* OR-Tools (`python -m pip install --user ortools`)

## Running the API server
1. Clone the repo
1. `cd api`
1. `python api.py`
1. Go to http://127.0.0.1:5000 to see homepage for the API
1. Go to http://127.0.0.1:5000/api/v1/employees to see a list of all employees
1. Go to http://127.0.0.1:5000/api/v1/employees/{EMPLOYEE_ID} to see single employee
1. Go to http://127.0.0.1:5000/api/v1/keys to see a list of all keys
1. Go to http://127.0.0.1:5000/api/v1/keys/{API_KEY_ID} to see single API key
1. Go to http://127.0.0.1:5000/api/v1/locations to see a list of all locations
1. Go to http://127.0.0.1:5000/api/v1/locations/{LOCATION_ID} to see single location
1. Go to http://127.0.0.1:5000/api/v1/requests to see a list of all employee requests
1. Go to http://127.0.0.1:5000/api/v1/requests/{REQUEST_ID} to see single request

### Running the UI server
* Ensure flas-cors is installed `pip install flask-cors`
1. `cd ui`
2. `python server.py` (This script can also be passed a custom IP and port)
3. Ensure the API server is also running
4. Navigate http://localhost:8000

### Supported API Methods:
* `Get`
* `Post`
* `Put` (Must specifiy id as an endpoint)
* `Delete` (Must specifiy id as an endpoint)

### API Schemas:
**Employees:**
```
[
  {
    "employee_id": "DR001",
    "id": 0,
    "name": "Steven Strange",
    "type": "Doctor"
  },
  {
    "employee_id": "PA002",
    "id": 1,
    "name": "Claire Temple",
    "type": "PA"
  }
]
```

**API Keys:**
```
[
  {
    "id": 0,
    "key": "bfxgdsxbtgfegsvtfrsdhrshtrsht",
    "name": "testKey"
  },
  {
    "id": 1,
    "key": "gtrsgtrgt4esgt4ht",
    "name": "newkey2"
  }
]
```

**Locations:**
```
[
  {
    "coverage": [
      [1, 1, 1],
      [1, 1, 1],
      [1, 1, 1],
      [1, 1, 1],
      [1, 1, 1],
      [1, 1, 1],
      [1, 1, 1]
    ],
    "id": 0,
    "name": "Location A"
  },
  {
    "coverage": [
      [1, 1, 0],
      [1, 1, 0],
      [1, 1, 0],
      [1, 1, 0],
      [1, 1, 0],
      [1, 1, 0],
      [1, 1, 0]
    ],
    "id": 1,
    "name": "Location B"
  }
]
```

**Requests:**
```
[
  {
    "day": 3,
    "employee_id": "DR001",
    "request_id": 0,
    "shift": 0,
    "weight": -2
  },
  {
    "day": 4,
    "employee_id": "PA001",
    "request_id": 1,
    "shift": 3,
    "weight": 4
  },
  {
    "day": 57,
    "employee_id": "DR001",
    "request_id": 2,
    "shift": 1,
    "weight": -2
  }
]
```

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
