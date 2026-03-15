import { useState } from "react"
import "../style.css"

function Tasks(){

const [projectId,setProjectId] = useState("")
const [tasks,setTasks] = useState([])

const fetchTasks = async ()=>{

const res = await fetch(`http://127.0.0.1:8000/tasks/${projectId}`)

const data = await res.json()

setTasks(data)

}

return(

<div className="container">

<h1>Project Tasks</h1>

<div className="form-card">

<label>Enter Project ID</label>

<input
type="number"
value={projectId}
onChange={(e)=>setProjectId(e.target.value)}
/>

<button onClick={fetchTasks}>
Load Tasks
</button>

</div>

<table>

<thead>

<tr>
<th>Task ID</th>
<th>Project</th>
<th>Compliance Task</th>
<th>Deadline</th>
<th>Status</th>
</tr>

</thead>

<tbody>

{tasks.map(t=>(

<tr key={t.task_id}>

<td>{t.task_id}</td>

<td>{t.project_id}</td>

<td>{t.compliance_type}</td>

<td>{t.deadline}</td>

<td>{t.status}</td>

</tr>

))}

</tbody>

</table>

</div>

)

}

export default Tasks