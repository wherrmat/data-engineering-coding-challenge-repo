# src/app.py
from dotenv import load_dotenv
from flask import Flask

# enviromental variables
load_dotenv()

from infrastructure.controllers.employee_controller import employee_blueprint
from infrastructure.controllers.job_controller import job_blueprint
from infrastructure.controllers.department_controller import department_blueprint
from infrastructure.controllers.analysis_controller import analysis_blueprint

app = Flask(__name__)

app.register_blueprint(employee_blueprint, url_prefix='/api')
app.register_blueprint(job_blueprint, url_prefix='/api')
app.register_blueprint(department_blueprint, url_prefix='/api')
app.register_blueprint(analysis_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    #app.run(debug=True)