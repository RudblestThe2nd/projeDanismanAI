import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Chat() {
  const [conversations, setConversations] = useState([]);
  const [activeConvId, setActiveConvId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [skill, setSkill] = useState("otomatik");
  const [loading, setLoading] = useState(false);
  const [pendingFile, setPendingFile] = useState(null);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();
  useEffect(()=>{loadConversations();},[]);
  async function loadConversations(){ try{setConversations((await api.get("/conversations")).data)}catch{navigate("/login")} }
  async function newConversation(){const c=(await api.post("/conversations",{title:"Yeni Sohbet"})).data;setConversations(p=>[c,...p]);setActiveConvId(c.id);setMessages([]);}
  async function sendMessage(){if(!input.trim()||!activeConvId||loading)return;const content=input;setInput("");setLoading(true);try{const r=await api.post("/chat",{conversation_id:activeConvId,message:content,skill});setMessages(p=>[...p,{role:"user",content},{role:"assistant",content:r.data.response}]);}finally{setLoading(false)}}
  async function uploadFile(){if(!pendingFile||!activeConvId)return;const fd=new FormData();fd.append("file",pendingFile);fd.append("conversation_id",activeConvId);fd.append("instruction","Bu belgeyi analiz et.");fd.append("skill",skill);const r=await api.post("/chat/upload",fd);setMessages(p=>[...p,{role:"assistant",content:r.data.response}]);setPendingFile(null);}
  return <main><button onClick={newConversation}>Yeni Sohbet</button><input ref={fileInputRef} type="file" onChange={e=>setPendingFile(e.target.files[0])}/>{pendingFile&&<button onClick={uploadFile}>Belgeyi Analiz Et</button>}<textarea value={input} onChange={e=>setInput(e.target.value)}/><button onClick={sendMessage}>Gönder</button>{messages.map((m,i)=><p key={i}>{m.content}</p>)}</main>;
}
