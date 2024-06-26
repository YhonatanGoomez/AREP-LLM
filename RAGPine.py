from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, PodSpec
import os
#from langchain_openai import OpenAIEmbeddings

os.environ["OPENAI_API_KEY"] = "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"
os.environ["PINECONE_API_KEY"] = "2eee1831-8898-454a-82fa-a544c6d72366"
os.environ["PINECONE_ENV"] = "gcp-starter"

def loadText():
    loader = TextLoader("Conocimiento.txt")
    documents = loader.load()
    #text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap  = 200,
        length_function = len,
        is_separator_regex = False,
    )


    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    import pinecone


    index_name = "langchain-demo"
    pc = Pinecone(api_key='2eee1831-8898-454a-82fa-a544c6d72366')

    print(pc.list_indexes())

    # First, check if our index already exists. If it doesn't, we create it
    if len(pc.list_indexes())==0:
        # we create a new index
        #pc.create_index(name=index_name, metric="cosine", dimension=1536)
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=PodSpec(
                environment=os.getenv("PINECONE_ENV"),
                pod_type="p1.x1",
                pods=1
            )
        )

    # The OpenAI embedding model `text-embedding-ada-002 uses 1536 dimensions`
    docsearch = PineconeVectorStore.from_documents(docs, embeddings, index_name=index_name)

def search():
    embeddings = OpenAIEmbeddings()
    index_name = "langchain-demo"
    docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)
    query = "What is a distributed pointcut"
    docs = docsearch.similarity_search(query)

    if docs:
        print(docs[0].page_content)
    else:
        print("No documents found matching the query.")

loadText()
search()