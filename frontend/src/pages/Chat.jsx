import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

const SKILLS = ["otomatik", "project_idea_refinement", "report_section_writer", "feasibility_and_risk_check"];

export default function Chat() {
  const [conversations, setConversations] = useState([]);
  const [activeConvId, setActiveConvId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [skill, setSkill] = useState("otomatik");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  useEffect(() => { loadConversations(); }, []);
  async function loadConversations(){ try { setConversations((await api.get("/conversations")).data); } catch { navigate("/login"); } }
  async function newConversation(){ const c=(await api.post("/conversations",{title:"Yeni Sohbet"})).data; setConversations(p=>[c,...p]); setActiveConvId(c.id); setMessages([]); }
  async function selectConversation(id){ setActiveConvId(id); setMessages((await api.get(`/conversations/${id}/messages`)).data); }
  async function sendMessage(){ if(!input.trim()||!activeConvId||loading)return; const content=input; setMessages(p=>[...p,{role:"user",content}]); setInput(""); setLoading(true); try { const r=await api.post("/chat",{conversation_id:activeConvId,message:content,skill}); setMessages(p=>[...p,{role:"assistant",content:r.data.response}]); } finally { setLoading(false); } }
  return <main><button onClick={newConversation}>Yeni Sohbet</button><select value={skill} onChange={e=>setSkill(e.target.value)}>{SKILLS.map(s=><option key={s}>{s}</option>)}</select>{conversations.map(c=><button key={c.id} onClick={()=>selectConversation(c.id)}>{c.title}</button>)}{messages.map((m,i)=><p key={i}><b>{m.role}:</b> {m.content}</p>)}<textarea value={input} onChange={e=>setInput(e.target.value)} /><button onClick={sendMessage}>Gönder</button></main>;
}
