from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

import socket

def recv_all(sock, bufsize=4096):
    """
    Receive data from the socket until no more data is available.
    """
    data = b""
    while True:
        chunk = sock.recv(bufsize)
        if not chunk:
            break
        data += chunk
    return data

llm = Ollama(model="llama2")

# test = llm.invoke("What is a Module in Talon?")
# print(test)

from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://talon.wiki/unofficial_talon_docs/")

embeddings = OllamaEmbeddings()
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)
vector = FAISS.from_documents(documents, embeddings)

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('0.0.0.0', 12345)
print('Starting up on {} port {}'.format(*server_address))
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

while True:
    print('Waiting for a connection...')
    connection, client_address = server_socket.accept()
    
    try:
        print('Connection from', client_address)

        received_data = recv_all(connection)
        print('Received {!r}'.format(received_data))
        
        phrase = received_data.decode('utf-8')
        
        response = retrieval_chain.invoke({"input": phrase})
        print(response["answer"])

        # if received_data == b'minimize window':
        #     pyautogui.hotkey('win', 'down')
                
    finally:
        # Clean up the connection
        connection.close()










