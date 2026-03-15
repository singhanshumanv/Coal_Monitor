import {Link} from "react-router-dom"
import { useEffect, useState } from "react"

function Navbar(){

const [alertCount,setAlertCount] = useState(0)

useEffect(()=>{

fetch("http://127.0.0.1:8000/alerts")
.then(res=>res.json())
.then(data=>setAlertCount(data.length))

},[])

return(

<nav style={{
display:"flex",
justifyContent:"space-between",
alignItems:"center",
padding:"15px 30px",
background:"#020617",
borderBottom:"1px solid rgba(255,255,255,0.1)"
}}>

<h2 style={{color:"#6366f1"}}>AI Compliance</h2>

<div style={{display:"flex",gap:"25px"}}>

<Link to="/" style={{color:"white",textDecoration:"none"}}>
Dashboard
</Link>

<Link to="/create-project" style={{color:"white",textDecoration:"none"}}>
Create Project
</Link>

<Link to="/upload" style={{color:"white",textDecoration:"none"}}>
Upload Regulation
</Link>


<Link to="/tasks" style={{color:"white",textDecoration:"none"}}>
Tasks
</Link>


<Link to="/reports" style={{color:"white",textDecoration:"none"}}>
Reports
</Link>
</div>


<div className="alert-bell">
🔔
<span className="alert-count">{alertCount}</span>
</div>

</nav>

)

}

export default Navbar