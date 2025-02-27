@echo off
:: departments
::curl -X POST http://localhost:5000/api/departments -H "Content-Type: application/json" -d "[[2025,\"HR\"], [2026,\"HR2\"], [2027,\"HR3\"]]"
::curl -X POST -F "file=@departments.csv" http://localhost:5000/api/departments/csvfile
::curl -X GET http://localhost:5000/api/departments
::curl -X DELETE http://localhost:5000/api/departments -H "Content-Type: application/json" -d "[2025, 2026, 2027]"

:: jobs
::curl -X POST http://localhost:5000/api/jobs -H "Content-Type: application/json" -d "[[2025,\"Job2025\"], [2026,\"Job2026\"], [2027,\"Job2027\"]]"
::curl -X POST -F "file=@jobs.csv" http://localhost:5000/api/jobs/csvfile
::curl -X GET http://localhost:5000/api/jobs
::curl -X DELETE http://localhost:5000/api/jobs -H "Content-Type: application/json" -d "[2025, 2026, 2027]"

:: employees
::curl -X POST http://localhost:5000/api/employees -H "Content-Type: application/json" -d "[[2025,\"Wilmer\",\"2025-02-26\",1,3], [2026,null,\"2025-02-26\",1,3], [2027,\"Wilmer\",\"2025-02-26\",null,3]]"
::curl -X POST -F "file=@hired_employees_test.csv" http://localhost:5000/api/employees/csvfile
::curl -X GET http://localhost:5000/api/employees
::curl -X DELETE http://localhost:5000/api/employees -H "Content-Type: application/json" -d "[2025, 2026, 2027]"

:: analysis
::curl -X GET http://localhost:5000/api/req1/2021
curl -X GET http://localhost:5000/api/req2/2021

pause
