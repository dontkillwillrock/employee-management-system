from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Employee, Department, User
from extensions import db
from datetime import datetime
from routes.decorators import admin_required

employee_bp = Blueprint('employee', __name__)


@employee_bp.route('/employees', methods=['GET'])
@jwt_required()
def get_employees():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    name = request.args.get('name', '')
    department_id = request.args.get('department_id', type=int)
    status = request.args.get('status', '')

    query = Employee.query
    if name:
        query = query.filter(Employee.name.contains(name))
    if department_id:
        query = query.filter_by(department_id=department_id)
    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(Employee.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'code': 200,
        'data': {
            'items': [e.to_dict() for e in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
        }
    })


@employee_bp.route('/employees', methods=['POST'])
@jwt_required()
@admin_required
def create_employee():
    data = request.get_json()
    employee = Employee(
        name=data.get('name'),
        gender=data.get('gender', '男'),
        phone=data.get('phone', ''),
        email=data.get('email', ''),
        position=data.get('position', ''),
        department_id=data.get('department_id'),
        hire_date=datetime.strptime(data['hire_date'], '%Y-%m-%d').date() if data.get('hire_date') else datetime.utcnow().date(),
        status=data.get('status', '在职'),
    )
    db.session.add(employee)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '创建成功', 'data': employee.to_dict()})


@employee_bp.route('/employees/<int:pk>', methods=['GET'])
@jwt_required()
def get_employee(pk):
    employee = Employee.query.get_or_404(pk)
    return jsonify({'code': 200, 'data': employee.to_dict()})


@employee_bp.route('/employees/<int:pk>', methods=['PUT'])
@jwt_required()
@admin_required
def update_employee(pk):
    employee = Employee.query.get_or_404(pk)
    data = request.get_json()
    for field in ['name', 'gender', 'phone', 'email', 'position', 'department_id', 'status']:
        if field in data:
            setattr(employee, field, data[field])
    if 'hire_date' in data and data['hire_date']:
        employee.hire_date = datetime.strptime(data['hire_date'], '%Y-%m-%d').date()
    db.session.commit()
    return jsonify({'code': 200, 'msg': '更新成功', 'data': employee.to_dict()})


@employee_bp.route('/employees/<int:pk>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_employee(pk):
    employee = Employee.query.get_or_404(pk)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '删除成功'})


@employee_bp.route('/employees/all', methods=['GET'])
@jwt_required()
def get_all_employees():
    employees = Employee.query.filter_by(status='在职').all()
    return jsonify({'code': 200, 'data': [e.to_dict() for e in employees]})


@employee_bp.route('/employees/<int:pk>/account', methods=['POST'])
@jwt_required()
@admin_required
def create_employee_account(pk):
    """为员工创建登录账号"""
    employee = Employee.query.get_or_404(pk)
    if employee.user_id:
        return jsonify({'code': 400, 'msg': '该员工已有登录账号'})

    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'code': 400, 'msg': '用户名和密码不能为空'})

    if User.query.filter_by(username=username).first():
        return jsonify({'code': 400, 'msg': '用户名已存在'})

    user = User(username=username, role='employee')
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    employee.user_id = user.id
    db.session.commit()

    return jsonify({'code': 200, 'msg': '账号创建成功', 'data': {'user_id': user.id, 'username': username}})


@employee_bp.route('/employees/<int:pk>/account', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_employee_account(pk):
    """删除员工登录账号"""
    employee = Employee.query.get_or_404(pk)
    if not employee.user_id:
        return jsonify({'code': 400, 'msg': '该员工没有登录账号'})

    user = User.query.get(employee.user_id)
    if user and user.role == 'admin':
        return jsonify({'code': 400, 'msg': '不能删除管理员账号'})

    employee.user_id = None
    if user:
        db.session.delete(user)
    db.session.commit()

    return jsonify({'code': 200, 'msg': '账号删除成功'})
