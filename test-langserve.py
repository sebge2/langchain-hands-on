# https://python.langchain.com/docs/get_started/installation/
# https://medium.com/@abonia/ollama-and-langchain-run-llms-locally-900931914a46

from fastapi import FastAPI
from langchain.llms import Ollama
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langserve import add_routes
import uvicorn

llama2 = Ollama(model="llama2:latest")
template = PromptTemplate.from_template("Tell me a joke about {topic}.")
chain = template | llama2 | CommaSeparatedListOutputParser()

app = FastAPI(title="LangChain", version="1.0", description="The first server ever!")
add_routes(app, chain, path="/chain")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)