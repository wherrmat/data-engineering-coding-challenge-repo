Clear-Host
write-host "Starting deployment at $(Get-Date)"

#Set-PSRepository -Name PSGallery -InstallationPolicy Trusted

# Generate unique random suffix
[string]$suffix =  -join ((48..57) + (97..122) | Get-Random -Count 7 | % {[char]$_})
Write-Host "Your randomly-generated suffix for Azure resources is $suffix"

# parameters
$resourceGroupName = "code-challenge-resource-group"
$region = "East US"
$storageAccountName = "ccstorageaccount$suffix"
$containerName = "data"
$sqlServerName = "ccsqlserver$suffix"
$sqlDatabaseName = "ccsqldatabase"
$sqlUser = "sqladmin"


# Set azure subscription
$subscriptions = Get-AzSubscription | Where-Object { $_.State -eq "Enabled" }

if ($subscriptions.Count -eq 1) {
    Select-AzSubscription -SubscriptionId $subscriptions.Name
    az account set --subscription $subscriptions.Name
    Write-Host "Subscription to be used for deployment: $($subscriptions.Name)"
}
else {
    Write-Host "Available subscriptions" -ForegroundColor Green
    for ($i = 0; $i -lt $subscriptions.Count; $i++) {
        Write-Host "$($i + 1). $($subscriptions[$i].Name) (ID: $($subscriptions[$i].Id))"
    }
    $subscription_name = Read-Host "Please, type subscription name you want to use for deployment..."
    
    Select-AzSubscription -SubscriptionId $subscription_name
    az account set --subscription $subscription_name
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
    }
    else
    {
        Write-Output "$SqlPassword does not meet the complexity requirements."
    }
}

# Register resource providers
Write-Host "Registering resource providers...";
$provider_list = "Microsoft.Sql", "Microsoft.Storage"
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
  -storageAccountName $storageAccountName `
  -containerName $containerName `
  -sqlServerName $sqlServerName `
  -sqlDatabaseName $sqlDatabaseName `
  -sqlUser $sqlUser `
  -sqlPassword $sqlPassword `
  -Force


# Create storage account
#Write-Host "Creating $storageAccountName storage account ..."
#New-AzStorageAccount -ResourceGroupName $resourceGroupName `
#    -Name $storageAccountName `
#    -Location $region `
#    -SkuName Standard_LRS

# Upload files
write-host "Loading data..."
$storageAccount = Get-AzStorageAccount -ResourceGroupName $resourceGroupName -Name $storageAccountName
$storageContext = $storageAccount.Context
Get-ChildItem "./data/*.csv" -File | Foreach-Object {
    write-host ""
    $file = $_.Name
    Write-Host $file
    $blobPath = "data/$file"
    Set-AzStorageBlobContent -File $_.FullName -Container "files" -Blob $blobPath -Context $storageContext
}

# Create Azure SQL Server
#Write-Host "Creating $sqlServerName SQL server ..."
#New-AzSqlServer -ResourceGroupName $resourceGroupName `
#    -ServerName $sqlServerName `
#    -Location $region `
#    -SqlAdministratorCredentials (Get-Credential -UserName $sqlAdminLogin -Password $SqlPassword)

# Create Azure SQL database
#Write-Host "Creating $sqlDatabaseName database in $sqlServerName SQL server ..."
#New-AzSqlDatabase -ResourceGroupName $resourceGroupName `
#    -ServerName $sqlServerName `
#    -DatabaseName $sqlDatabaseName `
#    -Edition Basic

# Create database
write-host "Creating the $sqlDatabaseName database..."
sqlcmd -S "$sqlServerName.database.windows.net" -U $sqlUser -P $sqlPassword -d $sqlDatabaseName -I -i setup.sql