import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import api from "../services/api";
import CompassSVG from "../components/CompassSVG";
import pusulaImg from "../assets/pusula.png";

const SKILLS = [
  { value: "otomatik",                          label: "Otomatik Tespit" },
  { value: "project_idea_refinement",           label: "Proje Fikri Netleştirme" },
  { value: "report_section_writer",             label: "Rapor Bölümü Yazma" },
  { value: "tubitak_application_guidance",      label: "TÜBİTAK Başvuru" },
  { value: "teknofest_ktr_ptr_guidance",        label: "TEKNOFEST KTR/PTR" },
  { value: "feasibility_and_risk_check",        label: "Risk Analizi" },
  { value: "title_abstract_generator",          label: "Başlık ve Özet" },
  { value: "presentation_and_jury_preparation", label: "Sunum Hazırlığı" },
];

const QUICK_ACTIONS = [
  { icon: "</>", label: "Kod",               skill: "project_idea_refinement",    prompt: "Proje fikrimi geliştirmeme yardım et",                    highlight: false },
  { icon: "✎",  label: "Yaz",               skill: "report_section_writer",      prompt: "Rapor bölümü yazmama yardım et",                          highlight: false },
  { icon: "⚡",  label: "Analiz",            skill: "feasibility_and_risk_check", prompt: "Projemi risk ve fizibilite açısından analiz et",           highlight: false },
  { icon: "◈",  label: "Pusula'nın Seçimi", skill: "otomatik",                   prompt: "Projem hakkında danışmak istiyorum",                      highlight: true  },
];

function getDisplayName() {
  const email = localStorage.getItem("email") || "";
  const local = email.split("@")[0] || "Kullanıcı";
  return local.charAt(0).toUpperCase() + local.slice(1);
}

export default function Chat() {
  const [conversations,     setConversations]     = useState([]);
  const [activeConvId,      setActiveConvId]      = useState(null);
  const [messages,          setMessages]          = useState([]);
  const [input,             setInput]             = useState("");
  const [skill,             setSkill]             = useState("otomatik");
  const [loading,           setLoading]           = useState(false);
  const [uploadLoading,     setUploadLoading]     = useState(false);
  const [uploadInstruction, setUploadInstruction] = useState("");
  const [showUploadModal,   setShowUploadModal]   = useState(false);
  const [pendingFile,       setPendingFile]       = useState(null);
  const [pendingChunks,     setPendingChunks]     = useState(null);
  const [showSkillMenu,     setShowSkillMenu]     = useState(false);

  const messagesEndRef = useRef(null);
  const fileInputRef   = useRef(null);
  const navigate       = useNavigate();

  useEffect(() => { loadConversations(); }, []);
  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  async function loadConversations() {
    try {
      const res = await api.get("/conversations");
      setConversations(res.data);
    } catch {
      navigate("/login");
    }
  }

  async function newConversation(overrideSkill) {
    const res  = await api.post("/conversations", { title: "Yeni Sohbet" });
    const conv = res.data;
    setConversations((prev) => [conv, ...prev]);
    setActiveConvId(conv.id);
    setMessages([]);
    setPendingChunks(null);
    if (overrideSkill) setSkill(overrideSkill);
    return conv.id;
  }

  async function selectConversation(id) {
    setActiveConvId(id);
    setPendingChunks(null);
    const res = await api.get(`/conversations/${id}/messages`);
    setMessages(res.data);
  }

  async function deleteConversation(e, id) {
    e.stopPropagation();
    await api.delete(`/conversations/${id}`);
    setConversations((prev) => prev.filter((c) => c.id !== id));
    if (activeConvId === id) { setActiveConvId(null); setMessages([]); setPendingChunks(null); }
  }

  async function sendMessage(overrideConvId, overrideInput) {
    const convId  = overrideConvId ?? activeConvId;
    const content = overrideInput  ?? input;
    if (!content.trim() || !convId || loading) return;

    if (pendingChunks && !overrideConvId) {
      const lower = content.trim().toLowerCase();
      const isYes = ["evet", "e", "devam", "devam et", "yes"].includes(lower);
      setMessages((prev) => [...prev, { role: "user", content }]);
      setInput("");
      if (!isYes) {
        setPendingChunks(null);
        setMessages((prev) => [...prev, { role: "assistant", content: "Tamam, analizi durdurdum. Başka bir konuda yardımcı olabilir miyim?" }]);
        return;
      }
      await processNextChunk();
      return;
    }

    const userMsg = { role: "user", content };
    setMessages((prev) => [...prev, userMsg]);
    if (!overrideConvId) setInput("");
    setLoading(true);

    try {
      const res = await api.post("/chat", { conversation_id: convId, message: content, skill });
      setMessages((prev) => [...prev, { role: "assistant", content: res.data.response, skill_used: res.data.skill_used }]);
      loadConversations();
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "Bir hata oluştu. Tekrar dene." }]);
    } finally {
      setLoading(false);
    }
  }

  async function processNextChunk() {
    if (!pendingChunks || pendingChunks.remaining.length === 0) return;
    setUploadLoading(true);
    const { remaining, chunkIndex, totalChunks, filename, instruction } = pendingChunks;
    try {
      const res = await api.post("/chat/upload/continue", {
        conversation_id: activeConvId, chunk: remaining[0],
        chunk_index: chunkIndex, total_chunks: totalChunks, filename, instruction, skill,
      }, { timeout: 300000 });
      setMessages((prev) => [...prev, { role: "assistant", content: res.data.response, skill_used: res.data.skill_used }]);
      if (res.data.has_more) {
        setPendingChunks({ remaining: remaining.slice(1), chunkIndex: chunkIndex + 1, totalChunks, filename, instruction });
      } else {
        setPendingChunks(null);
        loadConversations();
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: `❌ Bölüm işleme hatası: ${err.response?.data?.detail || err.message}` }]);
      setPendingChunks(null);
    } finally {
      setUploadLoading(false);
    }
  }

  function handleFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;
    const ext = "." + file.name.split(".").pop().toLowerCase();
    if (![".pdf", ".docx", ".txt"].includes(ext)) { alert("Sadece PDF, DOCX veya TXT dosyaları yüklenebilir."); return; }
    if (file.size > 10 * 1024 * 1024) { alert("Dosya çok büyük. Maksimum 10MB."); return; }
    setPendingFile(file);
    setUploadInstruction("Bu belgeyi analiz et ve TEKNOFEST/TÜBİTAK açısından değerlendir.");
    setShowUploadModal(true);
    e.target.value = "";
  }

  async function uploadFile() {
    if (!pendingFile || !activeConvId || uploadLoading) return;
    setShowUploadModal(false);
    setUploadLoading(true);
    setMessages((prev) => [...prev, { role: "user", content: `📎 **${pendingFile.name}** yüklendi\n\n${uploadInstruction}` }]);
    const formData = new FormData();
    formData.append("file", pendingFile);
    formData.append("conversation_id", activeConvId);
    formData.append("instruction", uploadInstruction);
    formData.append("skill", skill);
    try {
      const res = await api.post("/chat/upload", formData, { headers: { "Content-Type": "multipart/form-data" }, timeout: 300000 });
      setMessages((prev) => [...prev, { role: "assistant", content: res.data.response, skill_used: res.data.skill_used }]);
      if (res.data.has_more) {
        setPendingChunks({ remaining: res.data.remaining_chunks, chunkIndex: 1, totalChunks: res.data.total_chunks, filename: res.data.filename, instruction: res.data.instruction });
      } else {
        loadConversations();
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: `❌ Dosya yükleme hatası: ${err.response?.data?.detail || err.message}` }]);
    } finally {
      setUploadLoading(false);
      setPendingFile(null);
    }
  }

  async function downloadWord() {
    if (!activeConvId || loading) return;
    const last = [...messages].reverse().find((m) => m.role === "user");
    if (!last) { alert("Önce bir mesaj gönder."); return; }
    try {
      const res = await api.post("/chat/word", { conversation_id: activeConvId, message: last.content, skill }, { responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a   = document.createElement("a");
      a.href = url; a.download = "rapor.docx";
      document.body.appendChild(a); a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("Word dosyası oluşturulamadı: " + (err.message || "bilinmeyen hata"));
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("email");
    navigate("/login");
  }

  async function handleQuickAction(action) {
    const convId = await newConversation(action.skill);
    await sendMessage(convId, action.prompt);
  }

  const isLoading   = loading || uploadLoading;
  const displayName = getDisplayName();

  return (
    <div style={S.layout}>
      {/* Upload Modal */}
      {showUploadModal && (
        <div style={S.modalOverlay}>
          <div style={S.modal}>
            <h3 style={S.modalTitle}>📎 {pendingFile?.name}</h3>
            <p style={S.modalSub}>Bu dosyayla ne yapmamı istersin?</p>
            <textarea
              style={S.modalTA} value={uploadInstruction} rows={4}
              onChange={(e) => setUploadInstruction(e.target.value)}
              placeholder="Örnek: Bu rapordaki hataları bul ve düzelt."
            />
            <div style={S.modalBtns}>
              <button style={S.modalCancel} onClick={() => { setShowUploadModal(false); setPendingFile(null); }}>İptal</button>
              <button style={S.modalConfirm} onClick={uploadFile} disabled={!uploadInstruction.trim()}>Analiz Et</button>
            </div>
          </div>
        </div>
      )}

      {/* Sidebar */}
      <aside style={S.sidebar}>
        <div style={S.sidebarTop}>
          <span style={S.logoText}>ProjeDanışmanAI</span>
        </div>
        <div style={S.divider} />

        <button style={S.newChatBtn} onClick={() => newConversation()}>+ Yeni Sohbet</button>

        <span style={S.convLabel}>SON SOHBETLER</span>

        <div style={S.convList}>
          {conversations.map((c) => (
            <div
              key={c.id}
              style={{
                ...S.convItem,
                background:  activeConvId === c.id ? "var(--bg-tertiary)" : "transparent",
                borderLeft:  activeConvId === c.id ? "2px solid var(--border-bright)" : "2px solid transparent",
              }}
              onClick={() => selectConversation(c.id)}
            >
              <span style={S.convTitle}>{activeConvId === c.id ? "▸ " : ""}{c.title}</span>
              <button style={S.deleteBtn} onClick={(e) => deleteConversation(e, c.id)}>✕</button>
            </div>
          ))}
        </div>

        <div style={S.divider} />
        <div style={S.userStrip} onClick={logout} title="Çıkış Yap">
          <img src={pusulaImg} width={22} height={22} alt="" style={{ flexShrink: 0, objectFit: "contain" }} />
          <div>
            <div style={S.userName}>{displayName}</div>
            <div style={S.userPlan}>Pro plan</div>
          </div>
        </div>
      </aside>

      {/* Main */}
      <main style={S.main}>
        {!activeConvId ? (
          <WelcomeView
            displayName={displayName}
            input={input}
            setInput={setInput}
            skill={skill}
            setSkill={setSkill}
            onQuickAction={handleQuickAction}
            onNewConversation={newConversation}
            onSendMessage={sendMessage}
            onLogout={logout}
          />
        ) : (
          <>
            {/* Top bar */}
            <div style={S.topBar}>
              <span style={S.topBarTitle}>
                {conversations.find((c) => c.id === activeConvId)?.title || "Sohbet"}
              </span>
              <button style={S.shareBtn}>Paylaş</button>
            </div>

            {/* Messages */}
            <div style={S.messages}>
              <div style={S.dateSep}>— bugün —</div>

              {messages.map((msg, i) => (
                <div key={i} style={{ ...S.msgRow, justifyContent: msg.role === "user" ? "flex-end" : "flex-start" }}>
                  {msg.role === "assistant" && <AiAvatar />}
                  <div style={msg.role === "user" ? S.userBubble : S.aiBubble}>
                    <div className="md-content">
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                    {msg.skill_used && msg.role === "assistant" && (
                      <div style={S.skillBadge}>{msg.skill_used}</div>
                    )}
                  </div>
                  {msg.role === "user" && <UserAvatar />}
                </div>
              ))}

              {isLoading && (
                <div style={{ ...S.msgRow, justifyContent: "flex-start" }}>
                  <AiAvatar />
                  <div style={S.aiBubble}>
                    <TypingDots label={uploadLoading ? "Belge analiz ediliyor" : undefined} />
                  </div>
                </div>
              )}

              {pendingChunks && !isLoading && (
                <div style={S.continueRow}>
                  <button style={S.continueYes} onClick={processNextChunk}>✅ Evet, devam et</button>
                  <button style={S.continueNo} onClick={() => {
                    setPendingChunks(null);
                    setMessages((prev) => [...prev, { role: "assistant", content: "Tamam, analizi durdurdum." }]);
                  }}>⏹ Dur</button>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input area */}
            <div style={S.inputArea}>
              <input ref={fileInputRef} type="file" accept=".pdf,.docx,.txt" style={{ display: "none" }} onChange={handleFileSelect} />

              <div style={S.inputBox}>
                <textarea
                  style={S.textarea}
                  placeholder={pendingChunks ? "Devam etmemi ister misin? (evet / hayır)" : "Bir mesaj yaz..."}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  rows={2}
                />
                <div style={S.inputActions}>
                  <button style={S.iconBtn} onClick={() => !isLoading && fileInputRef.current?.click()} title="PDF veya DOCX yükle" disabled={isLoading}>📎</button>
                  <button style={S.iconBtn} onClick={downloadWord} title="Son yanıtı Word olarak indir" disabled={isLoading}>📄</button>
                  <div style={{ position: "relative" }}>
                    <button style={S.iconBtn} onClick={() => setShowSkillMenu((p) => !p)} title="Skill seç">🎯</button>
                    {showSkillMenu && (
                      <div style={S.skillMenu}>
                        {SKILLS.map((s) => (
                          <button
                            key={s.value}
                            style={{ ...S.skillMenuItem, color: skill === s.value ? "var(--text-accent)" : "var(--text-mid)" }}
                            onClick={() => { setSkill(s.value); setShowSkillMenu(false); }}
                          >
                            {skill === s.value ? "▸ " : ""}{s.label}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                  <button
                    style={{ ...S.sendBtn, opacity: isLoading || !input.trim() ? 0.35 : 1 }}
                    onClick={() => sendMessage()}
                    disabled={isLoading || !input.trim()}
                    title="Gönder"
                  >
                    ⌁
                  </button>
                </div>
              </div>

              <div style={S.disclaimer}>ProjeDanışmanAI hata yapabilir. Önemli bilgileri doğrulayın.</div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

/* ── Sub-components ─────────────────────────────────── */

function WelcomeView({ displayName, input, setInput, skill, setSkill, onQuickAction, onNewConversation, onSendMessage, onLogout }) {
  return (
    <div style={W.container}>
      <nav style={W.nav}>
        <span style={W.navLogo}>ProjeDanışmanAI</span>
        <button style={W.navLogout} onClick={onLogout}>Çıkış</button>
      </nav>

      <div style={W.center}>
        <CompassSVG size="large" />
        <h1 style={W.greeting}>İyi günler, {displayName}</h1>
        <p style={W.tagline}>Pusulayı kullanmaya hemen başlayın ✦</p>

        <div style={W.promptBox}>
          <textarea
            style={W.promptInput}
            placeholder="Bugün nasıl yardımcı olabilirim?"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={async (e) => {
              if (e.key === "Enter" && !e.shiftKey && input.trim()) {
                e.preventDefault();
                const convId = await onNewConversation(skill);
                await onSendMessage(convId, input);
              }
            }}
            rows={2}
          />
          <div style={W.promptBar}>
            <span style={W.promptPlus}>+</span>
            <select style={W.skillSelect} value={skill} onChange={(e) => setSkill(e.target.value)}>
              {SKILLS.map((s) => (
                <option key={s.value} value={s.value}>{s.label}</option>
              ))}
            </select>
          </div>
        </div>

        <div style={W.chips}>
          {QUICK_ACTIONS.map((a) => (
            <button
              key={a.label}
              style={a.highlight ? W.chipHighlight : W.chip}
              onClick={() => onQuickAction(a)}
            >
              <span style={{ marginRight: 5 }}>{a.icon}</span>{a.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

function AiAvatar() {
  return (
    <img src={pusulaImg} width={24} height={24} alt="AI"
      style={{ flexShrink: 0, marginTop: 2, objectFit: "contain" }} />
  );
}

function UserAvatar() {
  return (
    <img src={pusulaImg} width={24} height={24} alt=""
      style={{ flexShrink: 0, marginTop: 2, objectFit: "contain", opacity: 0.6 }} />
  );
}

function TypingDots({ label }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
      {[["#1e4888", "0s"], ["#2a6abf", "0.2s"], ["#60b0ff", "0.4s"]].map(([color, delay], i) => (
        <span key={i} style={{
          width: 7, height: 7, borderRadius: "50%", background: color,
          display: "inline-block",
          animation: `dot-pulse 1.4s ease-in-out ${delay} infinite`,
        }} />
      ))}
      {label && <span style={{ fontSize: 12, color: "var(--text-dim)", marginLeft: 4 }}>{label}...</span>}
    </div>
  );
}

/* ── Styles ─────────────────────────────────────────── */

const S = {
  layout: { display: "flex", height: "100vh", background: "var(--bg-primary)", overflow: "hidden" },

  modalOverlay: { position: "fixed", inset: 0, background: "rgba(0,0,0,0.8)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000 },
  modal: { background: "var(--bg-secondary)", border: "1px solid var(--border-mid)", borderRadius: 12, padding: 24, width: 440, display: "flex", flexDirection: "column", gap: 14 },
  modalTitle: { margin: 0, fontSize: 14, color: "var(--text-bright)", fontFamily: "Georgia, serif", fontStyle: "italic" },
  modalSub:   { margin: 0, fontSize: 12, color: "var(--text-mid)",    fontFamily: "Georgia, serif", fontStyle: "italic" },
  modalTA:    { background: "var(--bg-primary)", border: "1px solid var(--border-mid)", borderRadius: 8, color: "var(--text-bright)", padding: "10px 14px", fontSize: 13, resize: "vertical", outline: "none", lineHeight: 1.5, fontFamily: "Georgia, serif" },
  modalBtns:  { display: "flex", gap: 10, justifyContent: "flex-end" },
  modalCancel:  { background: "none", border: "1px solid var(--border-mid)", borderRadius: 8, color: "var(--text-mid)", padding: "7px 16px", fontSize: 12, cursor: "pointer", fontFamily: "Georgia, serif" },
  modalConfirm: { background: "var(--bg-card)", border: "1px solid var(--text-accent)", borderRadius: 8, color: "var(--text-bright)", padding: "7px 20px", fontSize: 12, cursor: "pointer", fontFamily: "Georgia, serif" },

  sidebar: { width: 182, minWidth: 182, background: "var(--bg-secondary)", borderRight: "1px solid var(--border-subtle)", display: "flex", flexDirection: "column", paddingBottom: 12 },
  sidebarTop: { padding: "14px 14px 0" },
  logoText:  { fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 12, color: "var(--text-accent)" },
  divider:   { height: 1, background: "var(--border-subtle)", margin: "10px 0" },
  newChatBtn: { margin: "0 10px 10px", background: "var(--bg-card)", border: "0.6px solid var(--text-accent)", borderRadius: 7, padding: "9px 0", color: "var(--text-bright)", fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 11, cursor: "pointer", textAlign: "center" },
  convLabel:  { fontFamily: "monospace", fontSize: 9, color: "var(--text-dim)", letterSpacing: "0.5px", padding: "0 14px", marginBottom: 6 },
  convList:   { flex: 1, overflowY: "auto", display: "flex", flexDirection: "column", gap: 2, padding: "0 8px" },
  convItem:   { display: "flex", alignItems: "center", justifyContent: "space-between", padding: "7px 8px", borderRadius: 3, cursor: "pointer", gap: 4 },
  convTitle:  { fontSize: 10, color: "var(--text-mid)", fontFamily: "Georgia, serif", fontStyle: "italic", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", flex: 1 },
  deleteBtn:  { background: "none", border: "none", color: "var(--text-dim)", cursor: "pointer", fontSize: 10, flexShrink: 0 },
  userStrip:  { display: "flex", alignItems: "center", gap: 8, padding: "8px 14px", cursor: "pointer" },
  userName:   { fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 11, color: "var(--text-mid)" },
  userPlan:   { fontFamily: "monospace", fontSize: 9, color: "var(--text-dim)" },

  main: { flex: 1, display: "flex", flexDirection: "column", overflow: "hidden" },

  topBar:      { background: "var(--bg-secondary)", borderBottom: "1px solid var(--border-subtle)", padding: "10px 20px", display: "flex", alignItems: "center", justifyContent: "space-between" },
  topBarTitle: { fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 11, color: "var(--text-mid)" },
  shareBtn:    { background: "var(--bg-secondary)", border: "1px solid var(--border-mid)", borderRadius: 5, color: "var(--text-mid)", padding: "4px 14px", fontSize: 10, cursor: "pointer", fontFamily: "Georgia, serif" },

  messages: { flex: 1, overflowY: "auto", padding: "20px 24px", display: "flex", flexDirection: "column", gap: 14 },
  dateSep:  { fontFamily: "monospace", fontSize: 9, color: "var(--text-dim)", textAlign: "center", marginBottom: 6 },
  msgRow:   { display: "flex", alignItems: "flex-start", gap: 8 },
  userBubble: {
    maxWidth: "68%", padding: "10px 14px", borderRadius: 10,
    background: "var(--bg-tertiary)", border: "0.8px solid var(--border-bright)",
    color: "var(--text-accent)", fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 10,
  },
  aiBubble: {
    maxWidth: "68%", padding: "10px 14px", borderRadius: 10,
    background: "var(--bg-secondary)", border: "0.8px solid #0e2040",
    color: "var(--text-mid)", fontFamily: "Georgia, serif", fontStyle: "italic",
  },
  skillBadge:  { marginTop: 6, fontSize: 10, color: "var(--text-dim)", borderTop: "1px solid var(--border-subtle)", paddingTop: 5, fontFamily: "monospace" },
  continueRow: { display: "flex", gap: 10, paddingLeft: 32 },
  continueYes: { background: "var(--bg-tertiary)", border: "1px solid var(--border-bright)", borderRadius: 8, color: "var(--text-accent)", padding: "7px 14px", fontSize: 12, cursor: "pointer", fontFamily: "Georgia, serif" },
  continueNo:  { background: "#1a0808", border: "1px solid #3a1a1a", borderRadius: 8, color: "#a05050", padding: "7px 14px", fontSize: 12, cursor: "pointer", fontFamily: "Georgia, serif" },

  inputArea:    { background: "var(--bg-secondary)", borderTop: "1px solid var(--border-subtle)", padding: "12px 20px 10px" },
  inputBox:     { border: "0.8px dashed var(--border-mid)", outline: "0.25px solid rgba(96,176,255,0.25)", borderRadius: 10, background: "var(--bg-primary)", display: "flex", flexDirection: "column" },
  textarea:     { background: "transparent", border: "none", outline: "none", color: "var(--text-accent)", fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 11, padding: "12px 14px", resize: "none", lineHeight: 1.5 },
  inputActions: { display: "flex", alignItems: "center", gap: 4, padding: "6px 10px", borderTop: "1px solid var(--border-subtle)" },
  iconBtn:      { background: "none", border: "none", cursor: "pointer", fontSize: 15, padding: "2px 6px", opacity: 0.7 },
  skillMenu: {
    position: "absolute", bottom: "calc(100% + 4px)", left: 0,
    background: "var(--bg-secondary)", border: "1px solid var(--border-mid)",
    borderRadius: 8, minWidth: 210, display: "flex", flexDirection: "column",
    zIndex: 10, boxShadow: "0 4px 16px rgba(0,0,0,0.5)",
  },
  skillMenuItem: { background: "none", border: "none", padding: "8px 14px", fontSize: 11, cursor: "pointer", textAlign: "left", fontFamily: "Georgia, serif", fontStyle: "italic" },
  sendBtn:       { marginLeft: "auto", background: "none", border: "none", color: "var(--text-dim)", fontSize: 18, cursor: "pointer", padding: "2px 8px" },
  disclaimer:    { fontFamily: "monospace", fontSize: 9, color: "var(--border-mid)", textAlign: "center", marginTop: 8 },
};

const W = {
  container: { flex: 1, display: "flex", flexDirection: "column", background: "var(--bg-primary)" },
  nav: { background: "var(--bg-secondary)", borderBottom: "1px solid var(--border-subtle)", padding: "10px 24px", display: "flex", alignItems: "center", justifyContent: "space-between" },
  navLogo:   { fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 13, color: "var(--text-accent)" },
  navLogout: { background: "none", border: "none", color: "var(--text-dim)", fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 11, cursor: "pointer" },
  center: { flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 12, padding: "24px 40px" },
  greeting: { fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 26, color: "var(--text-bright)", margin: 0 },
  tagline:  { fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 12, color: "#3a6aa0", margin: 0 },
  promptBox: { width: 420, background: "var(--bg-secondary)", border: "0.8px dashed var(--border-mid)", outline: "0.3px solid rgba(96,176,255,0.3)", borderRadius: 12 },
  promptInput: { width: "100%", background: "transparent", border: "none", outline: "none", color: "var(--text-dim)", fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 11, padding: "14px 16px", resize: "none", lineHeight: 1.5, boxSizing: "border-box" },
  promptBar:   { borderTop: "1px solid var(--border-subtle)", padding: "8px 14px", display: "flex", alignItems: "center", justifyContent: "space-between" },
  promptPlus:  { color: "var(--text-dim)", fontFamily: "monospace", fontSize: 14, cursor: "pointer" },
  skillSelect: { background: "transparent", border: "none", outline: "none", color: "var(--text-dim)", fontFamily: "monospace", fontSize: 10, cursor: "pointer" },
  chips: { display: "flex", gap: 8, flexWrap: "wrap", justifyContent: "center", marginTop: 4 },
  chip: { background: "var(--bg-secondary)", border: "0.8px solid var(--border-mid)", borderRadius: 13, padding: "6px 16px", color: "var(--text-mid)", fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 10, cursor: "pointer" },
  chipHighlight: { background: "var(--bg-card)", border: "0.8px solid var(--text-accent)", borderRadius: 13, padding: "6px 16px", color: "var(--text-bright)", fontFamily: "Georgia, serif", fontStyle: "italic", fontSize: 10, cursor: "pointer" },
};
