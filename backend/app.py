from flask import Flask
from config import Config
from extensions import db, jwt, cors, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    migrate.init_app(app, db)

    # 注册蓝图
    from routes.auth import auth_bp
    from routes.employee import employee_bp
    from routes.department import department_bp
    from routes.attendance import attendance_bp
    from routes.salary import salary_bp
    from routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(employee_bp, url_prefix='/api')
    app.register_blueprint(department_bp, url_prefix='/api')
    app.register_blueprint(attendance_bp, url_prefix='/api')
    app.register_blueprint(salary_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api')

    # 创建数据库表
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
