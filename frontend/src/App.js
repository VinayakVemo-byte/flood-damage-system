import { useState } from "react";
import axios from "axios";
import "./App.css";

import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

function App() {

  const [before,setBefore] = useState(null);
  const [after,setAfter] = useState(null);

  const [beforeURL,setBeforeURL] = useState(null);
  const [afterURL,setAfterURL] = useState(null);

  const [result,setResult] = useState(null);
  const [buildingStats,setBuildingStats] = useState(null);
  const [loading,setLoading] = useState(false);

  const analyze = async () => {

    if(!before || !after){
      alert("Upload both images");
      return;
    }

    setLoading(true);

    const fd = new FormData();
    fd.append("before",before);
    fd.append("after",after);

    try{
      const r = await axios.post("http://localhost:3001/analyze",fd);
      setResult(r.data);
      setBuildingStats(r.data.building_counts);
    }
    catch(err){
      alert("Backend error");
    }

    setLoading(false);
  };

  const pieData = buildingStats ? {
    labels: Object.keys(buildingStats),
    datasets: [
      {
        data: Object.values(buildingStats),
        backgroundColor: [
          "#22c55e",  // no damage
          "#eab308",  // minor
          "#f97316",  // major
          "#ef4444"   // destroyed
        ],
        borderWidth: 0,
        hoverOffset: 10
      }
    ]
  } : null;

  const pieOptions = {
    responsive:true,
    cutout:"60%",
    plugins:{
      legend:{
        position:"bottom",
        labels:{
          color:"#e5e7eb",
          padding:12
        }
      }
    }
  };

  return (
    <div className="app">

      <h1>Flood Damage Assessment</h1>

      <div className="card upload-box">

        <div className="upload pre">
          <span className="label">Before (Pre-Disaster)</span>
          <input type="file" onChange={e=>{
            setBefore(e.target.files[0]);
            setBeforeURL(URL.createObjectURL(e.target.files[0]));
          }}/>
        </div>

        <div className="upload post">
          <span className="label">After (Post-Disaster)</span>
          <input type="file" onChange={e=>{
            setAfter(e.target.files[0]);
            setAfterURL(URL.createObjectURL(e.target.files[0]));
          }}/>
        </div>

        <button onClick={analyze}>
          {loading ? "Analyzing..." : "Analyze"}
        </button>

      </div>

      {result && (
        <>

        <div className="card stats-grid">

          <div className="stat">
            <h3>Actual Flood %</h3>
            <p>{result.actual_flood}</p>
          </div>

          <div className="stat">
            <h3>Predicted Flood %</h3>
            <p className="highlight">{result.predicted_flood}</p>
          </div>

          <div className="stat">
            <h3>Flood Pixels</h3>
            <p>{result.flood_pixels}</p>
          </div>

        </div>

        <div className="card">

          <h3>Building Damage Distribution</h3>

          {buildingStats && Object.values(buildingStats).some(v=>v>0) ? (

            <div className="chart">
              <Pie data={pieData} options={pieOptions}/>
            </div>

          ) : (

            <div className="info-card">
              <h4>No Building Labels Found</h4>
              <p>
                Building-level damage is shown only for xBD dataset images.
                For custom uploads, only flood prediction and mask are available.
              </p>
            </div>

          )}

        </div>


        <div className="card images">

  <img src={beforeURL} alt="before"/>

  <img src={afterURL} alt="after"/>

  <img src={result.mask_url+"?"+Date.now()} alt="mask"/>

  <img src={result.overlay_url+"?"+Date.now()} alt="overlay"/>

</div>


        </>
      )}

    </div>
  );
}

export default App;
