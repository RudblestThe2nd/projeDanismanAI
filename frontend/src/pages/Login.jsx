import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const res = await api.post("/auth/login", { email, password });
      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("email", email);
      navigate("/");
    } catch {
      setError("Giriş başarısız.");
    }
  }

  return (
    <main>
      <h1>ProjeDanışmanAI</h1>
      <form onSubmit={handleSubmit}>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="E-posta" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Şifre" />
        <button type="submit">Giriş Yap</button>
      </form>
      {error && <p>{error}</p>}
      <Link to="/register">Kayıt ol</Link>
    </main>
  );
}
