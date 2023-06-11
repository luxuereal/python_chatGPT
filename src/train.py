from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, LLMPredictor, PromptHelper, StorageContext, load_index_from_storage, ServiceContext
from langchain.chat_models import ChatOpenAI
from PIL import ImageFile

import gradio as gr
import sys
import os

os.environ["OPENAI_API_KEY"] = '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'

ImageFile.LOAD_TRUNCATED_IMAGES = True
max_input_size = 4096
num_outputs = 512
max_chunk_overlap = 20
chunk_size_limit = 600

prompt_helper = PromptHelper(
    max_input_size=max_input_size, num_output=num_outputs, max_chunk_overlap=max_chunk_overlap, chunk_size_limit=chunk_size_limit)
llm_predictor = LLMPredictor(llm=ChatOpenAI(
    temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))
service_context = ServiceContext.from_defaults(
    llm_predictor=llm_predictor, prompt_helper=prompt_helper)


def construct_index(directory_path):
    print("========== Training ==========")
    documents = SimpleDirectoryReader(directory_path).load_data()
    index = GPTVectorStoreIndex.from_documents(
        documents, service_context=service_context
    )
    index.storage_context.persist("src/storage")
    print("========== End ==========")
    return index

construct_index("docs")