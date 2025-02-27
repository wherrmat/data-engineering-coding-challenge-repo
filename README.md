# data-engineering-coding-challenge-repo
REST API for data migration and SQL analysis

## Endpoints

### Jobs
- /api/job

### Departments
- /api/department


### Employees
- /api/employee

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