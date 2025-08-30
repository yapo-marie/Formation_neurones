
import { Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import Profile from "./components/Profile";
import { RequireToken } from "./components/Auth";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/profile" element={<RequireToken> <Profile /></RequireToken>}/>
              
      </Routes>
    </div>
  );
}

export default App;
