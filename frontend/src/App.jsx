import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Signup from "./pages/Signup";
import Login from "./pages/Login";
import Task from "./pages/Task";
import UserManagment from "./pages/UserManagment";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/users/login" />} />

        <Route path="/users/signup" element={<Signup />} />
        <Route path="/users/login" element={<Login />} />
        <Route path="/tasks" element={<Task />} />
        <Route path="/UserManagment" element={<UserManagment />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;