from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Salary
from extensions import db
from routes.decorators import admin_required

salary_bp = Blueprint('salary', __name__)


@salary_bp.route('/salaries', methods=['GET'])
@jwt_required()
def get_salaries():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    employee_id = request.args.get('employee_id', type=int)
    month = request.args.get('month', '')
    status = request.args.get('status', '')

    query = Salary.query
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    if month:
        query = query.filter_by(month=month)
    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(Salary.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'code': 200,
        'data': {
            'items': [s.to_dict() for s in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
        }
    })


@salary_bp.route('/salaries', methods=['POST'])
@jwt_required()
@admin_required
def create_salary():
    data = request.get_json()
    base_salary = data.get('base_salary', 0)
    bonus = data.get('bonus', 0)
    deduction = data.get('deduction', 0)

    salary = Salary(
        employee_id=data.get('employee_id'),
        month=data.get('month'),
        base_salary=base_salary,
        bonus=bonus,
        deduction=deduction,
        total=base_salary + bonus - deduction,
        status=data.get('status', '未发放'),
    )
    db.session.add(salary)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '创建成功', 'data': salary.to_dict()})


@salary_bp.route('/salaries/<int:pk>', methods=['PUT'])
@jwt_required()
@admin_required
def update_salary(pk):
    salary = Salary.query.get_or_404(pk)
    data = request.get_json()
    for field in ['base_salary', 'bonus', 'deduction', 'status', 'month', 'employee_id']:
        if field in data:
            setattr(salary, field, data[field])
    salary.total = salary.base_salary + salary.bonus - salary.deduction
    db.session.commit()
    return jsonify({'code': 200, 'msg': '更新成功', 'data': salary.to_dict()})


@salary_bp.route('/salaries/<int:pk>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_salary(pk):
    salary = Salary.query.get_or_404(pk)
    db.session.delete(salary)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '删除成功'})


@salary_bp.route('/salaries/<int:pk>/pay', methods=['PUT'])
@jwt_required()
@admin_required
def pay_salary(pk):
    salary = Salary.query.get_or_404(pk)
    salary.status = '已发放'
    db.session.commit()
    return jsonify({'code': 200, 'msg': '发放成功', 'data': salary.to_dict()})
