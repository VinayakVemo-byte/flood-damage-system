import {useState} from "react";
import axios from "axios";

function App(){

const [sar,setSar]=useState();
const [before,setBefore]=useState();
const [after,setAfter]=useState();

const analyze=async()=>{

 const fd=new FormData();
 fd.append("sar",sar);
 fd.append("before",before);
 fd.append("after",after);

 const res=await axios.post("http://localhost:3001/analyze",fd);
 alert(JSON.stringify(res.data));
}

return(
<div>
<h1>Flood Damage System</h1>

<input type="file" onChange={e=>setSar(e.target.files[0])}/><br/>
<input type="file" onChange={e=>setBefore(e.target.files[0])}/><br/>
<input type="file" onChange={e=>setAfter(e.target.files[0])}/><br/>

<button onClick={analyze}>Analyze</button>

</div>
)
}

export default App;
