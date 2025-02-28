@echo off

:: URL base
set base_url=http://cc-api-container-cccontainerregistryk0p41f2.eastus.azurecontainer.io:80
::set base_url=http://localhost:80

:: departments
::curl -X POST %base_url%/api/departments -H "Content-Type: application/json" -d "[[2025,\"HR\"], [2026,\"HR2\"], [2027,\"HR3\"]]"
::curl -X POST -F "file=@departments.csv" %base_url%/api/departments/csvfile
curl -X GET %base_url%/api/departments
::curl -X DELETE %base_url%/api/departments -H "Content-Type: application/json" -d "[2025, 2026, 2027]"

:: jobs
::curl -X POST %base_url%/api/jobs -H "Content-Type: application/json" -d "[[2025,\"Job2025\"], [2026,\"Job2026\"], [2027,\"Job2027\"]]"
::curl -X POST -F "file=@jobs.csv" %base_url%/api/jobs/csvfile
curl -X GET %base_url%/api/jobs
::curl -X DELETE %base_url%/api/jobs -H "Content-Type: application/json" -d "[2025, 2026, 2027]"

:: employees
::curl -X POST %base_url%/api/employees -H "Content-Type: application/json" -d "[[2025,\"Wilmer\",\"2025-02-26\",1,3], [2026,null,\"2025-02-26\",1,3], [2027,\"Wilmer\",\"2025-02-26\",null,3]]"
::curl -X POST -F "file=@hired_employees_test.csv" %base_url%/api/employees/csvfile
curl -X GET %base_url%/api/employees
::curl -X DELETE %base_url%/api/employees -H "Content-Type: application/json" -d "[2025, 2026, 2027]"

:: analysis
curl -X GET %base_url%/api/req1/2021
curl -X GET %base_url%/api/req2/2021

pause
