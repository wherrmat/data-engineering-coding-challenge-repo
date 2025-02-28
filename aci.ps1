# parameters
$resourceGroupName = "code-challenge-resource-group"
$region = "East US"
$containerRegistryName = "cccontainerregistry6r8acbg"
$containerImageRegistryName = "ccapicr:v1"
$containerInstanceName = "cccontainerinstance"
$containerName = "cc-api-container"
$databaseStringConnection = "Mystring"

$akv_name = "code-challenge-api-akv"


# Set azure subscription
$subscriptions = Get-AzSubscription | Where-Object { $_.State -eq "Enabled" }

if ($subscriptions.Count -eq 1) {
    Select-AzSubscription -SubscriptionId $subscriptions.Name
    az account set --subscription $subscriptions.Name
    Write-Host "Subscription to be used for deployment: $($subscriptions.Name)"
    $subscriptionId = $subscriptions.Id
}

Connect-AzContainerRegistry
az container create --resource-group $resourceGroupName --name "acr-tasks" --image "$containerRegistryName.azurecr.io/$containerImageRegistryName" --dns-name-label "acr-tasks-$containerRegistryName" --env DATABASE_ODBC_CONNECTION_STRING=$databaseStringConnection --os-type "Linux" --cpu 1 --memory 1 --query "{FQDN:ipAddress.fqdn}" --output table