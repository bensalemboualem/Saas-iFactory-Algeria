// D:\iafactorychatgpt\dzir-ia\backend\src\services\llm\openai_compat.ts
export type ChatMsg = { content: string, role: "system" | "user" | "assistant"; };

function joinUrl(base: string, path: string) {
    const b = base.endsWith("/") ? base.slice(0, -1) : base;
    const p = path.startsWith("/") ? path : `/${path}`;
    return `${b}${p}`;
}

export async function chatOpenAICompat(opts: {
    apiKey?: string;
    baseUrl: string;
    extraHeaders?: Record<string, string>;
    maxTokens?: number;
    messages: ChatMsg[];
    // optional (local llm)
    model: string;
    temperature?: number;
}) {
    const {
        baseUrl,
        apiKey,
        model,
        messages,
        temperature = 0.2,
        maxTokens = 800,
        extraHeaders = {},
    } = opts;

    const url = joinUrl(baseUrl, "/chat/completions");

    const body: any = {
        max_tokens: maxTokens,
        messages,
        model,
        temperature,
    };

    // ✅ IMPORTANT: do NOT send Authorization header if apiKey is empty (Ollama/local)
    const headers: Record<string, string> = {
        "content-type": "application/json",
        ...extraHeaders,
    };

    if (apiKey && apiKey.trim().length > 0) {
        headers.authorization = `Bearer ${apiKey.trim()}`;
    }

    const res = await fetch(url, {
        body: JSON.stringify(body),
        headers,
        method: "POST",
    });

    if (!res.ok) {
        const text = await res.text().catch(() => "");
        throw new Error(`LLM ${res.status}: ${text}`);
    }

    const data: any = await res.json();
    const content = data?.choices?.[0]?.message?.content ?? "";
    return { raw: data, text: content };
}
