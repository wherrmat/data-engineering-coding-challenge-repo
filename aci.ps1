# parameters
$resourceGroupName = "code-challenge-resource-group"
$region = "East US"
$containerRegistryName = "cccontainerregistry6r8acbg"
$containerImageRegistryName = "ccapicr:v1"
$containerInstanceName = "cccontainerinstance"
$containerName = "cc-api-container"
$databaseStringConnection = "Mystring"

Connect-AzAccount
Connect-AzContainerRegistry

az container create --resource-group $resourceGroupName --name $containerInstanceName --image "$containerRegistryName.azurecr.io/$containerImageRegistryName" 
    --env DATABASE_ODBC_CONNECTION_STRING=$databaseStringConnection --dns-name-label "acr-tasks-$containerRegistryName" --query "{FQDN:ipAddress.fqdn}" --output table