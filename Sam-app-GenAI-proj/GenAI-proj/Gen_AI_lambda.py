from langchain.memory import ConversationSummaryBufferMemory
from langchain.llms import OpenAI
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
import pinecone
import PyPDF2
import io
from langchain.document_loaders import PyPDFLoader
import os


os.environ["OPENAI_API_KEY"] = "OPEN_AI_KEY"
os.environ["PINECONE_API_KEY"] = "PINE_CONE_KEY"
os.environ["PINECONE_ENV"] = "gcp-starter"

def lambda_handler(event,context):
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
                memory = ConversationSummaryBufferMemory(
                    llm=llm,
                    max_token_limit=100,
                    memory_key="chat_history",
                    return_messages=True,
                    output_key="answer",
                )
                return memory

            except Exception as e:
                return e

        def initialize_pinecone(self, model_name):
            try:
                embed = OpenAIEmbeddings(
                    model=model_name, openai_api_key=os.environ["OPENAI_API_KEY"]
                )

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
            pdf_file = io.BytesIO(pdf_bytes)
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

        def split_text(self, chunk_size, chunk_overlap):
            try:
                self.initialize_pinecone("text-embedding-ada-002")
                text_splitter = CharacterTextSplitter(
                    chunk_size=chunk_size, chunk_overlap=chunk_overlap
                )
                documents = self.uploaded_file_loader()
                # print(
                #     ":snake: File: Chat_bot_stream_lit/chat_bot.py | Line: 96 | split_text ~ documents",
                #     type(documents),
                # )
                documents = text_splitter.create_documents(documents)
                # print(
                #     ":snake: File: Chat_bot_stream_lit/chat_bot.py | Line: 97 | split_text ~ documents",
                #     (documents),
                # )

                self.vector_db = Pinecone.from_documents(
                    documents,
                    embedding=OpenAIEmbeddings(),
                    index_name="langchain-retrieval-augmentation",
                )
                print("---------------------------Returning Successfully-----------------")
                return self.vector_db

            except Exception as e:
                return e

        def create_chain(self, memory_file=None, model="gpt-3.5-turbo"):
            try:
                print("THis create_chain is running again ")
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
                    retriever=vector_db.as_retriever(search_kwargs={"k": 7}),
                    return_source_documents=True,
                    memory=memory,
                    verbose=False,
                )
                # print("Qa chain is", (qa_chain.memory.chat_memory))
                return qa_chain
            except Exception as e:
                return e