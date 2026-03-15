import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/navbar";
import Dashboard from "./pages/dashboard";
import CreateProject from "./pages/createproject";
import UploadRegulation from "./pages/uploadregulation";
import Tasks from "./pages/tasks"
import Reports from "./pages/reports"

function App() {

return (

<BrowserRouter>

<Navbar />

<Routes>

<Route path="/" element={<Dashboard />} />
<Route path="/create-project" element={<CreateProject />} />
<Route path="/upload" element={<UploadRegulation />} />
<Route path="/tasks" element={<Tasks />} />
<Route path="/reports" element={<Reports />} />

</Routes>

</BrowserRouter>

);

}

export default App;