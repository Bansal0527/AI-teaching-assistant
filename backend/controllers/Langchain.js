const { ChatGoogleGenerativeAI } = require("@langchain/google-genai");
const { YoutubeLoader } = require("@langchain/community/document_loaders/web/youtube");
const { StringOutputParser } = require("@langchain/core/output_parsers");
const { ChatPromptTemplate } = require("@langchain/core/prompts");
const {PDFLoader} = require("@langchain/community/document_loaders/fs/pdf");
const fs = require("fs/promises"); // Import the file system module
const path = require("path");

const model = new ChatGoogleGenerativeAI({
    model: "gemini-2.0-flash",
    temperature: 0,
    apiKey: process.env.GOOGLE_GENAI_API_KEY,
  });



 const generateNotes = async (req, res) => {
    let tempFilePath;
    let docs;
    if (req.file) {
        const docsDir = path.join(__dirname, '..', 'docs');
        await fs.mkdir(docsDir, { recursive: true });
        const uniqueFileName = `${Date.now()}-${req.file.originalname}`;
        tempFilePath = path.join(docsDir, uniqueFileName);
        await fs.writeFile(tempFilePath, req.file.buffer);
        const loader = new PDFLoader(tempFilePath);
        docs = await loader.load();
    }

    else if (req.body) {
        const {url} = req.body;
        console.log(url)
        const loader = YoutubeLoader.createFromUrl(url, {
            language: "en",
            addVideoInfo: true,
          });


        docs = await loader.load();
    }

    const prompt = ChatPromptTemplate.fromTemplate(
        `
Create detailed notes summarizing the {text} content of the video presentation, emphasizing the varied headings and subheadings conveyed through distinct sizes and text effects. Ensure that the notes provide a comprehensive understanding of the topic discussed, allowing readers to grasp key points effortlessly.
    `
      );
      const chain = prompt.pipe(model).pipe(new StringOutputParser());

    const response = await chain.invoke({ text: docs });
    return res.status(200).json({
        success: true,
        data: response
    })

}

module.exports = generateNotes;