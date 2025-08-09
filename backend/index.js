const express = require('express');
const langchainRoutes = require('./routes/Langchain'); 

const app = express();

const PORT = process.env.PORT || 3000;

app.use(express.json());

app.get("/", (req, res) => {
    res.send('welcome')
})

app.use('/api/v1', langchainRoutes);


app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
})