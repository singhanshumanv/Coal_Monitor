import {useState} from "react"
import "../style.css"

function CreateProject(){

const [name,setName]=useState("")
const [location,setLocation]=useState("")
const [owner,setOwner]=useState("")
const [startDate,setStartDate]=useState("")

const handleSubmit=async(e)=>{

e.preventDefault()

await fetch("http://127.0.0.1:8000/create_project",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
name:name,
location:location,
owner:owner,
start_date:startDate
})
})

alert("Project Created")
}

return(

<div className="page">

<div className="form-card">

<h2>Create Project</h2>

<form onSubmit={handleSubmit}>

<label>Project Name</label>
<input type="text" value={name} onChange={e=>setName(e.target.value)} required/>

<label>Location</label>
<input type="text" value={location} onChange={e=>setLocation(e.target.value)} required/>

<label>Owner</label>
<input type="text" value={owner} onChange={e=>setOwner(e.target.value)} required/>

<label>Start Date</label>
<input type="date" value={startDate} onChange={e=>setStartDate(e.target.value)} required/>

<button type="submit">Create Project</button>

</form>

</div>

</div>

)

}

export default CreateProject