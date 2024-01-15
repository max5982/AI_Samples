import fire
import os
import sys
import time

import torch
from transformers import LlamaTokenizer

from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import OnlinePDFLoader

from langchain.vectorstores import Chroma
# embeddings are numerical representations of the question and answer text
from langchain.embeddings import HuggingFaceEmbeddings
# use a common text splitter to split text into chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain

from transformers import LlamaForCausalLM, LlamaTokenizer
from transformers import pipeline
from langchain.llms.huggingface_pipeline import HuggingFacePipeline


"""
    Args:
        ckpt_dir (str): The directory containing checkpoint files for the pretrained model.
        tokenizer_path (str): The path to the tokenizer model used for text encoding/decoding.
        temperature (float, optional): The temperature value for controlling randomness in generation.
            Defaults to 0.6.
        top_p (float, optional): The top-p sampling parameter for controlling diversity in generation.
            Defaults to 0.9.
        max_seq_len (int, optional): The maximum sequence length for input prompts. Defaults to 512.
        max_batch_size (int, optional): The maximum batch size for generating sequences. Defaults to 8.
        max_gen_len (int, optional): The maximum length of generated sequences. If None, it will be
            set to the model's max sequence length. Defaults to None.
"""


# Step 1: load the external data source
loader = PyPDFLoader("aura.pdf")
documents = loader.load()


# Step 2: Get text splits from document
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
all_splits = text_splitter.split_documents(documents)


# Step 3: Use the embedding model
model_name = "sentence-transformers/all-mpnet-base-v2" # embedding model
model_kwargs = {"device": "cuda"}
embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)


# Step 4: Use vector store to store embeddings
vectorstore = FAISS.from_documents(all_splits, embeddings)

model_name = "llama-2-7b-chat-hf"
model_id = '../' + model_name
tokenizer = LlamaTokenizer.from_pretrained(model_id)
model = LlamaForCausalLM.from_pretrained(model_id, load_in_4bit=True, device_map='auto', torch_dtype='auto', cache_dir=model_id)


hf_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, \
                       do_sample=True, temperature=0.9, top_p=0.8, max_new_tokens=200)
hf_llm = HuggingFacePipeline(pipeline=hf_pipeline)


# Query against your own data
chain = ConversationalRetrievalChain.from_llm(hf_llm, vectorstore.as_retriever(), return_source_documents=True)

print("==============================================")
print(f"Model: {model_name}")
print("==============================================")
print("")
chat_history = []


while True:
    user_input = input("Query: ")

    if user_input == "exit":
        break

    query = user_input
    print("==============================================")
    print(f"[query]: {query}")
    start = time.perf_counter()
    result = chain({"question": query, "chat_history": chat_history})
    print(f"[answer]: {result['answer']}")
    e2e_inference_time = (time.perf_counter()-start)*1000
    print(f"[time] it takes {e2e_inference_time} ms")
    print("==============================================")

