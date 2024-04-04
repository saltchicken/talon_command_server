import json
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

from typing import Iterable
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessageChunk
from langchain_core.runnables import RunnableGenerator

from dataclasses import dataclass

import socket

class SocketMessage:
    type = 0
    message = 0

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

class ScreenWriterClient():
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def __enter__(self):
        # TODO: Add try | except
        self.client_socket.connect(('192.168.1.13', 12346))
        return self
    
    def __exit__(self, *args, **kwargs):
        self.client_socket.close()
        
    def write(self, message):
        self.client_socket.send(message.encode())
        
        
if __name__ == "__main__":
    llm = Ollama(model="llama2")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Your responses are terse."),
        ("user", "{input}")
    ])

    def streaming_parse(chunks: Iterable[BaseMessageChunk]) -> Iterable[str]:
        for chunk in chunks:
            yield chunk

    streaming_parse = RunnableGenerator(streaming_parse)


    chain = prompt | llm | streaming_parse

    # test = llm.invoke("What is a Module in Talon?")
    # print(test)

    # from langchain_community.document_loaders import WebBaseLoader
    # loader = WebBaseLoader("https://talon.wiki/unofficial_talon_docs/")

    # embeddings = OllamaEmbeddings()
    # docs = loader.load()

    # text_splitter = RecursiveCharacterTextSplitter()
    # documents = text_splitter.split_documents(docs)
    # vector = FAISS.from_documents(documents, embeddings)

    # prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    # <context>
    # {context}
    # </context>

    # Question: {input}""")

    # document_chain = create_stuff_documents_chain(llm, prompt)

    # retriever = vector.as_retriever()
    # retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    print('connecting to ScreenWriterServer')
    with ScreenWriterClient() as writer:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('0.0.0.0', 12345)
        # server_address = ('127.0.0.1', 12345)

        print('Starting up on {} port {}'.format(*server_address))
        server_socket.bind(server_address)

        # app = QApplication(sys.argv)
        # window = OverlayWindow('yes', 50)
        # window.show()
        # sys.exit(app.exec_())
        # queue = Queue()
        # p = Process(target=write_to_screen_process, args=('', 50, queue))
        # p.daemon = True
        # p.start()
        # controller = OverlayController(queue)
        # embed()

        # Listen for incoming connections
        server_socket.listen(1)

        while True:
            print('Waiting for a connection...')
            connection, client_address = server_socket.accept()
            
            try:
                print('Connection from', client_address)

                # received_data = recv_all(connection)
                received_data = connection.recv(4096).decode()
                
                if received_data:
                    # phrase = received_data.decode('utf-8')
                    received_object = json.loads(received_data)
                    print("Received Object:", received_object)
                    
                else:
                    continue
                # print('Received {!r}'.format(received_data))
                
                phrase = received_object['name']
                output = ''
                for chunk in chain.stream(phrase):
                    
                    # if '\n' in chunk:
                    #     chunk = chunk.replace('\n', '')
                    #     controller.clear()
                    output += chunk
                    try:
                        # print('wrote', output)
                        writer.write(output)
                    except Exception as e:
                        print(e)
                        # print(output)
                    # controller.append(chunk)
                    # print(chunk, end="", flush=True)
                
                # response = retrieval_chain.invoke({"input": phrase})
                # print(response["answer"])

                # if received_data == b'minimize window':
                #     pyautogui.hotkey('win', 'down')
                        
            finally:
                # Clean up the connection
                connection.close()
