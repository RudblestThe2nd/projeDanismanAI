import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Chat() {
  const [conversations, setConversations] = useState([]);
  const [activeConvId, setActiveConvId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const navigate = useNavigate();

  useEffect(() => { loadConversations(); }, []);
  async function loadConversations() {
    try { setConversations((await api.get("/conversations")).data); }
    catch { navigate("/login"); }
  }
  async function newConversation() {
    const conv = (await api.post("/conversations", { title: "Yeni Sohbet" })).data;
    setConversations((prev) => [conv, ...prev]);
    setActiveConvId(conv.id); setMessages([]);
  }
  async function selectConversation(id) {
    setActiveConvId(id);
    setMessages((await api.get(`/conversations/${id}/messages`)).data);
  }
  return <main><button onClick={newConversation}>Yeni Sohbet</button>{conversations.map(c => <button key={c.id} onClick={() => selectConversation(c.id)}>{c.title}</button>)}<textarea value={input} onChange={e => setInput(e.target.value)} /></main>;
}
