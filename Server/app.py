from flask import Flask, request, render_template, jsonify, make_response
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
from langchain_community.llms import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
# from utils import parse_file, RESPONSE_JSON, get_table_data
from langchain_community.document_loaders import YoutubeLoader
import json
from langchain.chains.combine_documents import create_stuff_documents_chain
load_dotenv()




app = Flask(__name__)
llm = ChatGoogleGenerativeAI(model="gemini-pro")
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate_notes', methods=['POST'])
def generate_notes():


    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            loader = AssemblyAIAudioTranscriptLoader(file_path=filename, api_key=os.getenv("ASSEMBLYAI_API_KEY"))
            docs = loader.load()
            prompt_template = """"Create detailed notes summarizing the {text} content of the video presentation, emphasizing the varied headings and subheadings conveyed through distinct sizes and text effects. Ensure that the notes provide a comprehensive understanding of the topic discussed, allowing readers to grasp key points effortlessly."""

            prompt = PromptTemplate.from_template(prompt_template)
            llm_chain = LLMChain(llm=llm, prompt=prompt)

            stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

            # print(stuff_chain.run(docs))
            notes = stuff_chain.run(docs)
            return jsonify({'notes': notes})

    elif 'youtube_url' in request.form:
            youtube_url = request.form['youtube_url']
            filename = youtube_url
            print(filename)
            loader = YoutubeLoader.from_youtube_url(filename, add_video_info=True)
            docs = loader.load()
            prompt_template = """Produce comprehensive paragraph-based notes derived from the {text}, emphasizing detailed explanations 
            over bullet points. Each subsection should feature elaborative paragraphs elucidating the content 
            under the respective subheadings. Maintain a long-format approach throughout, providing in-depth insights 
            and analysis. The goal is to deliver thorough comprehension of the lecture's topics, facilitating ease of 
            understanding for readers. """

            prompt = PromptTemplate.from_template(prompt_template)
            llm_chain = LLMChain(llm=llm, prompt=prompt)

            stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text", )
            notes = stuff_chain.run(docs)
            return jsonify({'notes': notes})

@app.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    # Here you would write code to generate a quiz based on the notes or video content
    # Placeholder code for demonstration
    youtube_url = request.form['youtube_url']
    filename = youtube_url
    print(filename)

    loader = YoutubeLoader.from_youtube_url(
        "https://www.youtube.com/watch?v=Nq7ok-OyEpg&list=PLgUwDviBIf0rAuz8tVcM0AymmhTRsfaLU", add_video_info=True
    )

    text = loader.load()

    model = ChatGoogleGenerativeAI(model="gemini-pro")

    prompt = ChatPromptTemplate.from_template(
        """
        Text:{text}
        You are an expert MCQ maker, Given the above text, it is your job to \n
    create a quiz of 10 multiple choice questions.
    Make sure that the questions are not repeated and check all the questions to be conforming the text as well.
    """
    )

    output_parser = StrOutputParser()

    chain = (
            {"text": RunnablePassthrough(),
             # "response_json": RunnablePassthrough(),
             "number": RunnablePassthrough()}
            | prompt
            | model
            | output_parser
    )

    # chain.invoke({"context": docs})

    # print(chain.invoke({"text": text, "response_json": json.dumps(RESPONSE_JSON)}))
    quiz= chain.invoke({"text": text})
    print(quiz)
    # quiz = {"question": "What was discussed in the video?", "options": ["Option 1", "Option 2", "Option 3", "Option 4"]}
    return jsonify({'quiz': quiz})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
