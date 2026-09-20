import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";
import CompassSVG from "../components/CompassSVG";

const STARS = [
  [9, 9], [8, 85], [78, 6], [62, 92], [31, 88],
  [76, 82], [14, 44], [50, 4], [88, 55], [40, 70],
];

export default function Register() {
  const [email, setEmail]       = useState("");
  const [password, setPassword] = useState("");
  const [error, setError]       = useState("");
  const [success, setSuccess]   = useState("");
  const navigate                = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError(""); setSuccess("");
    try {
      await api.post("/auth/register", { email, password });
      setSuccess("Kayıt başarılı! Giriş yapılıyor...");
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      setError(err.response?.data?.detail || "Kayıt başarısız.");
    }
  }

  return (
    <div style={S.page}>
      {STARS.map(([top, left], i) => (
        <span key={i} style={{
          ...S.star,
          top: `${top}%`, left: `${left}%`,
          width:  i % 3 === 0 ? 2 : 1.5,
          height: i % 3 === 0 ? 2 : 1.5,
          animationDelay: `${(i * 0.7) % 3}s`,
        }} />
      ))}

      <div style={S.card}>
        <div style={S.compassWrap}>
          <CompassSVG size="small" />
        </div>

        <h1 style={S.title}>ProjeDanışmanAI</h1>
        <p style={S.subtitle}>Yeni hesap oluştur</p>

        {error   && <div style={S.errorBox}>{error}</div>}
        {success && <div style={S.successBox}>{success}</div>}

        <form onSubmit={handleSubmit} style={S.form}>
          <input
            style={S.input} type="email" placeholder="Email"
            value={email} onChange={(e) => setEmail(e.target.value)} required
          />
          <input
            style={S.input} type="password" placeholder="Şifre (en az 6 karakter)"
            value={password} onChange={(e) => setPassword(e.target.value)}
            minLength={6} required
          />
          <button style={S.btn} type="submit">Kayıt Ol</button>
        </form>

        <hr style={S.divider} />

        <p style={S.linkRow}>
          Zaten hesabın var mı?{" "}
          <Link to="/login" style={S.link}>Giriş Yap</Link>
        </p>
      </div>
    </div>
  );
}

const S = {
  page: {
    minHeight: "100vh", width: "100%",
    background: "var(--bg-primary)",
    display: "flex", alignItems: "center", justifyContent: "center",
    position: "relative", overflow: "hidden",
  },
  star: {
    position: "absolute", borderRadius: "50%",
    background: "#a0d4ff",
    animation: "twinkle 3s ease-in-out infinite",
  },
  card: {
    background: "var(--bg-secondary)",
    border: "1px solid #1e4888",
    outline: "0.4px solid rgba(96,176,255,0.3)",
    borderRadius: 14, padding: "36px 32px", width: 280,
    display: "flex", flexDirection: "column", alignItems: "center",
    position: "relative", zIndex: 1,
  },
  compassWrap: { marginBottom: 16 },
  title: {
    fontFamily: "Georgia, serif", fontStyle: "italic",
    fontSize: 14, color: "var(--text-bright)",
    marginBottom: 4, textAlign: "center",
  },
  subtitle: {
    fontFamily: "Georgia, serif", fontStyle: "italic",
    fontSize: 10, color: "#3a6aa0",
    marginBottom: 20, textAlign: "center",
  },
  errorBox: {
    background: "#1a050a", border: "1px solid #7a2a2a",
    borderRadius: 8, color: "#ff6b6b",
    padding: "8px 12px", fontSize: 12, marginBottom: 10, width: "100%",
  },
  successBox: {
    background: "#051a0a", border: "1px solid #2a7a2a",
    borderRadius: 8, color: "#6bff8b",
    padding: "8px 12px", fontSize: 12, marginBottom: 10, width: "100%",
  },
  form: { display: "flex", flexDirection: "column", gap: 10, width: "100%" },
  input: {
    background: "var(--bg-primary)", border: "1px solid var(--border-mid)",
    borderRadius: 7, padding: "10px 14px",
    color: "var(--text-bright)", fontSize: 11,
    fontFamily: "Georgia, serif", fontStyle: "italic",
    outline: "none", width: "100%",
  },
  btn: {
    background: "var(--bg-card)", border: "1px solid var(--text-accent)",
    borderRadius: 9, padding: 11, color: "var(--text-bright)",
    fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 12,
    cursor: "pointer", width: "100%",
  },
  divider: {
    border: "none", borderTop: "1px solid var(--border-subtle)",
    width: "100%", margin: "18px 0 12px",
  },
  linkRow: {
    fontFamily: "Georgia, serif", fontStyle: "italic",
    fontSize: 10, color: "var(--text-dim)", textAlign: "center",
  },
  link: { color: "var(--text-accent)", textDecoration: "none" },
};
