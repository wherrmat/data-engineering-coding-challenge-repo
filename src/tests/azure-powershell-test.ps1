$resourceGroupName = "code-challenge-resource-group"
$containerName = "cc-api-container" 


# Tests
write-host "Starting tests..."
Start-Sleep -Seconds 3
write-host "Getting container URL, IP and port..."
$ipAddress = (az container show --resource-group $resourceGroupName --name $containerName | ConvertFrom-Json).IpAddress
$publicIp = $ipAddress.ip
$baseUrl = $ipAddress.fqdn
$port = $ipAddress.ports[0].port

write-host "URL: $baseUrl"
write-host "Public IP: $($publicIp):$port"
Start-Sleep -Seconds 3


write-host "Starting test..."
Start-Sleep -Seconds 3

# Departments
write-host "Departments..."
Start-Sleep -Seconds 3

# POST
write-host "POST"
Start-Sleep -Seconds 3
$body = '[[1,"Human Resources"], [2,"TI"], [3,"People"]]'
$headers = @{"Content-Type" = "application/json"}
write-host Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/departments" -Method Post -Headers $headers -Body $body
Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/departments" -Method Post -Headers $headers -Body $body

# GET
write-host "GET"
Start-Sleep -Seconds 3
write-host Invoke-WebRequest -Uri "http://$($baseUrl):$port/api/departments" -Method Get
Invoke-WebRequest -Uri "http://$($baseUrl):$port/api/departments" -Method Get | ConvertFrom-Json

# DELETE
write-host "DELETE"
Start-Sleep -Seconds 3
$body = '[1, 2, 3]'
$headers = @{"Content-Type" = "application/json"}
write-host Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/departments" -Method Delete -Headers $headers -Body $body
Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/departments" -Method Delete -Headers $headers -Body $body


# Jobs
write-host "Jobs..."
Start-Sleep -Seconds 3

# POST
write-host "POST"
Start-Sleep -Seconds 3
$body = '[[1,"Office Assistant IV"], [2,"Financial Analyst"], [3,"Electrical Engineer"]]'
$headers = @{"Content-Type" = "application/json"}
write-host Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/jobs" -Method Post -Headers $headers -Body $body
Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/jobs" -Method Post -Headers $headers -Body $body

# GET
write-host "GET"
Start-Sleep -Seconds 3
write-host Invoke-WebRequest -Uri "http://$($baseUrl):$port/api/jobs" -Method Get
Invoke-WebRequest -Uri "http://$($baseUrl):$port/api/jobs" -Method Get | ConvertFrom-Json

# DELETE
write-host "DELETE"
Start-Sleep -Seconds 3
$body = '[1, 2, 3]'
$headers = @{"Content-Type" = "application/json"}
write-host Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/jobs" -Method Delete -Headers $headers -Body $body
Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/jobs" -Method Delete -Headers $headers -Body $body



# Employees
write-host "Employees..."
Start-Sleep -Seconds 3

# POST
write-host "POST"
Start-Sleep -Seconds 3
$body = '[[1,"Harold Vogt","2021-11-07T02:48:42Z",2,96], [2,"Ty Hofer","2021-05-30T05:43:46Z",8,null], [3,"Lyman Hadye","2021-09-01T23:27:38Z",5,52]]'
$headers = @{"Content-Type" = "application/json"}
write-host Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/employees" -Method Post -Headers $headers -Body $body
Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/employees" -Method Post -Headers $headers -Body $body

# GET
write-host "GET"
Start-Sleep -Seconds 3
write-host Invoke-WebRequest -Uri "http://$($baseUrl):$port/api/employees" -Method Get
Invoke-WebRequest -Uri "http://$($baseUrl):$port/api/employees" -Method Get | ConvertFrom-Json

# DELETE
write-host "DELETE"
Start-Sleep -Seconds 3
$body = '[1, 2, 3]'
$headers = @{"Content-Type" = "application/json"}
write-host Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/employees" -Method Delete -Headers $headers -Body $body
Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/employees" -Method Delete -Headers $headers -Body $body


# Load csv files
write-host "Load csv files..."
Start-Sleep -Seconds 3

# Departments
# POST load csv file
write-host "Departments..."
Start-Sleep -Seconds 3
$fileName = "departments.csv"
$filePath = "./src/tests/data/$fileName"
$fileContent = Get-Content -Path $filePath -Raw

$boundary = [System.Guid]::NewGuid().ToString()
$bodyLines = @(
    "--$boundary"
    "Content-Disposition: form-data; name=`"file`"; filename=`"$fileName`""
    "Content-Type: text/csv"
    ""
    $fileContent
    "--$boundary--"
)
$body = $bodyLines -join "`r`n"
$headers = @{"Content-Type" = "multipart/form-data; boundary=$boundary"}
write-host Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/departments/csvfile" -Method Post -Headers "headers" -Body "body"
Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/departments/csvfile" -Method Post -Headers $headers -Body $body

# Jobs
# POST load csv file
write-host "Jobs..."
Start-Sleep -Seconds 3
$fileName = "jobs.csv"
$filePath = "./src/tests/data/$fileName"
$fileContent = Get-Content -Path $filePath -Raw

$boundary = [System.Guid]::NewGuid().ToString()
$bodyLines = @(
    "--$boundary"
    "Content-Disposition: form-data; name=`"file`"; filename=`"$fileName`""
    "Content-Type: text/csv"
    ""
    $fileContent
    "--$boundary--"
)
$body = $bodyLines -join "`r`n"
$headers = @{"Content-Type" = "multipart/form-data; boundary=$boundary"}
write-host Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/jobs/csvfile" -Method Post -Headers "headers" -Body "body"
Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/jobs/csvfile" -Method Post -Headers $headers -Body $body

# Employees
# POST load csv file
write-host "Employees..."
Start-Sleep -Seconds 3
$fileName = "hired_employees.csv"
$filePath = "./src/tests/data/$fileName"
$fileContent = Get-Content -Path $filePath -Raw

$boundary = [System.Guid]::NewGuid().ToString()
$bodyLines = @(
    "--$boundary"
    "Content-Disposition: form-data; name=`"file`"; filename=`"$fileName`""
    "Content-Type: text/csv"
    ""
    $fileContent
    "--$boundary--"
)
$body = $bodyLines -join "`r`n"
$headers = @{"Content-Type" = "multipart/form-data; boundary=$boundary"}
write-host Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/employees/csvfile" -Method Post -Headers "headers" -Body "body"
Invoke-RestMethod -Uri "http://$($baseUrl):$port/api/employees/csvfile" -Method Post -Headers $headers -Body $body

# Analysis
write-host "Analysis..."
Start-Sleep -Seconds 3

# Section 2 - Requirement 1
write-host "Section 2 - Requirement 1"
Start-Sleep -Seconds 3
write-host Invoke-WebRequest -Uri "http://$($baseUrl):$port/api/req1/2021" -Method Get
Invoke-WebRequest -Uri "http://$($baseUrl):$port/api/req1/2021" -Method Get | ConvertFrom-Json

# Section 2 - Requirement 1
write-host "Section 2 - Requirement 2"
Start-Sleep -Seconds 3
write-host Invoke-WebRequest -Uri "http://$($baseUrl):$port/api/req2/2021" -Method Get
Invoke-WebRequest -Uri "http://$($baseUrl):$port/api/req2/2021" -Method Get | ConvertFrom-Json