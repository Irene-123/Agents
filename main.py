import os
from dotenv import load_dotenv

from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = AzureAIChatCompletionsModel(
    endpoint=os.getenv("AZURE_INFERENCE_ENDPOINT"),
    credential=os.getenv("AZURE_INFERENCE_CREDENTIAL"),
    model_name="gpt-4o-mini"
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Translate the following into {language}:"),
    ("user", "{input_text}")
])

output_parser = StrOutputParser()
model_chain = prompt_template | model | output_parser

print(model_chain.invoke({"language": "French", "input_text": "Hello, how are you?"}))
