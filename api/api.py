import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create basic example of API

# Employees array for proof of concept, will be replaced with DB queries later
employees = [
    {'id': 0,
     'name': 'Steven Strange',
     'employee_id': 'DR001',
     'type': 'Doctor'},
    {'id': 1,
     'name': 'Claire Temple',
     'employee_id': 'PA002',
     'type': 'PA'}
]

# Homepage
@app.route('/', methods=['GET'])
def home():
    return '''<h1>John's Hopkins University Scheduler</h1>
<p>A prototype API for CMSC447 Group 8 scheduler project.</p>'''

#TODO: Implement way to query DB and put all employees in an array like the employees array above to display in API response

# A route to return all employees.
@app.route('/api/v1/employees/all', methods=['GET'])
def api_all():
    return jsonify(employees)

@app.route('/api/v1/employees', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'employee_id' in request.args:
        employee_id = str(request.args['employee_id'])
    else:
        return "Error: No employee_id field provided. Please specify an employee_id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for employee in employees:
        if employee['employee_id'] == employee_id:
            results.append(employee)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

app.run()