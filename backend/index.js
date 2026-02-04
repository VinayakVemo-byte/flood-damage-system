const express = require("express");
const axios = require("axios");
const app = express();

app.use(require("cors")());

app.post("/analyze", async(req,res)=>{
 const result = await axios.post("http://localhost:5000/analyze");
 res.json(result.data);
});

app.listen(3001,()=>console.log("Node running on port 3001"));
