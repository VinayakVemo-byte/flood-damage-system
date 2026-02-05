const express = require("express");
const axios = require("axios");
const multer = require("multer");
const cors = require("cors");
const fs = require("fs");
const FormData = require("form-data");

const app = express();
app.use(cors());

const upload = multer({ dest: "uploads/" });

app.post("/analyze",upload.fields([{name:"before"},{name:"after"}]),async(req,res)=>{

 const before=req.files.before[0];
 const after=req.files.after[0];

 const fd=new FormData();

 fd.append("before",fs.createReadStream(before.path));
 fd.append("after",fs.createReadStream(after.path));

 // IMPORTANT: send original filename
 fd.append("after_name",after.originalname);

 const r=await axios.post("http://localhost:5000/analyze",fd,{
   headers:fd.getHeaders()
 });

 res.json(r.data);
});


app.listen(3001, () => console.log("Node running on 3001"));
