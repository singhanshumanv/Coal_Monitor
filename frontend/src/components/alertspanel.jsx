import { useEffect, useState } from "react";
import "../style.css"

function AlertsPanel() {

const [alerts,setAlerts] = useState([]);

useEffect(()=>{

fetch("http://127.0.0.1:8000/alerts")
.then(res=>res.json())
.then(data=>setAlerts(data));

},[]);

return(

<div className="alerts-panel">

<h3>Alerts</h3>

<ul className="alert-list">
{alerts.map((a,index)=>(
<li key={index} className={a.message.toLowerCase().includes("overdue") ? "alert-danger" : "alert-warning"}>
    {a.message}</li>
))}
</ul>
</div>

);
}

export default AlertsPanel;