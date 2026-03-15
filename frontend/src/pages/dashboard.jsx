import { useEffect, useState } from "react"
import AlertsPanel from "../components/alertspanel"
import "../style.css"
import { Pie } from "react-chartjs-2"
import {
Chart as ChartJS,
ArcElement,
Tooltip,
Legend
} from "chart.js"

ChartJS.register(ArcElement, Tooltip, Legend)

function Dashboard(){

const [projects,setProjects] = useState([])
const [bottlenecks,setBottlenecks] = useState({})
const lowRisk = projects.filter(p => p.risk_level === "LOW").length
const mediumRisk = projects.filter(p => p.risk_level === "MEDIUM").length
const highRisk = projects.filter(p => p.risk_level === "HIGH").length


const chartData = {
labels:["Low Risk","Medium Risk","High Risk"],
datasets:[
{
data:[lowRisk, mediumRisk, highRisk],
backgroundColor:[
"#22c55e",
"#f59e0b",
"#ef4444"
]
}
]
}

useEffect(()=>{

fetch("http://127.0.0.1:8000/dashboard")
.then(res=>res.json())
.then(data=>{

setProjects(data)

data.forEach(p=>{

fetch(`http://127.0.0.1:8000/bottleneck_analysis/${p.project_id}`)
.then(res=>res.json())
.then(b=>{

setBottlenecks(prev=>({
...prev,
[p.project_id]:b
}))

})

})

})

fetch("http://127.0.0.1:8000/alerts")
.then(res=>res.json())
.then(data=>setAlerts(data))

},[])

const totalProjects = projects.length
const totalTasks = projects.reduce((a,b)=>a+b.total_tasks,0)
const totalOverdue = projects.reduce((a,b)=>a+b.overdue_tasks,0)

const riskColor=(risk)=>{
if(risk==="HIGH") return "#ef4444"
if(risk==="MEDIUM") return "#f59e0b"
return "#22c55e"
}



const generateReport = async (projectId)=>{

const response = await fetch(
`http://127.0.0.1:8000/generate_report/${projectId}`
)

const blob = await response.blob()

const url = window.URL.createObjectURL(blob)

const a = document.createElement("a")

a.href = url

a.download = "compliance_report.pdf"

document.body.appendChild(a)

a.click()

a.remove()

}

return(

<div className="container">

<h1>AI Compliance Dashboard</h1>

{/* KPI Cards */}

<div className="kpi-grid">

<div className="kpi-card">
<h3>Total Projects</h3>
<p>{totalProjects}</p>
</div>

<div className="kpi-card">
<h3>Total Tasks</h3>
<p>{totalTasks}</p>
</div>

<div className="kpi-card">
<h3>Overdue Tasks</h3>
<p>{totalOverdue}</p>
</div>

</div>

<AlertsPanel />

{/* Project Table */}

<div className="card">

<h2>Risk Distribution</h2>

<div style={{width:"300px"}}>
<Pie data={chartData}/>
</div>

</div>

<div className="card">

<table>

<thead>

<tr>
<th>Project</th>
<th>Location</th>
<th>Total Tasks</th>
<th>Overdue</th>
<th>Due Soon</th>
<th>Risk</th>
<th>Bottleneck</th>
<th>Report</th>
</tr>

</thead>

<tbody>

{projects.map(p=>(
<tr key={p.project_id}>

<td>{p.project_name}</td>
<td>{p.location}</td>
<td>{p.total_tasks}</td>
<td>

{p.overdue_tasks}

<div className="risk-bar">

<div
className="risk-fill"
style={{
width: p.total_tasks
? `${(p.overdue_tasks / p.total_tasks) * 100}%`
: "0%"
}}
></div>

</div>

</td>
<td>{p.due_soon_tasks}</td>

<td>

<span className={`risk ${p.risk_level.toLowerCase()}`}>
{p.risk_level}
</span>

</td>



<td>

{bottlenecks[p.project_id] && (
<span className={`bottleneck ${
bottlenecks[p.project_id].bottleneck_level.toLowerCase().includes("critical")
? "critical"
: bottlenecks[p.project_id].bottleneck_level.toLowerCase()
}`}>
{bottlenecks[p.project_id].bottleneck_level}
</span>
)}

</td>

<td>
    
<button onClick={()=>generateReport(p.project_id)}>
Generate Report
</button>

</td>

</tr>

))}

</tbody>

</table>

</div>

</div>

)

}

export default Dashboard