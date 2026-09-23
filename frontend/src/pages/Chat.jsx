import { useState } from "react";

export default function Chat() {
  const [input, setInput] = useState("");
  return (
    <main>
      <h1>ProjeDanışmanAI</h1>
      <textarea value={input} onChange={(e) => setInput(e.target.value)} placeholder="Projen hakkında yaz..." />
    </main>
  );
}
