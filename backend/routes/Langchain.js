const express = require("express")
const router = express.Router()
const multer = require('multer');
const generateNotes  = require("../controllers/Langchain")
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

router.post('/generate-notes',upload.single('file'), generateNotes);

module.exports = router