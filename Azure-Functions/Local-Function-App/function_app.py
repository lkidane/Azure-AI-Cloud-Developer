import azure.functions as func
import logging
import os
from openai import AzureOpenAI
import json


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="openai_http_trigger") # openai_http_trigger is the name of the function app
def openai_http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # loading the environment variables
    azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    azure_openai_api_key = os.environ["AZURE_OPENAI_API_KEY"]
    chat_completions_model = os.environ["CHAT_COMPLETIONS_MODEL"]

    # extracting the user query from the request payload
    req_body = req.get_json()
    user_query = req_body.get("user_query") # extracts user query from the requst

    
    if user_query:
        # creating the Azure OpenAI Client 
        azure_openai_client = AzureOpenAI(
            azure_endpoint = azure_openai_endpoint,
            api_version = "2024-06-01",
            api_key = azure_openai_api_key
        )
        
        # sending a request to the chat completions model deployment
        response = azure_openai_client.chat.completions.create(
            model = chat_completions_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant"
                },
                {
                    "role": "user",
                    "content": user_query
                }
            ],
            temperature = 0.7
        )
        
        # extracting the assistant response text from the api response
        assistant_reponse_text = response.choices[0].message.content
        
        # returning the assistant response text as an http call output
        return func.HttpResponse(assistant_reponse_text)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a user_query in the query string or in the request body for a personalized response.",
             status_code=200
        )

# this is input binding feature
@app.service_bus_queue_trigger(
    arg_name="msg",
    queue_name="YOUR-SERVICE-BUS-QUEUE-NAME",
    connection="SERVICE_BUS_CONNECTION"
)
# output binding
# create a new blob or txt file in storage account
@app.blob_output(
    arg_name="outputblob",
    path="descriptions/{rand-guid}.txt", # path for the blob with randomgenerated name
    connection="STORAGE_ACCOUNT_CONNECTION"
)
# image description
def generate_image_description(
    msg: func.ServiceBusMessage,
    outputblob: func.Out[str]
):
    logging.info("Service Bus Triggered Function processed a message")
    
    # extracting the blob_url from the queue payload (gets msg from service bus queue)
    payload = json.loads(
        msg.get_body().decode("utf-8")
    )

    image_url = payload["data"]["url"] # extract image url from that msg
    
    # loading the environment variables
    azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    azure_openai_api_key = os.environ["AZURE_OPENAI_API_KEY"]
    chat_completions_model = os.environ["CHAT_COMPLETIONS_MODEL"]

    azure_openai_client = AzureOpenAI(
        azure_endpoint = azure_openai_endpoint,
        api_version = "2024-06-01",
        api_key = azure_openai_api_key
    )

    response = azure_openai_client.chat.completions.create(
        model = chat_completions_model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],
        temperature = 0.7
    )

    image_description = response.choices[0].message.content

#this create new blob container that wil contain the image description
    outputblob.set(
        image_description
    )

    logging.info(
        f"image description generated: {image_description}"
    )
