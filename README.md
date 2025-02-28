# Data Engineering Coding Challenge API
**REST Python Flask API**
This API runs in a Azure Container Instance, provides functionality to load data from csv files to a Azure SQL database.

## Development
Development proccess took place in a Windows 10 environment, making use of the following tools and services:

    - Visual Studio Code
    - GitHub
    - Python 3
    - Flask 2.3.2
    - Docker

## Project architechture
**![screenshot](/arch.png)**

## API bsed on Hexagonal architechture

```
.
├── src/ 
│   ├── domain/
│   │   ├── models/
│   │   └── ports/
│   │
│   ├── app/
│   │   └── use_cases/
│   │
│   ├── infrastructure/ 
│   │   ├── adapters/
│   │   ├── controllers/
│   │   └── database/
│   │
│   ├── tests/
│   │
│   ├── app.py
│   ├── dockerfile
│   └── requirements.txt
│   
└── README.md
```

## Deploy using Azure Cloud Services
Repo includes a ps1 file **(setup.ps1)** for automated deploying of the SQL server and database, Container registration and building using Azure services and tools like:
    
    - Azure SQL Database
    - Azure Container Registry
    - Azure Container Instance
    - Azure Resource Manager templates
    - Azure PowerShell scripting

### Prerequisites
    - An active Azure Subscription
    - Basic PowerShell scripting and Git knowledge

### Azure Deployment process and test
A .ps1 file was included for automated deployment and test, at the end of the correct deployment you will see each endpoint test.

1. Go to [Azure Portal](https://portal.azure.com/) and Log In
2. Open Azure Cloud Shell using the button at the top-right of the azure portal and wait for successfully started.
3. run `rm -r code-challenge -f` to remove previous folder if exists
4. Clone this repository using `git clone https://github.com/wherrmat/data-engineering-coding-challenge-repo code-challenge`
5. Move to the main directory using `cd code-challenge`
6. Run the automated deployment using `./setup.ps1`
7. Await for the deployment process
8. After deployment process, then an automated test will take place
9. At the end of the test process you will see the public IP for API use
10. If you want to re-run test, use `./src/tests/azure-powershell-test.ps1`
11. A .bat file was included in ./src/tests/ with some CURL queries you can use for testing the API

Deployment proccess will take some time, you will be able to se some outputs with status, please, note the following:
    
    - At the first deployment attempt, Providers Registration will take place and it could rise an error, just re-try
    - If mora than one Azure Subscription is active in your directory, the proccess will request you to type the name of a specific subscripcion for the deployment
    - A Password aligned with specific requirements will be required for SQL Login in the Azure SQL Database, keep it.
    - Yout public IP is not added automatically to the Azure SQL Server Firewall Rules
    - If any of the resources deployment process rise a Failure, please delete the resource group and re-try the deployment
    - If you want to see some API run logs on cloud shell terminal, you could use next command
        `az container attach --resource-group "code-challenge-resource-group" --name "cc-api-container"`

## SQL database
The database for this project is automatically created during the deployment process and using **setup.sql** file for the Azure SQL Database service, and following tables will be incorporated

### Employees - [dbo].[hired_employees]
| Field         | Type       | Description            |
|---------------|------------|------------------------|
| id            | int        | ID of the employee     |
| name          | string     | Name of the employee   |
| datetime      | string     | Hiring date and time   |
| department_id | int        | ID of the department   |
| job_id        | int        | ID of the job          |

### Departments - [dbo].[hired_employees]
| Field         | Type       | Description            |
|---------------|------------|------------------------|
| id            | int        | ID of the department   |
| department    | string     | Name of the department |

### Jobs - [dbo].[jobs]
| Field         | Type       | Description            |
|---------------|------------|------------------------|
| id            | int        | ID of the job          |
| job           | string     | Name of the job        |


## API Use

This API expose endpoints on Container Instance URL on **port 80** for Create, Read and Delete records over three previous tables, an Enpoint to upload records from CSV files for each table. Also expose two Endpoints to get specific data analysis.

- Base URL will depends on the Container Instance resource, and it will by provided at the end of the cloud shell proccess deployment, it should looks like `cc-api-container-cccontainerregistryxxxxxxx.eastus.azurecontainer.io`, you also could put the url in a browser to see if the API was successfully deployed

**Endpoints and Methods**

***Section 1 - API***

**To write, read and delete records using a list in JSON boy request**
- http://<url-base>:80/api/employees (GET, POST, DELETE)
- http://<url-base>:80/api/departments (GET, POST, DELETE)
- http://<url-base>:80/api/jobs (GET, POST, DELETE)

**To load records from a CSV files, limited to a maximum of 1000 records and at least one**
- http://<url-base>:80/api/employees/csvfile (POST)
- http://<url-base>:80/api/departments/csvfile (POST)
- http://<url-base>:80/api/jobs/csvfile (POST)


**Data Analysis Endpoints**

To get data of two specific analysis. It is neccesary to provide the year you want to analyse


**Get number of employees hired for each job and department by a year, divided by quarter.**

- http://<url-base>:80/api/req1/<int:year> (GET)

***Query for Section 2 - Requirement 1***

```
select
    d.department as department, 
    j.job as job,
    sum(case when datepart(quarter, cast(datetime as DATETIME)) between 1 and 3 THEN 1 else 0 end) as q1,
    sum(case when datepart(quarter, cast(datetime as DATETIME)) between 4 and 6 THEN 1 else 0 end) as q2,
    sum(case when datepart(quarter, cast(datetime as DATETIME)) between 7 and 9 THEN 1 else 0 end) as q3,
    sum(case when datepart(quarter, cast(datetime as DATETIME)) between 10 and 12 THEN 1 else 0 end) as q4
from [dbo].[hired_employees] e
join [dbo].[departments] d on e.department_id = d.id
join [dbo].[jobs] j on e.job_id = j.id
where year(cast(datetime as DATETIME)) = ?
group by department, job order by department, job;
```


**Get a list of ids, name and number of employees hired of each department, greater than the mean of employees hired in a year for all the departments**

- http://<url-base>:80/api/req2/<int:year> (GET)

***Query for Section 2 - Requirement 2***

```
with employees_count as (
    select department_id, count(id) as num_employees
    from [dbo].[hired_employees]
    where year(cast(datetime as DATETIME)) = ?
    group by department_id
),
average_hired as (
    select top 1 avg(num_employees) over() as mean_hired from employees_count
)
select
    ec.department_id as id,
    d.department as department,
    ec.num_employees as hired
from employees_count ec
cross join average_hired ah
join [dbo].[departments] d on ec.department_id=d.id
where ec.num_employees > ah.mean_hired
order by ec.num_employees desc;
```

**CURL query models**
Consider the path to csv local files "file=@path/file.csv"

### departments

```
curl -X POST %base_url%/api/departments -H "Content-Type: application/json" -d "[[2025,\"HR\"], [2026,\"HR2\"], [2027,\"HR3\"]]"
curl -X POST -F "file=@departments.csv" %base_url%/api/departments/csvfile
curl -X GET %base_url%/api/departments
curl -X DELETE %base_url%/api/departments -H "Content-Type: application/json" -d "[2025, 2026, 2027]"
```

### jobs
```
curl -X POST %base_url%/api/jobs -H "Content-Type: application/json" -d "[[2025,\"Job2025\"], [2026,\"Job2026\"], [2027,\"Job2027\"]]"
curl -X POST -F "file=@jobs.csv" %base_url%/api/jobs/csvfile
curl -X GET %base_url%/api/jobs
curl -X DELETE %base_url%/api/jobs -H "Content-Type: application/json" -d "[2025, 2026, 2027]"
```
### employees
```
curl -X POST %base_url%/api/employees -H "Content-Type: application/json" -d "[[2025,\"Wilmer\",\"2025-02-26\",1,3], [2026,null,\"2025-02-26\",1,3], [2027,\"Wilmer\",\"2025-02-26\",null,3]]"
curl -X POST -F "file=@hired_employees_test.csv" %base_url%/api/employees/csvfile
curl -X GET %base_url%/api/employees
curl -X DELETE %base_url%/api/employees -H "Content-Type: application/json" -d "[2025, 2026, 2027]"
```

### analysis
```
curl -X GET %base_url%/api/req1/2021
curl -X GET %base_url%/api/req2/2021
```

## Contact

**If you have any questions or suggestions, please contact me:**

- email: [wilmeryes96@yahoo.es]