import flask
from flask import request, jsonify, Flask, render_template, current_app
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import json
import os

#get the current working directory
file_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder= file_path + "/../ui/views")
CORS(app)
api = Api(app)
app.config["DEBUG"] = True


# Get APIKeys and store into array
input_file = open(file_path + '/../data/config.json', 'r')
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
input_file = open(file_path + '/../data/employees.json', 'r')
json_array = json.load(input_file)
employees = []
for item in json_array:
    employee_details = {"id":None, "firstName":None, "lastName":None, "employee_id":None, "type":None, "moonlighter":None}
    employee_details['id'] = item['id']
    employee_details['firstName'] = item['firstName']
    employee_details['lastName'] = item['lastName']
    employee_details['employee_id'] = item['employee_id']
    employee_details['type'] = item['type']
    employee_details['moonlighter'] = item['moonlighter']
    employees.append(employee_details)
input_file.close()

# Get Locations and store into array
input_file = open(file_path + '/../data/locations.json', 'r')
json_array = json.load(input_file)
locations = []
for item in json_array:
    location_details = {"id":None, "name":None, "coverage":None}
    location_details['id'] = item['id']
    location_details['name'] = item['name']
    location_details['coverage'] = item['coverage']
    locations.append(location_details)
input_file.close()

# Get Requests and store into array
input_file = open(file_path + '/../data/requests.json', 'r')
json_array = json.load(input_file)
requests = []
for item in json_array:
    request_details = {"request_id":None, "employee_id":None, "shift":None, "day":None, "weight":None}
    request_details['request_id'] = item['request_id']
    request_details['employee_id'] = item['employee_id']
    request_details['shift'] = item['shift']
    request_details['weight'] = item['weight']
    requests.append(request_details)
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
            new_employee['firstName'] = employee_details['firstName']
            new_employee['lastName'] = employee_details['lastName']
            new_employee['employee_id'] = employee_details['employee_id']
            new_employee['type'] = employee_details['type']
            new_employee['moonlighter'] = employee_details['moonlighter']
        except:
            return {'message': 'Invalid employee data provided'}, 400
        # Save new employee
        employees.append(new_employee)

        # Save updated array to file
        output_file = open(file_path + '/../data/employees.json', 'w')
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
                result['firstName'] = employee_details['firstName']
                result['lastName'] = employee_details['lastName']
                result['type'] = employee_details['type']
                result['moonlighter'] = employee_details['moonlighter']
                output_file = open(file_path + '/../data/employees.json', 'w')
                json.dump(employees, output_file)
                output_file.close()
            # No employee found
            else:
                return "Error: No employees found with that employee_id. Please enter a valid employee_id.", 404
        except:
            return {'message': 'Invalid employee data provided'}, 400

    def delete(self, employee_id):
        result = None
        try:
            # Find employee to delete
            for employee in employees:
                if employee['employee_id'] == employee_id:
                    result = employee
            # Delete employee
            if result:
                employees.remove(result)
                output_file = open(file_path + '/../data/employees.json', 'w')
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
        output_file = open(file_path + '/../data/config.json', 'w')
        json.dump(apiKeys, output_file)
        output_file.close()

class APIKey(Resource):
    def get(self, api_key_id):
        result = None
        for key in apiKeys:
            if key['id'] == int(api_key_id):
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
                if key['id'] == int(api_key_id):
                    result = key
            # Update key
            if result:
                result['name'] = key_details['name']
                result['key'] = key_details['key']
                output_file = open(file_path + '/../data/config.json', 'w')
                json.dump(apiKeys, output_file)
                output_file.close()
            # No key found
            else:
                return "Error: No keys found with that api_key_id. Please enter a valid api_key_id.", 404
        except:
            return {'message': 'Invalid key data provided'}, 400

    def delete(self, api_key_id):
        result = None
        try:
            # Find key to delete
            for key in apiKeys:
                if key['id'] == int(api_key_id):
                    result = key
            # Delete key
            if result:
                apiKeys.remove(result)
                output_file = open(file_path + '/../data/config.json', 'w')
                json.dump(apiKeys, output_file)
                output_file.close()
            # No key found
            else:
                return "Error: No keys found with that api_key_id. Please enter a valid api_key_id.", 404
        except:
            return {'message': 'Invalid key data provided'}, 400

class Locations(Resource):
    def get(self):
        return jsonify(locations)

    def post(self):
        loc_details = request.get_json(force=True)
        # empty request
        if not loc_details:
               return {'message': 'No location data provided'}, 400
        try:
            # Ensure a unique id is assigned to new location
            loc_id = -1
            for location in locations:
                if loc_id < location['id']:
                    loc_id = location['id']
            loc_id = loc_id + 1
            # Parse request body and put into a new location
            new_location = {"id":None, "name":None, "key":None}
            new_location['id'] = loc_id
            new_location['name'] = loc_details['name']
            new_location['coverage'] = loc_details['coverage']
        # No location found
        except:
            return {'message': 'Invalid location data provided'}, 400
        # Save new location
        locations.append(new_location)

        # Save updated array to file
        output_file = open(file_path + '/../data/locations.json', 'w')
        json.dump(locations, output_file)
        output_file.close()

class Location(Resource):
    def get(self, location_id):
        result = None
        for location in locations:
            if location['id'] == int(location_id):
                result = location
            if result:
                return jsonify(result)
            else:
                return "Error: No locations found with that location_id. Please enter a valid location_id.", 404
    def put(self, location_id):
        location_details = request.get_json(force=True)
        # Empty request
        if not location_details:
               return {'message': 'No location data provided'}, 400
        result = None
        try:
            # Find location to update
            for location in locations:
                if location['id'] == int(location_id):
                    result = location
            # Update location
            if result:
                result['name'] = location_details['name']
                result['coverage'] = location_details['coverage']
                output_file = open(file_path + '/../data/locations.json', 'w')
                json.dump(locations, output_file)
                output_file.close()
            # No location found
            else:
                return "Error: No locations found with that location_id. Please enter a valid location_id.", 404
        except:
            return {'message': 'Invalid location data provided'}, 400

    def delete(self, location_id):
        result = None
        try:
            # Find location to delete
            for location in locations:
                if location['id'] == int(location_id):
                    result = location
            # Delete location
            if result:
                locations.remove(result)
                output_file = open(file_path + '/../data/locations.json', 'w')
                json.dump(locations, output_file)
                output_file.close()
            # No location found
            else:
                return "Error: No locations found with that location_id. Please enter a valid location_id.", 404
        except:
            return {'message': 'Invalid location data provided'}, 400

class Requests(Resource):
    def get(self):
        return jsonify(requests)

    def post(self):
        request_details = request.get_json(force=True)
        # empty request
        if not request_details:
               return {'message': 'No request data provided'}, 400
        try:
            # Ensure a unique id is assigned to new request
            req_id = -1
            for req in requests:
                if req_id < req['request_id']:
                    req_id = req['request_id']
            req_id = req_id + 1
            # Parse request body and put into a new request
            new_request = {"request_id":None, "employee_id":None, "shift":None, "day":None, "weight":None}
            new_request['request_id'] = req_id
            new_request['employee_id'] = request_details['employee_id']
            new_request['shift'] = request_details['shift']
            new_request['day'] = request_details['day']
            new_request['weight'] = request_details['weight']
        # No request found
        except:
            return {'message': 'Invalid request data provided'}, 400
        # Save new request
        requests.append(new_request)

        # Save updated array to file
        output_file = open(file_path + '/../data/requests.json', 'w')
        json.dump(requests, output_file)
        output_file.close()

class Request(Resource):
    def get(self, request_id):
        result = None
        for req in requests:
            if req['request_id'] == int(request_id):
                result = req
        if result:
            return jsonify(result)
        else:
            return "Error: No requests found with that request_id. Please enter a valid request_id.", 404
    def put(self, request_id):
        request_details = request.get_json(force=True)
        # Empty request
        if not request_details:
               return {'message': 'No request data provided'}, 400
        result = None
        try:
            # Find request to update
            for req in requests:
                if req['request_id'] == int(request_id):
                    result = req
            # Update request
            if result:
                result['employee_id'] = request_details['employee_id']
                result['shift'] = request_details['shift']
                result['day'] = request_details['day']
                result['weight'] = request_details['weight']
                output_file = open(file_path + '/../data/requests.json', 'w')
                json.dump(requests, output_file)
                output_file.close()
            # No request found
            else:
                return "Error: No requests found with that request_id. Please enter a valid request_id.", 404
        except:
            return {'message': 'Invalid request data provided'}, 400

    def delete(self, request_id):
        result = None
        try:
            # Find request to delete
            for req in requests:
                if req['request_id'] == int(request_id):
                    result = req
            # Delete request
            if result:
                requests.remove(result)
                output_file = open(file_path + '/../data/requests.json', 'w')
                json.dump(requests, output_file)
                output_file.close()
            # No request found
            else:
                return "Error: No requests found with that request_id. Please enter a valid request_id.", 404
        except:
            return {'message': 'Invalid request data provided'}, 400

# Homepage
api.add_resource(EmployeeList, '/api/v1/employees')
api.add_resource(Employee, '/api/v1/employees/<employee_id>')
api.add_resource(APIKeys, '/api/v1/keys')
api.add_resource(APIKey, '/api/v1/keys/<api_key_id>')
api.add_resource(Locations, '/api/v1/locations')
api.add_resource(Location, '/api/v1/locations/<location_id>')
api.add_resource(Requests, '/api/v1/requests')
api.add_resource(Request, '/api/v1/requests/<request_id>')
app.run()
