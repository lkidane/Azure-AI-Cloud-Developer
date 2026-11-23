import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import Flask-CORS
from openai import AzureOpenAI

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

#take the secrets as environment variables
# Read configuration from environment variables
AZURE_OPENAI_ENDPOINT = os.environ.get("azure-api-url")
AZURE_OPENAI_API_KEY = os.environ.get("azure-api-key")
AZURE_OPENAI_MODEL_NAME = os.environ.get("azure-model-name")
AZURE_OPENAI_API_VERSION = os.environ.get("azure-api-version", "2024-12-01-preview")

#create azure openai client
client = AzureOpenAI(
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
)

#exposes a /chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
        model=AZURE_OPENAI_MODEL_NAME,
    )

   #json response from the model
    return jsonify({
        "model": response.model,
        "reply": response.choices[0].message.content
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




# from azure.identity import DefaultAzureCredential
# from azure.mgmt.appcontainers import ContainerAppsAPIClient   

# client = ContainerAppsAPIClient(DefaultAzureCredential(), subscription_id="id")
# for env in client.managed_environments.list_by_resource_group("rg-aca-demo"):
#     logs = env.app_logs_configuration.destnation if env.app_logs_configuration else None
#     print(env.name, env.location, env.default_domain, "logs:", logs)
#     for wp in env.workload_profiles or []:
#         print("prfile:", wp.name, wp.workload_profile_type)



# # pip install azure-identity azure-keyvault-secrets
# import os
# from azure.identity import DefaultAzureCredential
# from azure.keyvault.secrets import SecretClient

# # Option 1: read Key Vault directly. No client_id/secret/tenant in code.
# client = SecretClient(vault_url="https://my-demo-kv.vault.azure.net/",
#                       credential=DefaultAzureCredential())
# db_password = client.get_secret("DatabasePassword").value

# # Option 2: Container Apps injected it via secretref
# db_password_env = os.environ["DATABASE_PASSWORD"]
# log_level = os.getenv("LOG_LEVEL", "info")
 
        
