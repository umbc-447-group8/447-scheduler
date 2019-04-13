import flask
from flask import request, jsonify, Flask
from flask_restful import reqparse, abort, Api, Resource
import json

app = Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True

# Get APIKeys and store into array
input_file = open('..\data\config.json', 'r')
json_array = json.load(input_file)
apiKeys = []
for item in json_array:
    key_details = {"id":None, "name":None, "key":None}
    key_details['id'] = item['id']
    key_details['name'] = item['name']
    key_details['key'] = item['key']
    apiKeys.append(key_details)
input_file.close()

# Get Employees and store into array
input_file = open('..\data\employees.json', 'r')
json_array = json.load(input_file)
employees = []
for item in json_array:
    employee_details = {"id":None, "name":None, "employee_id":None, "type":None}
    employee_details['id'] = item['id']
    employee_details['name'] = item['name']
    employee_details['employee_id'] = item['employee_id']
    employee_details['type'] = item['type']
    employees.append(employee_details)
input_file.close()

# Employees classes
class EmployeeList(Resource):
    def get(self):
        return jsonify(employees)

    def post(self):
        employee_details = request.get_json(force=True)
        # empty request
        if not employee_details:
               return {'message': 'No employee data provided'}, 400
        # Ensure a unique id is assigned to new employee
        try:
            emp_id = -1
            for employee in employees:
                if emp_id < employee['id']:
                    emp_id = employee['id']
                if employee_details['employee_id'] == employee['employee_id']:
                    raise Exception('Provided employee_id already exists')
            emp_id = emp_id + 1 
            # Parse request body and put into a new employee
            new_employee = {"id":None, "name":None, "employee_id":None, "type":None}
            new_employee['id'] = emp_id
            new_employee['name'] = employee_details['name']
            new_employee['employee_id'] = employee_details['employee_id']
            new_employee['type'] = employee_details['type']
        except: 
            return {'message': 'Invalid employee data provided'}, 400
        # Save new employee
        employees.append(new_employee)
        
        # Save updated array to file
        output_file = open('..\data\employees.json', 'w')
        json.dump(employees, output_file)
        output_file.close()

class Employee(Resource):
    def get(self, employee_id):
        result = None
        for employee in employees:
            if employee['employee_id'] == employee_id:
                result = employee
        if result:
            return jsonify(result)
        else:
            return "Error: No employee found with that employee_id. Please enter a valid employee_id.", 404
    
    def put(self, employee_id):
        employee_details = request.get_json(force=True)
        # Empty request
        if not employee_details:
               return {'message': 'No employee data provided'}, 400
        result = None
        try:
            # Find employee to update
            for employee in employees:
                if employee['employee_id'] == employee_id:
                    result = employee
            # Update employee
            if result:
                result['name'] = employee_details['name']
                result['type'] = employee_details['type']
                output_file = open('..\data\employees.json', 'w')
                json.dump(employees, output_file)
                output_file.close()
            # No employee found
            else:
                return "Error: No employees found with that employee_id. Please enter a valid employee_id.", 404
        except:
            return {'message': 'Invalid employee data provided'}, 400

class APIKeys(Resource):
    def get(self):
        return jsonify(apiKeys)
    
    def post(self):
        key_details = request.get_json(force=True)
        # empty request
        if not key_details:
               return {'message': 'No key data provided'}, 400
        try:
            # Ensure a unique id is assigned to new key
            key_id = -1
            for key in apiKeys:
                if key_id < key['id']:
                    key_id = key['id']
            key_id = key_id + 1
            # Parse request body and put into a new key
            new_key = {"id":None, "name":None, "key":None}
            new_key['id'] = key_id
            new_key['name'] = key_details['name']
            new_key['key'] = key_details['key']
        # No key found
        except: 
            return {'message': 'Invalid key data provided'}, 400
        # Save new key
        apiKeys.append(new_key)
        
        # Save updated array to file
        output_file = open('..\data\config.json', 'w')
        json.dump(apiKeys, output_file)
        output_file.close()

class APIKey(Resource):
    def get(self, api_key_id):
        result = None
        for key in apiKeys:
            if key['id'] == api_key_id:
                result = key
            if result:
                return jsonify(result)
            else:
                return "Error: No keys found with that api_key_id. Please enter a valid api_key_id.", 404
    def put(self, api_key_id):
        key_details = request.get_json(force=True)
        # Empty request
        if not key_details:
               return {'message': 'No key data provided'}, 400
        result = None
        try:
            # Find key to update
            for key in apiKeys:
                if key['id'] == api_key_id:
                    result = key
            # Update key
            if result:
                result['name'] = key_details['name']
                result['key'] = key_details['key']
                output_file = open('..\data\config.json', 'w')
                json.dump(apiKeys, output_file)
                output_file.close()
            # No key found
            else:
                return "Error: No keys found with that api_key_id. Please enter a valid api_key_id.", 404
        except:
            return {'message': 'Invalid key data provided'}, 400



# Homepage
@app.route('/', methods=['GET'])
def home():
    return '''<h1>John's Hopkins University Scheduler</h1>
<p>A prototype API for CMSC447 Group 8 scheduler project.</p>'''

#TODO: Implement way to query DB and put all employees in an array like the employees array above to display in API response  
    
api.add_resource(EmployeeList, '/api/v1/employees')
api.add_resource(Employee, '/api/v1/employees/<employee_id>')
api.add_resource(APIKeys, '/api/v1/keys')
api.add_resource(APIKey, '/api/v1/keys/<api_key_id>')
app.run()