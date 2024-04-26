import os
from langchain.chains.qa_generation.base import QAGenerationChain
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import AssemblyAIAudioTranscriptLoader
from langchain.chains import LLMSummarizationCheckerChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro")

audio_file = "demo.mp4"
# or a local file path: audio_file = "./nbc.mp3"

loader = AssemblyAIAudioTranscriptLoader(file_path=audio_file, api_key=os.getenv("ASSEMBLYAI_API_KEY"))

docs = loader.load()
# print(docs[0].page_content)


# print(docs[0].page_content)


# Summarizer
# chain = load_summarize_chain(llm=llm,chain_type='stuff',)
# chain = LLMSummarizationCheckerChain.from_llm(llm,)
# response = chain.run(docs)
# print("#######")
# print(response)
# print("#######")





#2nd Way
# Define prompt
prompt_template = """Write a concise summary of the following:
"{text}"
CONCISE SUMMARY:"""
prompt = PromptTemplate.from_template(prompt_template)
llm_chain = LLMChain(llm=llm, prompt=prompt)

stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")


print(stuff_chain.run(docs))




