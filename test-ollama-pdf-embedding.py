# https://ollama.com/blog/embedding-models
# https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf/

import ollama
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


# Load pdf content
loader = PyPDFLoader("~/Downloads/1_CKA_CKAD_Basics_of_kubernetes.pdf")
pages = loader.load_and_split()
pdfContent = ""
for i in range(len(pages)):
    pdfContent += pages[i].page_content

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 100, chunk_overlap = 0)
texts = text_splitter.create_documents([pdfContent])


client = chromadb.Client()

client.delete_collection(name="docs")

collection = client.get_or_create_collection(name="docs")

# store each document in a vector embedding database
for i, d in enumerate(texts):
    response = ollama.embeddings(model="mxbai-embed-large", prompt=d.page_content)
    embedding = response["embedding"]
    collection.add(
        ids=[str(i)],
        embeddings=[embedding],
        documents=[d.page_content]
    )


# an example prompt
prompt = "What is Kubernetes?"

# generate an embedding for the prompt and retrieve the most relevant doc
response = ollama.embeddings(
    prompt=prompt,
    model="mxbai-embed-large"
)
results = collection.query(
    query_embeddings=[response["embedding"]],
    n_results=1
)
data = results['documents'][0][0]

# generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
    model="llama2",
    prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
)

print(output['response'])