#is used to keep a buffer of recent interactions in memory. It compiles them into a summary and uses both the summary and the original interactions. 
# The buffer is flushed when the total token length exceeds a specified limit
from langchain.memory import ConversationSummaryBufferMemory
from langchain.llms import OpenAI
from langchain.llms import OpenAI

# used to interact with OpenAI's chat models. It allows you to pass in chat messages and receive responses from the mode
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory

# vector store is a data structure used for storing high-dimensional vectors and performing operations on them, such as nearest neighbor search.
# The vectors in a vector store are typically embeddings of text, and the operations are used for tasks like semantic search or text classification
from langchain.vectorstores import Pinecone

# It uses the OpenAI language model to generate embeddings, which are high-dimensional vectors that capture the semantic meaning of the text. 
from langchain.embeddings.openai import OpenAIEmbeddings

# The CharacterTextSplitter class in LangChain is used to split text into smaller chunks. 
# It is a document transformation system that takes an array of documents and returns an array of transformed documents.
from langchain.text_splitter import CharacterTextSplitter

# The ConversationalRetrievalChain class in LangChain is a chain that allows you to have a conversation based on retrieved documents.
# It takes in chat history (a list of messages) and new questions, and then returns an answer to that question. 
from langchain.chains import ConversationalRetrievalChain

# The ChatOpenAI class in LangChain is used to interact with OpenAI's chat models. 
# It allows you to pass in chat messages and receive responses from the model
from langchain.chat_models import ChatOpenAI

import pinecone
import PyPDF2
import io
from langchain.document_loaders import PyPDFLoader
import os


os.environ["OPENAI_API_KEY"] = "OPEN_AI_KEY"
os.environ["PINECONE_API_KEY"] = "PINE_CONE_KEY"
os.environ["PINECONE_ENV"] = "gcp-starter"


class chat_bot:
    def __init__(
        self,
        max_token,
        temperature,
        chunk_size,
        chunk_overlap,
        uploaded_file,
        reference=None,
    ):
        self.max_token = max_token
        self.reference = reference
        self.temperature = temperature
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.uploaded_file = uploaded_file

    def load_doc(self):
        try:
            pdf_loader = PyPDFLoader(self.reference)
            documents = pdf_loader.load()
            return documents
        except Exception as e:
            return e

    def initialize_memory(self):
        try:
            llm = OpenAI(temperature=self.temperature) 
            # randomness 0-1 (0 deterministic , 1 variety)
            memory = ConversationSummaryBufferMemory(
                llm=llm,
                max_token_limit=100,
                memory_key="chat_history",
                return_messages=True, 
                output_key="answer",
            )
            return memory
            #  It combines the ideas of keeping a buffer of recent interactions and summarizing older interactions.
        except Exception as e:
            return e

    def initialize_pinecone(self, model_name):
        try:
            #  to generate embeddings, which are high-dimensional vectors that capture the semantic meaning of the text. 
            embed = OpenAIEmbeddings(
                model=model_name, openai_api_key=os.environ["OPENAI_API_KEY"]
            )
            # This will initialize a Pinecone client with your API key and environment.
            # You can then use this client to create, delete, and configure Pinecone indexes  
            
            # A Pinecone index is the highest-level organizational unit of vector data in Pinecone. 
            # It accepts and stores vectors, serves queries over the vectors it contains, and performs other vector operations over its contents
            pinecone.init(
                api_key=os.environ["PINECONE_API_KEY"],
                environment=os.environ["PINECONE_ENV"],
            )

        except Exception as e:
            return e

    def uploaded_file_loader(self):
        pdf_bytes = self.uploaded_file.read()
        # print(
        #     ":snake: File: Chat_bot_stream_lit/chat_bot.py | Line: 79 | uploaded_file_loader ~ pdf_bytes",
        #     pdf_bytes,
        # )
        
        # However, if you want to avoid saving the PDF file explicitly to disk, for example, when you want to store the PDF in a database or AWS S3, you can convert the file into a byte stream using io.BytesIO and then pass it to PdfReader
        pdf_file = io.BytesIO(pdf_bytes) 
        # io.BytesIO class is useful when you need to work with binary data in memory, such as when reading and writing to files, processing binary data,
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        # print(type(pdf_reader))
        
        documents = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            documents.append(page_text)
            
        # print(type(documents))
        # print(documents[0])
        return documents
        # documents is a list where each element is the text of a page in the PDF document

    def split_text(self, chunk_size, chunk_overlap):
        try:
            self.initialize_pinecone("text-embedding-ada-002") 
            # text-embedding-ada-002: embedding model for text
            
            #  an instance of the CharacterTextSplitter class. 
            text_splitter = CharacterTextSplitter(
                chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )
            # process pdf
            documents = self.uploaded_file_loader()
            # print(
            #     ":snake: File: Chat_bot_stream_lit/chat_bot.py | Line: 96 | split_text ~ documents",
            #     type(documents),
            # )
            documents = text_splitter.create_documents(documents)
            # takes a list of texts as input and returns a list of smaller chunks of text
            
            
            # print(
            #     ":snake: File: Chat_bot_stream_lit/chat_bot.py | Line: 97 | split_text ~ documents",
            #     (documents),
            # )

            self.vector_db = Pinecone.from_documents(
                documents,
                embedding=OpenAIEmbeddings(),
                index_name="langchain-retrieval-augmentation",
            )
            
            # docs is a list of documents that have been split into smaller chunks using the RecursiveCharacterTextSplitter.
            # embeddings is an instance of the OpenAIEmbeddings class, which is responsible for converting text data into embeddings using OpenAI's language model
            # index_name is a string representing the name of the Pinecone index
            print("---------------------------Returning Successfully-----------------")
            return self.vector_db

        except Exception as e:
            return e

    def create_chain(self, memory_file=None, model="gpt-3.5-turbo"):
        try:
            print("THis create_chain is running again ")
            # pinecone db is initialized, pdf is read, split ,embeddings are created
            vector_db = self.split_text(self.chunk_size, self.chunk_overlap)
            
            # print(vector_db)
            # print("Memory file is =", memory_file)
            if memory_file == None:
                memory = self.initialize_memory()
            else:
                memory = memory_file

            print(
                ":snake: File: Chat_bot_stream_lit/chat_bot.py | Line: 133 | create_chain ~ memory",
                memory.chat_memory,
            )
            qa_chain = ConversationalRetrievalChain.from_llm(
                ChatOpenAI(temperature=self.temperature, model_name=model), 
                # wrapper for ai chatbot 
                retriever=vector_db.as_retriever(search_kwargs={"k": 7}), 
                # This is the retriever that the chain will use to fetch relevant documents
                return_source_documents=True,
                memory=memory,
                verbose=False,
                #  If verbose is set to True, the chain will print out more detailed logs about its operation. 
                # This can be useful for debugging or understanding the internal workings of the chain 
            )
            # print("Qa chain is", (qa_chain.memory.chat_memory))
            return qa_chain
        except Exception as e:
            return e