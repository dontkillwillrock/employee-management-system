from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models import Employee, Department, Attendance, Salary
from extensions import db
from sqlalchemy import func
from datetime import date

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
def get_stats():
    # 基本统计
    total_employees = Employee.query.filter_by(status='在职').count()
    total_departments = Department.query.count()

    # 今日考勤
    today = date.today()
    today_checked = Attendance.query.filter_by(date=today).count()
    today_late = Attendance.query.filter_by(date=today, status='迟到').count()

    # 部门人员分布
    dept_stats = db.session.query(
        Department.name,
        func.count(Employee.id)
    ).outerjoin(Employee, (Employee.department_id == Department.id) & (Employee.status == '在职')
    ).group_by(Department.id).all()

    # 薪资统计
    total_salary_paid = db.session.query(func.sum(Salary.total)).filter_by(status='已发放').scalar() or 0
    total_salary_unpaid = db.session.query(func.sum(Salary.total)).filter_by(status='未发放').scalar() or 0

    # 近 6 个月薪资趋势
    salary_trend = db.session.query(
        Salary.month,
        func.sum(Salary.total)
    ).group_by(Salary.month).order_by(Salary.month.desc()).limit(6).all()

    return jsonify({
        'code': 200,
        'data': {
            'total_employees': total_employees,
            'total_departments': total_departments,
            'today_checked': today_checked,
            'today_late': today_late,
            'dept_distribution': [{'name': name, 'value': count} for name, count in dept_stats],
            'total_salary_paid': total_salary_paid,
            'total_salary_unpaid': total_salary_unpaid,
            'salary_trend': [{'month': m, 'total': t} for m, t in salary_trend],
        }
    })
