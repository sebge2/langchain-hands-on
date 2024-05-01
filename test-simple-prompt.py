from langchain_community.llms import Ollama

llm = Ollama(model="llama2:latest")

invoke = llm.invoke("Tell me a joke")
print(invoke)