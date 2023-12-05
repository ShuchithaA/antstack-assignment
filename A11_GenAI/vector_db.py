import os
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import openai

# Initialize Pinecone
pinecone.init(api_key="65c8299a-a78a-4b8d-8cbe-8742996736fd", environment="gcp-starter")

# Create a Pinecone index
index_name = "langchain-retrieval-augmentation"
if index_name not in pinecone.list_indexes():
   pinecone.create_index(name=index_name, metric='cosine', dimension=1536)

# Initialize OpenAI
openai.api_key = "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"


# Initialize Langchain and OpenAI embeddings
index = pinecone.Index(index_name)
embeddings = OpenAIEmbeddings(openai_api_key="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")
vectorstore = Pinecone(index, embeddings, "text")

# User input
user_input = "what is AI"

# Embed user input and add it to the Pinecone index
vectorstore.add_texts(user_input)

# Generate output from GPT-3.5
response = openai.Completion.create(
   engine="text-davinci-002",
   prompt=user_input,
   max_tokens=60
)

# Print the generated response
print(response.choices[0].text.strip())
