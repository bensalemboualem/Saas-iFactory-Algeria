import type { ChatMsg } from "./openai_compat.js";

export async function chatGemini(opts: {
    apiKey: string;
    // ex: "gemini-2.0-flash"
    messages: ChatMsg[];
    model: string;
}) {
    const { apiKey, model, messages } = opts;

    // systemInstruction (Gemini)
    const systemText = messages.filter(m => m.role === "system").map(m => m.content).join("\n").trim();
    const contents = messages
        .filter(m => m.role !== "system")
        .map(m => ({
            parts: [{ text: m.content }],
            role: m.role === "assistant" ? "model" : "user",
        }));

    const url = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(
        model
    )}:generateContent?key=${encodeURIComponent(apiKey)}`;

    const body: any = { contents };
    if (systemText) {
        body.systemInstruction = { parts: [{ text: systemText }] };
    }

    const res = await fetch(url, {
        body: JSON.stringify(body),
        headers: { "content-type": "application/json" },
        method: "POST",
    });

    if (!res.ok) {
        const text = await res.text().catch(() => "");
        throw new Error(`Gemini ${res.status}: ${text}`);
    }

    const data: any = await res.json();
    const text =
        data?.candidates?.[0]?.content?.parts?.map((p: any) => p.text).filter(Boolean).join("") ?? "";
    return { raw: data, text };
}
