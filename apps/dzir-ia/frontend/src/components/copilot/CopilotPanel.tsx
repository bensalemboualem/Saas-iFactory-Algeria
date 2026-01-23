import { useEffect, useMemo, useRef, useState } from "react";
import { askApi, collectionsApi } from "../../api/client";

type Source = {
  index: number;
  score?: number | null;
  snippet?: string | null;
  title?: string | null;
};

type Msg =
  | { role: "user"; text: string }
  | { role: "assistant"; sources?: Source[], text: string; };

export default function CopilotPanel({ onClose }: { onClose: () => void }) {
  const [collections, setCollections] = useState<Array<{ id: string; name: string }>>([]);
  const [collectionId, setCollectionId] = useState<string>("");
  const collectionIds = useMemo(() => (collectionId ? [collectionId] : undefined), [collectionId]);

  const [messages, setMessages] = useState<Msg[]>([
    { role: "assistant", text: "Dzir IA Copilot â€” pose une question, je rÃ©ponds avec sources." },
  ]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const listRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await collectionsApi.list();
        const cols = (res.collections ?? []).map((c: any) => ({ id: c.id, name: c.name }));
        setCollections(cols);
        if (!collectionId && cols[0]?.id) setCollectionId(cols[0].id);
      } catch {
        // ignore
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    listRef.current?.scrollTo({ behavior: "smooth", top: listRef.current.scrollHeight });
  }, [messages]);

  async function send() {
    const q = input.trim();
    if (!q || busy) return;
    setInput("");
    setBusy(true);
    setMessages((m) => [...m, { role: "user", text: q }]);

    try {
      const res = await askApi.ask(q, collectionIds);
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          sources: (res.sources ?? []).map((s: any) => ({
            index: s.index,
            score: s.score,
            snippet: s.snippet,
            title: s.title,
          })),
          text: res.answer ?? "(rÃ©ponse vide)",
        },
      ]);
    } catch (e: any) {
      setMessages((m) => [...m, { role: "assistant", text: `âŒ ${String(e?.message ?? e)}` }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div style={{ background: "#020617", color: "#f8fafc", display: "flex", flexDirection: "column", height: "100%" }}>
      <div style={{ alignItems: "center", borderBottom: "1px solid rgba(255,255,255,.10)", display: "flex", gap: 10, height: 56, padding: "0 12px" }}>
        <div style={{ fontWeight: 900 }}>Copilot</div>
        <button onClick={onClose} style={{ background: "transparent", border: "none", color: "#f8fafc", cursor: "pointer", fontSize: 18, marginLeft: "auto" }}>
          âœ•
        </button>
      </div>

      <div style={{ borderBottom: "1px solid rgba(255,255,255,.10)", padding: 12 }}>
        <div style={{ fontSize: 12, marginBottom: 6, opacity: 0.7 }}>Collection (scope)</div>
        <select
          onChange={(e) => setCollectionId(e.target.value)}
          style={{ background: "rgba(255,255,255,.06)", border: "1px solid rgba(255,255,255,.12)", borderRadius: 12, color: "#f8fafc", padding: 10, width: "100%" }}
          value={collectionId}
        >
          <option value="">All</option>
          {collections.map((c) => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
      </div>

      <div ref={listRef} style={{ display: "flex", flex: 1, flexDirection: "column", gap: 10, overflow: "auto", padding: 12 }}>
        {messages.map((m, i) => (
          <div key={i} style={{ alignSelf: m.role === "user" ? "flex-end" : "flex-start", background: m.role === "user" ? "rgba(255,255,255,.06)" : "rgba(0,166,81,.10)", border: "1px solid rgba(255,255,255,.08)", borderRadius: 14, maxWidth: "92%", padding: "10px 12px", whiteSpace: "pre-wrap" }}>
            <div style={{ lineHeight: 1.5 }}>{m.text}</div>
            {"sources" in m && m.sources?.length ? (
              <div style={{ fontSize: 12, marginTop: 10, opacity: 0.95 }}>
                <div style={{ fontWeight: 900, marginBottom: 6 }}>Sources</div>
                {m.sources.map((s) => (
                  <div key={s.index} style={{ background: "rgba(0,0,0,.25)", borderRadius: 12, marginBottom: 8, padding: 10 }}>
                    <div style={{ fontWeight: 900 }}>
                      [{s.index}] {s.title ?? "(sans titre)"} {typeof s.score === "number" ? <span style={{ opacity: 0.7 }}>â€” {s.score.toFixed(3)}</span> : null}
                    </div>
                    {s.snippet ? <div style={{ marginTop: 6, opacity: 0.9 }}>{s.snippet}</div> : null}
                  </div>
                ))}
              </div>
            ) : null}
          </div>
        ))}
      </div>

      <div style={{ borderTop: "1px solid rgba(255,255,255,.10)", display: "flex", gap: 8, padding: 12 }}>
        <input
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter") send(); }}
          placeholder="Askâ€¦"
          style={{ background: "rgba(255,255,255,.06)", border: "1px solid rgba(255,255,255,.12)", borderRadius: 12, color: "#f8fafc", flex: 1, fontSize: 16, outline: "none", padding: 12 }}
          value={input}
        />
        <button
          disabled={busy}
          onClick={send}
          style={{ background: "#00a651", border: "none", borderRadius: "50%", color: "white", cursor: busy ? "not-allowed" : "pointer", fontWeight: 900, height: 44, width: 44 }}
          title="Send"
        >
          {busy ? "â€¦" : "â¬†"}
        </button>
      </div>
    </div>
  );
}
