# infrastructure/database/database.py
import pyodbc
from azure.identity import DefaultAzureCredential
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

class Database:

    # Connect to database
    def __init__(self, key_vault_url, secret_name):
        self.connection_string = self._get_connection_string_from_keyvault(key_vault_url, secret_name)   
        
        self.connection = pyodbc.connect(self.connection_string)
        self.cursor = self.connection.cursor()
    
    # Get string connection from Azure Key Vault
    def _get_connection_string_from_keyvault(self, key_vault_url, secret_name):
        credential = DefaultAzureCredential()
        credential = ManagedIdentityCredential() # Azure web service managed identity needs to be configured and role permissions granted
        secret_client = SecretClient(vault_url=key_vault_url, credential=credential)
        secret = secret_client.get_secret(secret_name)
        return secret.value

    # Execute a sql query
    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.connection.commit()

    # Execute a sql query and return all rows
    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    # Close database connection
    def close(self):
        self.cursor.close()
        self.connection.close()