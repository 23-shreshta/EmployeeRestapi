cat > routes/employees.py << 'EOF'
from flask import Blueprint, jsonify, request
import json, os

employees_bp = Blueprint('employees', __name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/data.json')

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@employees_bp.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(load_data()['employees'])

@employees_bp.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    employees = load_data()['employees']
    emp = next((e for e in employees if e['EmployeeID'] == id), None)
    return jsonify(emp) if emp else (jsonify({'error': 'Not found'}), 404)

@employees_bp.route('/employees', methods=['POST'])
def create_employee():
    data = load_data()
    new_emp = request.get_json()
    new_emp['EmployeeID'] = max((e['EmployeeID'] for e in data['employees']), default=0) + 1
    data['employees'].append(new_emp)
    save_data(data)
    return jsonify(new_emp), 201

@employees_bp.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    data = load_data()
    emp = next((e for e in data['employees'] if e['EmployeeID'] == id), None)
    if not emp:
        return jsonify({'error': 'Not found'}), 404
    emp.update(request.get_json())
    save_data(data)
    return jsonify(emp)

@employees_bp.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    data = load_data()
    data['employees'] = [e for e in data['employees'] if e['EmployeeID'] != id]
    save_data(data)
    return jsonify({'message': 'Deleted successfully'})
EOF