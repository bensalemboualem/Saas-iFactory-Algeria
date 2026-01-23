import type { ChatMsg } from "./openai_compat.js";

export async function chatAnthropic(opts: {
    apiKey: string;
    maxTokens?: number;
    messages: ChatMsg[];
    model: string;
}) {
    const { apiKey, model, messages, maxTokens = 800 } = opts;

    // Anthropic sépare "system" du reste
    const system = messages.filter(m => m.role === "system").map(m => m.content).join("\n").trim() || undefined;
    const msgs = messages
        .filter(m => m.role !== "system")
        .map(m => ({ content: m.content, role: m.role }));

    const res = await fetch("https://api.anthropic.com/v1/messages", {
        body: JSON.stringify({
            max_tokens: maxTokens,
            messages: msgs,
            model,
            system,
        }),
        headers: {
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
            "x-api-key": apiKey,
        },
        method: "POST",
    });

    if (!res.ok) {
        const text = await res.text().catch(() => "");
        throw new Error(`Claude ${res.status}: ${text}`);
    }

    const data: any = await res.json();
    const text = data?.content?.[0]?.text ?? "";
    return { raw: data, text };
}
