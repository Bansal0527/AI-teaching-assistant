### GenAI Application

This web application provides functionality to generate notes and quizzes based on video presentations or audio transcripts. Users can either upload a file or provide a YouTube URL to initiate the generation process.

#### Generate Notes
- Upload a file containing the content you want summarized.
- Alternatively, enter the URL of a YouTube video for automatic transcription.
- Click the "Generate Notes" button to initiate the process.

#### Generate Quiz
- Upload a file or input a YouTube URL containing the content for which you want to create a quiz.
- Click the "Generate Quiz" button to generate quiz questions based on the provided content.

### Setup Instructions
1. Clone the repository from [GitHub](https://github.com/Bansal0527/AI-teaching-assistant).
2. Ensure you have Python installed on your system.
3. Navigate to the "server" folder within the cloned repository.
4. Install the required Python dependencies using the following command:
    ```
    pip install -r requirements.txt
    ```
5. Set up environment variables:
    - `ASSEMBLYAI_API_KEY`: AssemblyAI API key.
    - `GOOGLE_API_KEY` : Google API Key.
6. Run the Flask application using the following command:
    ```
    python app.py
    ```
7. Access the application in your web browser at `http://localhost:8080`.

### Hosting on Render
This application is also hosted on Render for easy accessibility. You can access it using the following link: [GenAI Application on Render](https://ai-teaching-assistant-2.onrender.com/)

### Usage
1. **Generating Notes:**
    - Choose a file or provide a YouTube URL.
    - Click "Generate Notes" to generate summarized notes.
2. **Generating Quiz:**
    - Upload a file or enter a YouTube URL.
    - Click "Generate Quiz" to create quiz questions.

### API Endpoints
- **POST `/generate_notes`**
    - Accepts file uploads or YouTube URLs to generate detailed notes.
    - Returns JSON response containing generated notes.

- **POST `/generate_quiz`**
    - Accepts file uploads or YouTube URLs to generate a quiz.
    - Returns JSON response containing generated quiz questions.

### Additional Notes
- Ensure proper handling of sensitive data, especially API keys.
- Monitor resource usage, especially when dealing with large files or high traffic.
