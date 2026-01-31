import React, { useEffect, useMemo, useRef, useState } from "react";
import { captureApi, collectionsApi, API_BASE } from "../../api/client";
import "./dziria-chat.css";

type Source = {
  chunkId?: string;
  documentId?: string;
  index: number;
  position?: number | null;
  score?: number | null;
  snippet?: string | null;
  sourceUrl?: string | null;
  title?: string | null;
};

type Msg =
  | { role: "user"; text: string }
  | { role: "assistant"; sources?: Source[]; text: string }
  | { role: "system"; text: string };

type Mode = "chat" | "search";

type Provider = "auto" | "openai" | "local";

function getDevToken(): string | null {
  const stored = localStorage.getItem("token");
  if (stored) return stored;
  return import.meta.env.DEV ? "dev" : null;
}

async function postJson<T>(endpoint: string, body: any): Promise<T> {
  const token = getDevToken();
  const res = await fetch(`${API_BASE}${endpoint}`, {
    body: JSON.stringify(body),
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    method: "POST",
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err?.message || err?.error || `HTTP ${res.status}`);
  }
  return res.json();
}

function fileToText(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const fr = new FileReader();
    fr.addEventListener("load", () => resolve(String(fr.result ?? "")));
    fr.onerror = () => reject(new Error("File read error"));
    fr.readAsText(file);
  });
}

function fileToBase64DataUrl(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const fr = new FileReader();
    fr.addEventListener("load", () => resolve(String(fr.result ?? "")));
    fr.onerror = () => reject(new Error("File read error"));
    fr.readAsDataURL(file);
  });
}

const MODEL_PRESETS: Record<
  Exclude<Provider, "auto">,
  Array<{ label: string; value: string }>
> = {
  local: [{ label: "llama3.2:3b (Ollama)", value: "llama3.2:3b" }],
  openai: [
    { label: "gpt-4o-mini-2024-07-18", value: "gpt-4o-mini-2024-07-18" },
    { label: "gpt-4o", value: "gpt-4o" },
  ],
};

export default function DzirIAChat() {
  const [mode, setMode] = useState<Mode>("chat");

  // collections (scope)
  const [collections, setCollections] = useState<Array<{ id: string; name: string }>>([]);
  const [collectionId, setCollectionId] = useState<string>("");
  const collectionIds = useMemo(
    () => (collectionId ? [collectionId] : undefined),
    [collectionId]
  );

  // LLM routing
  const [provider, setProvider] = useState<Provider>("auto");
  const [model, setModel] = useState<string>("auto");

  // flags "tools" (UX only, injected into systemPrompt)
  const [thinking, setThinking] = useState(false);
  const [deepResearch, setDeepResearch] = useState(false);
  const [analysisTool, setAnalysisTool] = useState(false);

  // menus
  const [plusOpen, setPlusOpen] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);
  const plusBtnRef = useRef<HTMLButtonElement | null>(null);
  const toolsBtnRef = useRef<HTMLButtonElement | null>(null);
  const [plusPos, setPlusPos] = useState<{ bottom: number; left: number } | null>(null);
  const [toolsPos, setToolsPos] = useState<{ bottom: number; left: number } | null>(null);

  // chat
  const [messages, setMessages] = useState<Msg[]>([
    {
      role: "assistant",
      text:
        "👋 Bonjour ! Je suis Dzir IA.\n\n" +
        "• Mode Chat : je réponds avec sources à partir de ta base.\n" +
        "• Mode Search : je retourne des chunks (RAG search).\n\n" +
        "Astuce : Upload TXT/PDF via le bouton +.\n" +
        "Astuce LLM : sélectionne Provider=Local + Model=llama3.2:3b pour Ollama.",
    },
  ]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);

  // search
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [searchBusy, setSearchBusy] = useState(false);

  // ui
  const listRef = useRef<HTMLDivElement | null>(null);
  const fileRef = useRef<HTMLInputElement | null>(null);
  const [toast, setToast] = useState<{ kind: "ok" | "err" | "info"; msg: string } | null>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [drawerSources, setDrawerSources] = useState<Source[]>([]);
  const [drawerTitle, setDrawerTitle] = useState("Sources");
  const [activeSourceIndex, setActiveSourceIndex] = useState<number | null>(null);

  function notify(msg: string, kind: "ok" | "err" | "info" = "info") {
    setToast({ kind, msg });
    window.clearTimeout((notify as any)._t);
    (notify as any)._t = window.setTimeout(() => setToast(null), 2200);
  }

  function openSources(sources: Source[], title = "Sources", focusIndex?: number) {
    setDrawerSources(sources);
    setDrawerTitle(title);
    setActiveSourceIndex(typeof focusIndex === "number" ? focusIndex : null);
    setDrawerOpen(true);
  }

  // load collections
  useEffect(() => {
    (async () => {
      try {
        const res = await collectionsApi.list();
        const cols = (res.collections ?? []).map((c: any) => ({ id: c.id, name: c.name }));
        setCollections(cols);
        if (!collectionId && cols[0]?.id) setCollectionId(cols[0].id);
      } catch {
        // non-blocking
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // scroll bottom
  useEffect(() => {
    listRef.current?.scrollTo({ behavior: "smooth", top: listRef.current.scrollHeight });
  }, [messages, mode, searchResults]);

  // close menus on outside click
  useEffect(() => {
    const onClick = (e: MouseEvent) => {
      const t = e.target as HTMLElement;
      if (!t.closest(".dziria-plus-container")) setPlusOpen(false);
      if (!t.closest(".dziria-tools-container")) setToolsOpen(false);
    };
    document.addEventListener("click", onClick);
    return () => document.removeEventListener("click", onClick);
  }, []);

  // when provider changes, force a sane model
  useEffect(() => {
    if (provider === "auto") {
      setModel("auto");
      return;
    }
    const presets = MODEL_PRESETS[provider];
    if (!presets?.length) {
      setModel("auto");
      return;
    }
    if (!presets.some((p) => p.value === model)) {
      setModel(presets[0].value);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [provider]);

  function togglePlus() {
    const btn = plusBtnRef.current;
    if (!btn) return;
    if (!plusOpen) {
      const r = btn.getBoundingClientRect();
      setPlusPos({ bottom: window.innerHeight - r.top + 8, left: r.left });
    }
    setPlusOpen((s) => !s);
    setToolsOpen(false);
  }

  function toggleTools() {
    const btn = toolsBtnRef.current;
    if (!btn) return;
    if (!toolsOpen) {
      const r = btn.getBoundingClientRect();
      setToolsPos({ bottom: window.innerHeight - r.top + 8, left: r.left });
    }
    setToolsOpen((s) => !s);
    setPlusOpen(false);
  }

  function buildSystemPrompt(): string | undefined {
    const parts: string[] = [];
    if (thinking) {
      parts.push("Mode réflexion: sois rigoureux, structure, étapes, hypothèses explicites.");
    }
    if (deepResearch) {
      parts.push("Mode deep research: propose un plan + questions minimales + sources/citations strictes.");
    }
    if (analysisTool) {
      parts.push("Mode analyse: privilégie tableaux, checklists, étapes, décisions; évite le blabla.");
    }
    if (!parts.length) return undefined;
    return parts.join("\n");
  }

  function buildAskPayload(query: string) {
    const sys = buildSystemPrompt();

    const payload: any = {
      collectionIds,
      query,
      ...(sys ? { systemPrompt: sys } : {}),
    };

    if (provider !== "auto") payload.provider = provider;
    if (model !== "auto") payload.model = model;

    return payload;
  }

  async function sendChat() {
    const q = input.trim();
    if (!q || busy) return;

    setInput("");
    setBusy(true);
    setMessages((m) => [...m, { role: "user", text: q }]);

    try {
      const payload = buildAskPayload(q);
      const res = await postJson<{
        answer: string;
        model?: string;
        sources?: any[];
      }>("/ask", payload);

      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          sources: (res.sources ?? []).map((s: any) => ({
            chunkId: s.chunkId,
            documentId: s.documentId,
            index: s.index,
            position: s.position,
            score: s.score,
            snippet: s.snippet,
            sourceUrl: s.sourceUrl,
            title: s.title,
          })),
          text: res.answer ?? "(réponse vide)",
        },
      ]);
    } catch (e: any) {
      setMessages((m) => [...m, { role: "assistant", text: `❌ ${String(e?.message ?? e)}` }]);
      notify(`Erreur: ${String(e?.message ?? e)}`, "err");
    } finally {
      setBusy(false);
    }
  }

  async function runSearch() {
    const q = input.trim();
    if (!q || searchBusy) return;

    setSearchBusy(true);
    setSearchResults([]);
    try {
      const res = await postJson<{ results: any[] }>("/search", {
        collectionIds,
        limit: 12,
        query: q,
        threshold: 0,
      });
      setSearchResults(res.results ?? []);
    } catch (e: any) {
      notify(`Search error: ${String(e?.message ?? e)}`, "err");
    } finally {
      setSearchBusy(false);
    }
  }

  function onEnter(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key !== "Enter") return;
    if (mode === "chat") sendChat();
    else runSearch();
  }

  async function captureTextNote() {
    const text = prompt("Colle un texte à capturer (min 50 caractères) :") ?? "";
    const content = text.trim();
    if (content.length < 50) return notify("Contenu trop court (min 50).", "err");
    if (!collectionId) return notify("Choisis une collection d’abord.", "err");

    try {
      const r = await captureApi.capture({
        collectionId,
        content,
        source: "manual",
        sourceType: "text",
        title: "Note",
      } as any);
      notify(
        r.vectorIndexed ? "Capturé + indexé ✅" : "Capturé (index KO)",
        r.vectorIndexed ? "ok" : "info"
      );
    } catch (e: any) {
      notify(`Capture error: ${String(e?.message ?? e)}`, "err");
    } finally {
      setPlusOpen(false);
    }
  }

  async function captureUrl() {
    const url = prompt("Colle une URL à capturer :") ?? "";
    const sourceUrl = url.trim();
    if (!sourceUrl) return;
    if (!collectionId) return notify("Choisis une collection d’abord.", "err");

    try {
      const r = await captureApi.capture({
        collectionId,
        content: "",
        source: "web",
        sourceType: "url",
        sourceUrl,
        title: "URL",
      } as any);
      notify(
        r.vectorIndexed ? "URL capturée + indexée ✅" : "URL capturée (index KO)",
        r.vectorIndexed ? "ok" : "info"
      );
    } catch (e: any) {
      notify(`URL error: ${String(e?.message ?? e)}`, "err");
    } finally {
      setPlusOpen(false);
    }
  }

  function openFilePicker() {
    fileRef.current?.click();
    setPlusOpen(false);
  }

  async function onFilePicked(file: File) {
    if (!collectionId) return notify("Choisis une collection d’abord.", "err");

    const name = file.name.toLowerCase();
    try {
      if (name.endsWith(".txt") || name.endsWith(".md")) {
        const content = (await fileToText(file)).trim();
        if (content.length < 50) return notify("Fichier trop court (min 50).", "err");

        const r = await captureApi.capture({
          collectionId,
          content,
          source: "file",
          sourceType: "text",
          title: file.name,
        } as any);

        notify(
          r.vectorIndexed ? "TXT capturé + indexé ✅" : "TXT capturé (index KO)",
          r.vectorIndexed ? "ok" : "info"
        );
        return;
      }

      if (name.endsWith(".pdf")) {
        const dataUrl = await fileToBase64DataUrl(file);
        const base64 = dataUrl.split(",")[1] ?? "";
        if (!base64) return notify("PDF illisible.", "err");

        const r = await captureApi.capture({
          collectionId,
          content: "",
          filename: file.name,
          pdfBase64: base64,
          source: "file",
          sourceType: "pdf",
          title: file.name,
        } as any);

        notify(
          r.vectorIndexed ? "PDF capturé + indexé ✅" : "PDF capturé (index KO)",
          r.vectorIndexed ? "ok" : "info"
        );
        return;
      }

      notify("Formats supportés: .txt/.md/.pdf", "info");
    } catch (e: any) {
      notify(`Upload error: ${String(e?.message ?? e)}`, "err");
    }
  }

  const modelOptions =
    provider === "auto"
      ? [{ label: "Model: Auto", value: "auto" }]
      : [
          { label: "Model: Auto", value: "auto" },
          ...MODEL_PRESETS[provider].map((m) => ({ label: m.label, value: m.value })),
        ];

  return (
    <div className={`dziria-shell ${drawerOpen ? "drawer-open" : ""}`}>
      {toast ? <div className={`dziria-toast ${toast.kind}`}>{toast.msg}</div> : null}

      <div className="dziria-messages" ref={listRef}>
        {mode === "chat" ? (
          <>
            {messages.map((m, i) => (
              <div className={`dziria-msg ${m.role === "user" ? "user" : "assistant"}`} key={i}>
                <div className="dziria-avatar">{m.role === "user" ? "👤" : "🟢"}</div>
                <div className="dziria-bubble">
                  <div className="dziria-text">{m.text}</div>

                  {"sources" in m && m.sources?.length ? (
                    <div className="dziria-citations">
                      <div className="dziria-citations-label">Citations</div>
                      <div className="dziria-citations-list">
                        {m.sources.map((s) => (
                          <button
                            className="dziria-citation-chip"
                            key={s.index}
                            onClick={() => openSources(m.sources ?? [], "Sources", s.index)}
                          >
                            [{s.index}] {s.title ?? "Source"}
                          </button>
                        ))}
                      </div>
                      <button
                        className="dziria-citations-open"
                        onClick={() => openSources(m.sources ?? [], "Sources")}
                      >
                        Voir toutes les sources
                      </button>
                    </div>
                  ) : null}
                </div>
              </div>
            ))}
          </>
        ) : (
          <>
            <div className="dziria-search-head">
              <div className="dziria-search-title">Résultats Search</div>
              <div className="dziria-search-sub">threshold=0 (toujours des résultats si indexé)</div>
            </div>

            {searchBusy ? (
              <div className="dziria-empty">⏳ Recherche…</div>
            ) : searchResults.length === 0 ? (
              <div className="dziria-empty">Aucun résultat.</div>
            ) : (
              <div className="dziria-results">
                {searchResults.map((r: any, idx: number) => (
                  <div className="dziria-result" key={idx}>
                    <div className="dziria-result-title">
                      {r.title ?? "Document"}{" "}
                      {typeof r.score === "number" ? (
                        <span className="dziria-result-score">{r.score.toFixed(3)}</span>
                      ) : null}
                    </div>
                    <div className="dziria-result-snippet">{r.snippet ?? ""}</div>
                    <div className="dziria-result-meta">
                      docId: {r.documentId} — chunkId: {r.chunkId}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </div>

      <div className="dziria-chatbox">
        <div className="dziria-headerbar">
          <div className="dziria-selects">
            <select className="dziria-select" onChange={(e) => setMode(e.target.value as Mode)} value={mode}>
              <option value="chat">💬 Chat</option>
              <option value="search">🔍 Search</option>
            </select>

            <select className="dziria-select" onChange={(e) => setCollectionId(e.target.value)} value={collectionId}>
              <option value="">All collections</option>
              {collections.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>

            <select className="dziria-select" onChange={(e) => setProvider(e.target.value as Provider)} value={provider}>
              <option value="auto">Provider: Auto</option>
              <option value="openai">Cloud: OpenAI</option>
              <option value="local">Local: Ollama</option>
            </select>

            <select className="dziria-select" onChange={(e) => setModel(e.target.value)} value={model}>
              {modelOptions.map((o) => (
                <option key={o.value} value={o.value}>
                  {o.label}
                </option>
              ))}
            </select>
          </div>

          <div className="dziria-flags">
            <button className={`dziria-flag ${thinking ? "on" : ""}`} onClick={() => setThinking((s) => !s)}>
              🧠 Thinking
            </button>
            <button className={`dziria-flag ${deepResearch ? "on" : ""}`} onClick={() => setDeepResearch((s) => !s)}>
              🔎 Deep
            </button>
            <button className={`dziria-flag ${analysisTool ? "on" : ""}`} onClick={() => setAnalysisTool((s) => !s)}>
              📊 Analyse
            </button>
          </div>
        </div>

        <div className="dziria-inputrow">
          <div className="dziria-plus-container">
            <button className="dziria-plus" onClick={togglePlus} ref={plusBtnRef} title="Menu">
              +
            </button>

            {plusOpen && plusPos ? (
              <div className="dziria-menu" style={{ bottom: plusPos.bottom, left: plusPos.left }}>
                <button className="dziria-menu-item" onClick={openFilePicker}>
                  📎 Joindre fichier (TXT/PDF)
                </button>
                <button className="dziria-menu-item" onClick={captureTextNote}>
                  📝 Capture note (text)
                </button>
                <button className="dziria-menu-item" onClick={captureUrl}>
                  🌐 Capture URL
                </button>
                <button className="dziria-menu-item" onClick={() => notify("Capture écran: bientôt", "info")}>
                  📸 Capture écran
                </button>
                <button className="dziria-menu-item" onClick={() => notify("Voice: bientôt", "info")}>
                  🎙️ Message vocal
                </button>
              </div>
            ) : null}

            <input
              accept=".txt,.md,.pdf"
              onChange={async (e) => {
                const f = e.target.files?.[0];
                if (f) await onFilePicked(f);
                e.currentTarget.value = "";
              }}
              ref={fileRef}
              style={{ display: "none" }}
              type="file"
            />
          </div>

          <div className="dziria-tools-container">
            <button className="dziria-tools" onClick={toggleTools} ref={toolsBtnRef} title="Recherche & outils">
              🧰
            </button>

            {toolsOpen && toolsPos ? (
              <div className="dziria-menu" style={{ bottom: toolsPos.bottom, left: toolsPos.left }}>
                <button className="dziria-menu-item" onClick={() => setAnalysisTool(true)}>
                  📊 Outil d’analyse
                </button>
                <button className="dziria-menu-item" onClick={() => notify("Artifact: bientôt", "info")}>
                  🧾 Créer artifact
                </button>
                <button className="dziria-menu-item" onClick={() => notify("Projet: bientôt", "info")}>
                  📁 Créer projet
                </button>
                <button className="dziria-menu-item" onClick={() => notify("Contexte: bientôt", "info")}>
                  📎 Ajouter contexte
                </button>
                <button className="dziria-menu-item" onClick={() => notify("Intégrations: bientôt", "info")}>
                  🔌 Intégrations
                </button>
              </div>
            ) : null}
          </div>

          <input
            className="dziria-input"
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={onEnter}
            placeholder={mode === "chat" ? "Pose ta question…" : "Tape ta recherche…"}
            value={input}
          />

          <button className="dziria-mic" onClick={() => notify("Micro: bientôt", "info")} title="Micro">
            🎙️
          </button>

          <button
            className="dziria-send"
            disabled={busy || searchBusy}
            onClick={() => (mode === "chat" ? sendChat() : runSearch())}
            title="Envoyer"
          >
            {busy || searchBusy ? "…" : "⬆"}
          </button>
        </div>
      </div>

      {drawerOpen && (
        <>
          <div className="dziria-drawer-overlay" onClick={() => setDrawerOpen(false)} />
          <aside className="dziria-drawer">
            <div className="dziria-drawer-header">
              <div>
                <div className="dziria-drawer-title">{drawerTitle}</div>
                <div className="dziria-drawer-sub">{drawerSources.length} sources</div>
              </div>
              <button className="dziria-drawer-close" onClick={() => setDrawerOpen(false)}>
                ✕
              </button>
            </div>

            <div className="dziria-drawer-list">
              {drawerSources.length === 0 ? (
                <div className="dziria-drawer-empty">Aucune source à afficher.</div>
              ) : (
                drawerSources.map((s) => (
                  <div
                    className={`dziria-drawer-item ${activeSourceIndex === s.index ? "active" : ""}`}
                    key={s.index}
                    onClick={() => setActiveSourceIndex(s.index)}
                  >
                    <div className="dziria-drawer-item-head">
                      <span className="dziria-drawer-index">[{s.index}]</span>
                      <span className="dziria-drawer-title-text">{s.title ?? "Source"}</span>
                      {typeof s.score === "number" ? (
                        <span className="dziria-drawer-score">{s.score.toFixed(3)}</span>
                      ) : null}
                    </div>
                    {s.snippet ? <div className="dziria-drawer-snippet">{s.snippet}</div> : null}
                    {s.sourceUrl ? (
                      <a className="dziria-drawer-link" href={s.sourceUrl} target="_blank" rel="noreferrer">
                        Ouvrir la source
                      </a>
                    ) : null}
                  </div>
                ))
              )}
            </div>
          </aside>
        </>
      )}
    </div>
  );
}
