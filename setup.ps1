Clear-Host
write-host "Starting deployment at $(Get-Date)"

#Set-PSRepository -Name PSGallery -InstallationPolicy Trusted

# Generate unique random suffix
[string]$suffix =  -join ((48..57) + (97..122) | Get-Random -Count 7 | % {[char]$_})
Write-Host "Your randomly-generated suffix for Azure resources is $suffix"

# parameters
$subscriptionId = ""
$resourceGroupName = "code-challenge-resource-group"
$region = "East US"
$sqlServerName = "ccsqlserver$suffix"
$sqlDatabaseName = "ccsqldatabase"
$sqlUser = "sqladmin"
$containerRegistryName = "cccontainerregistry$suffix"
$containerImageRegistryName = "ccapicr:v1"
$containerInstanceName = "cccontainerinstance"
$containerName = "cc-api-container" 

# Set azure subscription
$subscriptions = Get-AzSubscription | Where-Object { $_.State -eq "Enabled" }

if ($subscriptions.Count -eq 1) {
    Select-AzSubscription -SubscriptionId $subscriptions.Name
    az account set --subscription $subscriptions.Name
    Write-Host "Subscription to be used for deployment: $($subscriptions.Name)"
    $subscriptionId = $subscriptions.Id
}
else {
    Write-Host "Available subscriptions" -ForegroundColor Green
    for ($i = 0; $i -lt $subscriptions.Count; $i++) {
        Write-Host "$($i + 1). $($subscriptions[$i].Name) (ID: $($subscriptions[$i].Id))"
    }
    $subscription_name = Read-Host "Please, type subscription name you want to use for deployment..."
    
    Select-AzSubscription -SubscriptionId $subscription_name
    az account set --subscription $subscription_name

    $subscriptionId = (Get-AzSubscription | Where-Object { $_.Name -eq $subscription_name}).Id
}

# Password for the database
while ($complexPassword -ne 1)
{
    $SqlPassword = Read-Host "Enter a password to use for the $sqlUser login.
    `The password must meet complexity requirements:
    ` - Minimum 8 characters. 
    ` - At least one upper case English letter [A-Z]
    ` - At least one lower case English letter [a-z]
    ` - At least one digit [0-9]
    ` - At least one special character (!,@,#,%,^,&,$)
    ` "

    if(($SqlPassword -cmatch '[a-z]') -and ($SqlPassword -cmatch '[A-Z]') -and ($SqlPassword -match '\d') -and ($SqlPassword.length -ge 8) -and ($SqlPassword -match '!|@|#|%|\^|&|\$'))
    {
        $complexPassword = 1
	    Write-Output "Password $SqlPassword accepted. Make sure you remember this!"
        $databaseStringConnection = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:$sqlServerName.database.windows.net,1433;Database=$sqlDatabaseName;Uid=$sqlUser;Pwd=$SqlPassword;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
        
    }
    else
    {
        Write-Output "$SqlPassword does not meet the complexity requirements."
    }
}

# Register resource providers
Write-Host "Registering resource providers...";
$provider_list = "Microsoft.Sql", "Microsoft.ContainerRegistry", "Microsoft.ContainerInstance"
$maxRetries = 5
$waittime = 30

foreach ($provider in $provider_list) {
    $retryCount = 0
    Register-AzResourceProvider -ProviderNamespace $provider
    while ($retryCount -lt $maxRetries) {
        $currentStatus = (Get-AzResourceProvider -ProviderNamespace $provider).RegistrationState
        if ($currentStatus -eq "Registered") {
            Write-Host "$provider is successfully registered."
            break
        }
        else {
            Write-Host "$provider is not yet registered. Waiting for $waitTime seconds before rechecking..."
            Start-Sleep -Seconds $waitTime
            $retryCount++
        }
    }
    if ($retryCount -eq $maxRetries) {
        Write-Host "Failed to register $provider after $maxRetries attempts."
    }
}


# Create resource group
Write-Host "Creating $resourceGroupName resource group in $region ..."
New-AzResourceGroup -Name $resourceGroupName -Location $region | Out-Null

# Deployment
write-host "Creating resources in $resourceGroupName resource group..."
write-host "This may take some time!"
New-AzResourceGroupDeployment -ResourceGroupName $resourceGroupName `
  -TemplateFile "setup.json" `
  -Mode Complete `
  -sqlServerName $sqlServerName `
  -sqlDatabaseName $sqlDatabaseName `
  -sqlUser $sqlUser `
  -sqlPassword $sqlPassword `
  -Force

# Create tables into the database
Start-Sleep -Seconds 30 # Wait for server and database
write-host "Creating the $sqlDatabaseName database..."
sqlcmd -S "$sqlServerName.database.windows.net" -U $sqlUser -P $sqlPassword -d $sqlDatabaseName -I -i setup.sql

# Create a Container Registry
Start-Sleep -Seconds 30
write-host "Creating the $containerRegistryName container registry..."
New-AzContainerRegistry -ResourceGroupName $resourceGroupName -Name $containerRegistryName -Sku "Standard" -AnonymousPullEnabled -Location $region

# Build image
Start-Sleep -Seconds 30
write-host "Starting image deployment to the $containerRegistryName container registry..."
az acr build --registry $containerRegistryName --image $containerImageRegistryName --file "./src/dockerfile" "./src"

# Container instance
Start-Sleep -Seconds 30
write-host "Creating the $containerName container..."
Connect-AzContainerRegistry -Name $containerRegistryName
Start-Sleep -Seconds 10
az container create --resource-group $resourceGroupName --name $containerName --image "$containerRegistryName.azurecr.io/$containerImageRegistryName" --registry-username "registryAdmin" --registry-password $sqlPassword --dns-name-label "$containerName-$containerRegistryName" --env DATABASE_ODBC_CONNECTION_STRING=$databaseStringConnection --os-type "Linux" --cpu 1 --memory 1 --query "{FQDN:ipAddress.fqdn}" --output table

write-host "Deployment process finished!"

# Tests
write-host "Starting tests..."
Start-Sleep -Seconds 15
write-host "Getting container IP Address..."
$ipAddress = (az container show --resource-group $resourceGroupName --name $containerName | ConvertFrom-Json).IpAddress
$publicIp = $ipAddress.ip
$base_url = $ipAddress.fqdn
$port = $ipAddress.ports[0].port

write-host "URL: $base_url"
write-host "Public IP: $publicIp:$port"


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
write-host Invoke-RestMethod -Uri "http://$($base_url):$port/api/departments" -Method Post -Headers $headers -Body $body
Invoke-RestMethod -Uri "http://$($base_url):$port/api/departments" -Method Post -Headers $headers -Body $body

# GET
write-host "GET"
Start-Sleep -Seconds 3
write-host Invoke-WebRequest -Uri "http://$($base_url):$port/api/departments" -Method Get
Invoke-WebRequest -Uri "http://$($base_url):$port/api/departments" -Method Get

# DELETE
write-host "DELETE"
Start-Sleep -Seconds 3
$body = '[1, 2, 3]'
$headers = @{"Content-Type" = "application/json"}
write-host Invoke-RestMethod -Uri "http://$($base_url):$port/api/departments" -Method Delete -Headers $headers -Body $body
Invoke-RestMethod -Uri "http://$($base_url):$port/api/departments" -Method Delete -Headers $headers -Body $body


# Jobs
write-host "Jobs..."
Start-Sleep -Seconds 3

# POST
write-host "POST"
Start-Sleep -Seconds 3
$body = '[[1,"Office Assistant IV"], [2,"Financial Analyst"], [3,"Electrical Engineer"]]'
$headers = @{"Content-Type" = "application/json"}
write-host Invoke-RestMethod -Uri "http://$($base_url):$port/api/jobs" -Method Post -Headers $headers -Body $body
Invoke-RestMethod -Uri "http://$($base_url):$port/api/jobs" -Method Post -Headers $headers -Body $body

# GET
write-host "GET"
Start-Sleep -Seconds 3
write-host Invoke-WebRequest -Uri "http://$($base_url):$port/api/jobs" -Method Get
Invoke-WebRequest -Uri "http://$($base_url):$port/api/jobs" -Method Get

# DELETE
write-host "DELETE"
Start-Sleep -Seconds 3
$body = '[1, 2, 3]'
$headers = @{"Content-Type" = "application/json"}
write-host Invoke-RestMethod -Uri "http://$($base_url):$port/api/jobs" -Method Delete -Headers $headers -Body $body
Invoke-RestMethod -Uri "http://$($base_url):$port/api/jobs" -Method Delete -Headers $headers -Body $body



# Employees
write-host "Employees..."
Start-Sleep -Seconds 3

# POST
write-host "POST"
Start-Sleep -Seconds 3
$body = '[[1,"Harold Vogt","2021-11-07T02:48:42Z",2,96], [2,"Ty Hofer","2021-05-30T05:43:46Z",8,null], [3,"Lyman Hadye","2021-09-01T23:27:38Z",5,52]]'
$headers = @{"Content-Type" = "application/json"}
write-host Invoke-RestMethod -Uri "http://$($base_url):$port/api/employees" -Method Post -Headers $headers -Body $body
Invoke-RestMethod -Uri "http://$($base_url):$port/api/employees" -Method Post -Headers $headers -Body $body

# GET
write-host "GET"
Start-Sleep -Seconds 3
write-host Invoke-WebRequest -Uri "http://$($base_url):$port/api/employees" -Method Get
Invoke-WebRequest -Uri "http://$($base_url):$port/api/employees" -Method Get

# DELETE
write-host "DELETE"
Start-Sleep -Seconds 3
$body = '[1, 2, 3]'
$headers = @{"Content-Type" = "application/json"}
write-host Invoke-RestMethod -Uri "http://$($base_url):$port/api/employees" -Method Delete -Headers $headers -Body $body
Invoke-RestMethod -Uri "http://$($base_url):$port/api/employees" -Method Delete -Headers $headers -Body $body


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
write-host Invoke-RestMethod -Uri "http://$($base_url):$port/api/departments/csvfile" -Method Post -Headers "headers" -Body "body"
Invoke-RestMethod -Uri "http://$($base_url):$port/api/departments/csvfile" -Method Post -Headers $headers -Body $body

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
write-host Invoke-RestMethod -Uri "http://$($base_url):$port/api/jobs/csvfile" -Method Post -Headers "headers" -Body "body"
Invoke-RestMethod -Uri "http://$($base_url):$port/api/jobs/csvfile" -Method Post -Headers $headers -Body $body

# Jobs
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
write-host Invoke-RestMethod -Uri "http://$($base_url):$port/api/employee/csvfile" -Method Post -Headers "headers" -Body "body"
Invoke-RestMethod -Uri "http://$($base_url):$port/api/employee/csvfile" -Method Post -Headers $headers -Body $body

# Analysis
write-host "Analysis..."
Start-Sleep -Seconds 3

# Section 2 - Requirement 1
write-host "Section 2 - Requirement 1"
Start-Sleep -Seconds 3
write-host Invoke-WebRequest -Uri "http://$($base_url):$port/api/req1/2021" -Method Get
Invoke-WebRequest -Uri "http://$($base_url):$port/api/req1/2021" -Method Get

# Section 2 - Requirement 1
write-host "Section 2 - Requirement 2"
Start-Sleep -Seconds 3
write-host Invoke-WebRequest -Uri "http://$($base_url):$port/api/req1/2021" -Method Get
Invoke-WebRequest -Uri "http://$($base_url):$port/api/req1/2021" -Method Get