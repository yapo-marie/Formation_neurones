import { useNavigate } from "react-router-dom";
import { setToken } from "./Auth";
import { useState } from "react";
import api from "../api";

export default function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const login = () => {
    if (!username || !password) return;

    api.post<{ token: string }>("/login", { username, password })
        .then((response) => {
        const { token } = response.data;
        if (token) {
          setToken(token);
          navigate("/profile");
        }
      })
      .catch((error) => {
        console.error("Login error:", error);
        alert("Login failed");
      });
  };

  return (
    <div style={{ minHeight: 800, marginTop: 30 }}>
      <h1>Login page</h1>
      <form onSubmit={(e) => { e.preventDefault(); login(); }}>
        <div>
          <label>Username</label>
          <input type="text" onChange={(e) => setUsername(e.target.value)} />
        </div>
        <div>
          <label>Password</label>
          <input type="password" onChange={(e) => setPassword(e.target.value)} />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}
