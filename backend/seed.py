"""初始化测试数据"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app
from extensions import db
from models import User, Department, Employee, Attendance, Salary, LeaveRequest
from datetime import datetime, date, timedelta
import random


def seed():
    app = create_app()
    with app.app_context():
        # 清空现有数据
        db.drop_all()
        db.create_all()

        # 创建管理员
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)

        # 创建普通用户
        user1 = User(username='zhangsan', role='employee')
        user1.set_password('123456')
        db.session.add(user1)
        db.session.flush()

        # 创建部门
        departments = [
            Department(name='技术部', description='负责产品开发和技术维护'),
            Department(name='市场部', description='负责市场推广和品牌建设'),
            Department(name='人事部', description='负责人员招聘和行政管理'),
            Department(name='财务部', description='负责公司财务管理和预算'),
            Department(name='运营部', description='负责日常运营管理'),
        ]
        db.session.add_all(departments)
        db.session.flush()

        # 创建员工
        names = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十',
                 '郑冬梅', '冯春花', '陈夏雨', '楚秋风', '卫冬雪', '蒋明辉',
                 '韩晓丽', '杨光耀', '朱晓红', '秦大力', '许小明', '何芳华']
        positions = ['工程师', '产品经理', '设计师', '测试', '前端开发', '后端开发',
                     '市场专员', '人事专员', '会计', '运营专员', '项目经理', '实习生']

        employees = []
        for i, name in enumerate(names):
            dept = departments[i % len(departments)]
            pos = positions[i % len(positions)]
            emp = Employee(
                name=name,
                gender='男' if i % 3 != 2 else '女',
                phone=f'138{i:08d}',
                email=f'emp{i:02d}@company.com',
                position=pos,
                department_id=dept.id,
                hire_date=date(2024, random.randint(1, 12), random.randint(1, 28)),
                status='在职',
                user_id=user1.id if i == 0 else None,
            )
            employees.append(emp)
        db.session.add_all(employees)
        db.session.flush()

        # 创建考勤数据（最近30天）
        for emp in employees:
            for day_offset in range(30):
                d = date.today() - timedelta(days=day_offset)
                if d.weekday() >= 5:  # 周末跳过
                    continue
                roll = random.random()
                if roll < 0.05:
                    continue  # 5% 缺勤
                check_in_hour = 8 + random.randint(0, 2)
                check_in_min = random.randint(0, 59)
                check_out_hour = 17 + random.randint(0, 2)
                status = '迟到' if check_in_hour >= 9 and check_in_min > 30 else '正常'
                att = Attendance(
                    employee_id=emp.id,
                    date=d,
                    check_in=datetime(d.year, d.month, d.day, check_in_hour, check_in_min),
                    check_out=datetime(d.year, d.month, d.day, check_out_hour, random.randint(0, 59)),
                    status=status,
                )
                db.session.add(att)

        # 创建薪资数据
        months = ['2025-10', '2025-11', '2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-05']
        for emp in employees:
            base = random.choice([6000, 8000, 10000, 12000, 15000, 20000])
            for month in months:
                bonus = random.randint(0, 3000)
                deduction = random.randint(0, 500)
                salary = Salary(
                    employee_id=emp.id,
                    month=month,
                    base_salary=base,
                    bonus=bonus,
                    deduction=deduction,
                    total=base + bonus - deduction,
                    status='已发放' if month != months[-1] else random.choice(['已发放', '未发放']),
                )
                db.session.add(salary)

        # 创建请假记录
        for i in range(5):
            emp = random.choice(employees)
            leave = LeaveRequest(
                employee_id=emp.id,
                start_date=date.today() + timedelta(days=random.randint(1, 30)),
                end_date=date.today() + timedelta(days=random.randint(31, 35)),
                reason=random.choice(['年假', '病假', '事假', '调休']),
                status=random.choice(['pending', 'approved', 'rejected']),
            )
            db.session.add(leave)

        db.session.commit()
        print('测试数据初始化成功！')
        print(f'管理员账号: admin / admin123')
        print(f'普通用户: zhangsan / 123456')
        print(f'部门数量: {len(departments)}')
        print(f'员工数量: {len(employees)}')


if __name__ == '__main__':
    seed()
