import logging
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_ollama import OllamaEmbeddings
from langchain_community.llms import Ollama
# from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever

llm = Ollama(model="llama3")

# Load blog post
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")

# loader = DirectoryLoader('../', glob="**/*.md")
# docs = loader.load()
data = loader.load()

# Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
splits = text_splitter.split_documents(data)

# VectorDB
embeddings = OllamaEmbeddings(model="nomic-text-embed"
                              model_kwargs={"top_p": 0, "frequency_penalty": 0, "presence_penalty:" 0})

vectordb = Chroma.from_documents(documents=splits, embedding=embedding)

question = "\n "

retriever_from_llm = MultiQueryRetriever.from_llm(
    retriever=vectordb.as_retriever(), llm=llm
)

# Set logging for the queries
logging.basicConfig()
logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)


unique_docs = retriever_from_llm.invoke(question)

len(unique_docs)
