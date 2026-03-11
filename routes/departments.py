from flask import Blueprint, jsonify, request
import json, os

departments_bp = Blueprint('departments', __name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/data.json')

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@departments_bp.route('/departments', methods=['GET'])
def get_departments():
    return jsonify(load_data()['departments'])

@departments_bp.route('/departments/<int:id>', methods=['GET'])
def get_department(id):
    depts = load_data()['departments']
    dept = next((d for d in depts if d['DepartmentID'] == id), None)
    return jsonify(dept) if dept else (jsonify({'error': 'Not found'}), 404)

@departments_bp.route('/departments', methods=['POST'])
def create_department():
    data = load_data()
    new_dept = request.get_json()
    new_dept['DepartmentID'] = max((d['DepartmentID'] for d in data['departments']), default=0) + 1
    data['departments'].append(new_dept)
    save_data(data)
    return jsonify(new_dept), 201

@departments_bp.route('/departments/<int:id>', methods=['PUT'])
def update_department(id):
    data = load_data()
    dept = next((d for d in data['departments'] if d['DepartmentID'] == id), None)
    if not dept:
        return jsonify({'error': 'Not found'}), 404
    dept.update(request.get_json())
    save_data(data)
    return jsonify(dept)

@departments_bp.route('/departments/<int:id>', methods=['DELETE'])
def delete_department(id):
    data = load_data()
    data['departments'] = [d for d in data['departments'] if d['DepartmentID'] != id]
    save_data(data)
    return jsonify({'message': 'Deleted successfully'})