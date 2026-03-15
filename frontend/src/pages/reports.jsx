import { useState } from "react"
import "../style.css"

function Reports(){

const [projectId,setProjectId] = useState("")
const [reports,setReports] = useState([])

const fetchReports = async ()=>{

const res = await fetch(`http://127.0.0.1:8000/reports/${projectId}`)

const data = await res.json()

setReports(data)

}

return(

<div className="container">

<h1>Report History</h1>

<div className="form-card">

<label>Enter Project ID</label>

<input
type="number"
value={projectId}
onChange={(e)=>setProjectId(e.target.value)}
/>

<button onClick={fetchReports}>
Load Reports
</button>

</div>

<table>

<thead>

<tr>
<th>Report ID</th>
<th>Project</th>
<th>File Path</th>
<th>Created</th>
</tr>

</thead>

<tbody>

{reports.map(r=>(

<tr key={r.report_id}>

<td>{r.report_id}</td>

<td>{r.project_id}</td>

<td>{r.report_path}</td>

<td>{r.created_at}</td>

</tr>

))}

</tbody>

</table>

</div>

)

}

export default Reports