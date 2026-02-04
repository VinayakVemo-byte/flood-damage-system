const express = require("express");
const axios = require("axios");
const multer = require("multer");
const cors = require("cors");
const fs = require("fs");
const FormData = require("form-data");

const app = express();
app.use(cors());

const upload = multer({ dest: "uploads/" });

app.post("/analyze", upload.fields([
  { name: "sar" },
  { name: "before" },
  { name: "after" }
]), async (req, res) => {

  const form = new FormData();
  form.append("sar", fs.createReadStream(req.files.sar[0].path));
  form.append("before", fs.createReadStream(req.files.before[0].path));
  form.append("after", fs.createReadStream(req.files.after[0].path));

  const result = await axios.post("http://localhost:5000/analyze", form, {
    headers: form.getHeaders()
  });

  res.json(result.data);
});

app.listen(3001, () => console.log("Node running on 3001"));
