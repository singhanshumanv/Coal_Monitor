import {useState} from "react"
import "../style.css"

function UploadRegulation(){

const [projectId,setProjectId]=useState("")
const [file,setFile]=useState(null)

const handleUpload=async(e)=>{

e.preventDefault()

const formData=new FormData()
formData.append("file",file)

await fetch(`http://127.0.0.1:8000/upload_regulation/${projectId}`,{
method:"POST",
body:formData
})

alert("Regulation Uploaded")
}

return(

<div className="page">

<div className="form-card">

<h2>Upload Regulation</h2>

<form onSubmit={handleUpload}>

<label>Project ID</label>
<input type="number" value={projectId} onChange={e=>setProjectId(e.target.value)} required/>

<label>Select PDF</label>
<input type="file" accept=".pdf" onChange={e=>setFile(e.target.files[0])} required/>

<button type="submit">Upload Regulation</button>

</form>

</div>

</div>

)

}

export default UploadRegulation