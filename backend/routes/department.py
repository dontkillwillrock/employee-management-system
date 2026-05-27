from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Department
from extensions import db
from routes.decorators import admin_required

department_bp = Blueprint('department', __name__)


@department_bp.route('/departments', methods=['GET'])
@jwt_required()
def get_departments():
    departments = Department.query.order_by(Department.id).all()
    return jsonify({'code': 200, 'data': [d.to_dict() for d in departments]})


@department_bp.route('/departments', methods=['POST'])
@jwt_required()
@admin_required
def create_department():
    data = request.get_json()
    department = Department(
        name=data.get('name', ''),
        description=data.get('description', ''),
    )
    db.session.add(department)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '创建成功', 'data': department.to_dict()})


@department_bp.route('/departments/<int:pk>', methods=['PUT'])
@jwt_required()
@admin_required
def update_department(pk):
    department = Department.query.get_or_404(pk)
    data = request.get_json()
    if 'name' in data:
        department.name = data['name']
    if 'description' in data:
        department.description = data['description']
    db.session.commit()
    return jsonify({'code': 200, 'msg': '更新成功', 'data': department.to_dict()})


@department_bp.route('/departments/<int:pk>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_department(pk):
    department = Department.query.get_or_404(pk)
    if department.employees.count() > 0:
        return jsonify({'code': 400, 'msg': '该部门下有员工，无法删除'}), 400
    db.session.delete(department)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '删除成功'})
