import os
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel

model = AzureAIChatCompletionsModel(
    endpoint=os.getenv("AZURE_INFERENCE_ENDPOINT"),
    credential=os.getenv("AZURE_INFERENCE_CREDENTIAL"),
    model_name="gpt-4o-mini"
)
