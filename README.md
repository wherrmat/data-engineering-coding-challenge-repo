# data-engineering-coding-challenge-repo
REST API for data migration and SQL analysis

## Endpoints and curl querie models

### /api/departments
- curl -X POST <base-url>/api/departments -H "Content-Type: application/json" -d "[[1,\"Human Resources\"], [2,\"TI\"], [3,\"People\"]]"
- curl -X POST -F "file=@path/file.csv" <base-url>/api/departments/csvfile
- curl -X GET <base-url>/api/departments
- curl -X DELETE <base-url>/api/departments -H "Content-Type: application/json" -d "[1, 2, 3]"

### /api/jobs
- curl -X POST <base-url>/api/jobs -H "Content-Type: application/json" -d "[[1,\"Technical Lead\"], [2,\"Developper\"], [3,\"Scrum master\"]]"
- curl -X POST -F "file=@jobs.csv" <base-url>/api/jobs/csvfile
- curl -X GET <base-url>/api/jobs
- curl -X DELETE <base-url>/api/jobs -H "Content-Type: application/json" -d "[2025, 2026, 2027]"

### /api/employees
- curl -X POST <base-url>/api/employees -H "Content-Type: application/json" -d "[[2025,\"Wilmer\",\"2025-02-26\",1,3], [2026,null,\"2025-02-26\",1,3], [2027,\"Wilmer\",\"2025-02-26\",null,3]]"
- curl -X POST -F "file=@hired_employees_test.csv" <base-url>/api/employees/csvfile
- curl -X GET <base-url>/api/employees
- curl -X DELETE <base-url>/api/employees -H "Content-Type: application/json" -d "[2025, 2026, 2027]"

## Deployment
1. Clone the repo using next Azure PowerShell commands
    - rm -r code-challenge -f
    - git clone https://github.com/wherrmat/data-engineering-coding-challenge-repo code-challenge
2. Run setup file for deployment with commands
    - cd code-challenge
    - ./setup.ps1
3. Specify the subscription name (if required)
4. Specify a password for the database aligned with the requirements
5. If you require, you can add a firewall rule to sql server with your public ip addres, so you will be able to query the server directly