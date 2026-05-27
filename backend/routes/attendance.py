from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Attendance, LeaveRequest, Employee
from extensions import db
from datetime import datetime, date
from routes.decorators import admin_required

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/attendances', methods=['GET'])
@jwt_required()
def get_attendances():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    employee_id = request.args.get('employee_id', type=int)
    date_str = request.args.get('date', '')

    query = Attendance.query
    if employee_id:
        query = query.filter_by(employee_id=employee_id)
    if date_str:
        query = query.filter_by(date=datetime.strptime(date_str, '%Y-%m-%d').date())

    pagination = query.order_by(Attendance.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'code': 200,
        'data': {
            'items': [a.to_dict() for a in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
        }
    })


@attendance_bp.route('/attendances/checkin', methods=['POST'])
@jwt_required()
def check_in():
    data = request.get_json()
    employee_id = data.get('employee_id')
    if not employee_id:
        return jsonify({'code': 400, 'msg': '请选择员工'}), 400

    today = date.today()
    existing = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
    if existing:
        return jsonify({'code': 400, 'msg': '今日已签到'}), 400

    now = datetime.now()
    status = '迟到' if now.hour >= 9 else '正常'
    attendance = Attendance(
        employee_id=employee_id,
        date=today,
        check_in=now,
        status=status,
    )
    db.session.add(attendance)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '签到成功', 'data': attendance.to_dict()})


@attendance_bp.route('/attendances/checkout', methods=['POST'])
@jwt_required()
def check_out():
    data = request.get_json()
    employee_id = data.get('employee_id')
    if not employee_id:
        return jsonify({'code': 400, 'msg': '请选择员工'}), 400

    today = date.today()
    attendance = Attendance.query.filter_by(employee_id=employee_id, date=today).first()
    if not attendance:
        return jsonify({'code': 400, 'msg': '今日未签到'}), 400

    now = datetime.now()
    attendance.check_out = now
    if now.hour < 18:
        attendance.status = '早退' if attendance.status == '正常' else attendance.status
    db.session.commit()
    return jsonify({'code': 200, 'msg': '签退成功', 'data': attendance.to_dict()})


@attendance_bp.route('/attendances/leave', methods=['POST'])
@jwt_required()
def apply_leave():
    data = request.get_json()
    leave = LeaveRequest(
        employee_id=data.get('employee_id'),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
        reason=data.get('reason', ''),
    )
    db.session.add(leave)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '请假申请已提交', 'data': leave.to_dict()})


@attendance_bp.route('/attendances/leave', methods=['GET'])
@jwt_required()
def get_leaves():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', '')

    query = LeaveRequest.query
    if status:
        query = query.filter_by(status=status)

    pagination = query.order_by(LeaveRequest.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'code': 200,
        'data': {
            'items': [l.to_dict() for l in pagination.items],
            'total': pagination.total,
        }
    })


@attendance_bp.route('/attendances/leave/<int:pk>/approve', methods=['PUT'])
@jwt_required()
@admin_required
def approve_leave(pk):
    leave = LeaveRequest.query.get_or_404(pk)
    data = request.get_json()
    action = data.get('action', 'approved')
    leave.status = action

    if action == 'approved':
        from datetime import timedelta
        current = leave.start_date
        while current <= leave.end_date:
            existing = Attendance.query.filter_by(employee_id=leave.employee_id, date=current).first()
            if not existing:
                att = Attendance(
                    employee_id=leave.employee_id,
                    date=current,
                    status='请假',
                )
                db.session.add(att)
            current += timedelta(days=1)

    db.session.commit()
    return jsonify({'code': 200, 'msg': '操作成功', 'data': leave.to_dict()})
