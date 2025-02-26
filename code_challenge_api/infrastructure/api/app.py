# infrastructure/api/app.py
from flask import Flask

from infrastructure.api.controllers.employee_controller import employee_blueprint
from infrastructure.api.controllers.job_controller import job_blueprint
from infrastructure.api.controllers.department_controller import department_blueprint

app = Flask(__name__)

app.register_blueprint(employee_blueprint, url_prefix='/api')
app.register_blueprint(job_blueprint, url_prefix='/api')
app.register_blueprint(department_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)