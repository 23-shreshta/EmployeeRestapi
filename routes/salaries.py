from flask import Blueprint, jsonify, request
import json, os

salaries_bp = Blueprint('salaries', __name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/data.json')

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@salaries_bp.route('/salaries', methods=['GET'])
def get_salaries():
    return jsonify(load_data()['salaries'])

@salaries_bp.route('/salaries/<int:id>', methods=['GET'])
def get_salary(id):
    salaries = load_data()['salaries']
    sal = next((s for s in salaries if s['SalaryID'] == id), None)
    return jsonify(sal) if sal else (jsonify({'error': 'Not found'}), 404)

@salaries_bp.route('/salaries', methods=['POST'])
def create_salary():
    data = load_data()
    new_sal = request.get_json()
    new_sal['SalaryID'] = max((s['SalaryID'] for s in data['salaries']), default=0) + 1
    data['salaries'].append(new_sal)
    save_data(data)
    return jsonify(new_sal), 201

@salaries_bp.route('/salaries/<int:id>', methods=['PUT'])
def update_salary(id):
    data = load_data()
    sal = next((s for s in data['salaries'] if s['SalaryID'] == id), None)
    if not sal:
        return jsonify({'error': 'Not found'}), 404
    sal.update(request.get_json())
    save_data(data)
    return jsonify(sal)

@salaries_bp.route('/salaries/<int:id>', methods=['DELETE'])
def delete_salary(id):
    data = load_data()
    data['salaries'] = [s for s in data['salaries'] if s['SalaryID'] != id]
    save_data(data)
    return jsonify({'message': 'Deleted successfully'})