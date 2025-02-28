# parameters
$resourceGroupName = "code-challenge-resource-group"
$region = "East US"
$containerRegistryName = "cccontainerregistry6r8acbg"
$containerImageRegistryName = "ccapicr:v1"
$containerInstanceName = "cccontainerinstance"
$containerName = "cc-api-container"
$databaseStringConnection = "Mystring"

$akv_name = "code-challenge-api-akv"

az keyvault create --resource-group $resourceGroupName --name $akv_name

# Create service principal, store its password in AKV (the registry *password*)
az keyvault secret set --vault-name $akv_name --name "$containerRegistryName-pull-pwd" --value $(az ad sp create-for-rbac --name "$containerRegistryName-pull" --scopes $(az acr show --name $containerRegistryName --query id --output tsv) --role acrpull --query password --output tsv)

# Store service principal ID in AKV (the registry *username*)
az keyvault secret set --vault-name $containerRegistryName --name $containerRegistryName-pull-usr --value $(az ad sp list --display-name $containerRegistryName-pull --query [].appId --output tsv)

az container create --resource-group $resourceGroupName --name "acr-tasks" --image "$containerRegistryName.azurecr.io/$containerImageRegistryName" --registry-login-server $containerRegistryName.azurecr.io --registry-username $(az keyvault secret show --vault-name $akv_name --name "$containerRegistryName-pull-usr" --query value -o tsv) --registry-password $(az keyvault secret show --vault-name $akv_name --name "$containerRegistryName-pull-pwd" --query value -o tsv) --dns-name-label "acr-tasks-$containerRegistryName" --env DATABASE_ODBC_CONNECTION_STRING=$databaseStringConnection --query "{FQDN:ipAddress.fqdn}" --output table