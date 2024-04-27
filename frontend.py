import streamlit as st
import requests

# Define the URL for your Flask backend
FLASK_URL = ' http://127.0.0.1:5000'

def generate_notes(file, youtube_url):
    if file:
        files = {'file': file}
    elif youtube_url:
        files = {'youtube_url': youtube_url}
    else:
        return 'No input provided.'

    response = requests.post(f'{FLASK_URL}/generate_notes', files=files)
    if response.status_code == 200:
        return response.json().get('notes', '')
    else:
        return 'Error generating notes.'

def generate_quiz(file, youtube_url):
    if file:
        files = {'file': file}
    elif youtube_url:
        files = {'youtube_url': youtube_url}
    else:
        return 'No input provided.'

    response = requests.post(f'{FLASK_URL}/generate_quiz', files=files)
    if response.status_code == 200:
        quiz_data = response.json().get('quiz')
        if quiz_data:
            return quiz_data
        else:
            return 'No quiz data generated.'
    else:
        return 'Error generating quiz.'

def main():
    st.title('GenAI Application')

    st.header('Generate Notes')
    uploaded_file_notes = st.file_uploader('Upload MP4 File for Notes', key='notes')
    youtube_url_notes = st.text_input('YouTube URL for Notes')
    if st.button('Generate Notes'):
        st.write('Generating notes...')
        notes = generate_notes(uploaded_file_notes, youtube_url_notes)
        st.write('**Notes:**')
        st.write(notes)

    st.header('Generate Quiz')
    uploaded_file_quiz = st.file_uploader('Upload MP4 File for Quiz', key='quiz')
    youtube_url_quiz = st.text_input('YouTube URL for Quiz')
    if st.button('Generate Quiz'):
        st.write('Generating quiz...')
        quiz_data = generate_quiz(uploaded_file_quiz, youtube_url_quiz)
        if isinstance(quiz_data, str):
            st.write(quiz_data)
        else:
            st.write('**Quiz Title:**', quiz_data['Quiz Title'])
            st.write('**Questions:**')
            for i, question in enumerate(quiz_data['Questions'], start=1):
                st.write(f'{i}. {question["question"]}')
                for option in question['options']:
                    st.write(option)

if __name__ == '__main__':
    main()

