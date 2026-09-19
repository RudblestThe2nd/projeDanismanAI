import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      await api.post("/auth/register", { email, password });
      navigate("/login");
    } catch {
      setError("Kayıt oluşturulamadı.");
    }
  }

  return (
    <main>
      <h1>Hesap Oluştur</h1>
      <form onSubmit={handleSubmit}>
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="E-posta" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Şifre" />
        <button type="submit">Kayıt Ol</button>
      </form>
      {error && <p>{error}</p>}
      <Link to="/login">Giriş yap</Link>
    </main>
  );
}
