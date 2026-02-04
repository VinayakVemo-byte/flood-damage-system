import axios from "axios";

function App(){

const analyze=async()=>{
 const res=await axios.post("http://localhost:3001/analyze");
 alert(JSON.stringify(res.data));
}

return(
 <div>
  <h1>Flood Damage System</h1>
  <button onClick={analyze}>Analyze</button>
 </div>
)
}

export default App;
