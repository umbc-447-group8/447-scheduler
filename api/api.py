#!/usr/bin/env python
import scheduler
import flask
from flask import request, jsonify, Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
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

# Class to define GET
class EmployeeList(Resource):
    def get(self):
        return jsonify(employees)
class Employee(Resource):
    def get(self, employee_id):
        for employee in employees:
            if employee['employee_id'] == employee_id:
                result = employee
            if result:
                return jsonify(result)
            else:
                return "Error: No employee found with that employee_id. Please enter a valid employee_id.", 404



# Homepage
@app.route('/', methods=['GET'])
def home():
    return '''<h1>John's Hopkins University Scheduler</h1>
<p>A prototype API for CMSC447 Group 8 scheduler project.</p>'''

#TODO: Implement way to query DB and put all employees in an array like the employees array above to display in API response  
    
api.add_resource(EmployeeList, '/api/v1/employees')
api.add_resource(Employee, '/api/v1/employees/<employee_id>')
app.run()

scheduler.main()