import { useEffect, useState } from 'react';

export default function PreviewIframe({ sandboxId }: { sandboxId?: string }) {
  const [status, setStatus] = useState<'idle'|'starting'|'running'|'error'>('idle');
  const [url, setUrl] = useState<string | null>(null);
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    let mounted = true;
    async function start() {
      setStatus('starting');
      try {
        const startRes = await fetch(`/api/preview?provider=e2b${sandboxId ? `&sandboxId=${sandboxId}` : ''}`, { method: 'POST' });
        const startJson = await startRes.json();
        setLogs((l) => [...l, `start: ${JSON.stringify(startJson)}`]);

        // Poll for status/url
        for (let i = 0; i < 20 && mounted; i++) {
          const res = await fetch(`/api/preview?provider=e2b${sandboxId ? `&sandboxId=${sandboxId}` : ''}`);
          const j = await res.json();
          setLogs((l) => [...l, `status: ${JSON.stringify(j)}`]);
          if (j?.url) {
            setUrl(j.url);
            setStatus('running');
            return;
          }
          await new Promise((r) => setTimeout(r, 400));
        }

        if (mounted && !url) {
          setStatus('error');
          setLogs((l) => [...l, 'timed out waiting for preview URL']);
        }
      } catch (err: any) {
        setStatus('error');
        setLogs((l) => [...l, `error: ${err?.message || err}`]);
      }
    }

    start();
    return () => { mounted = false; };
  }, [sandboxId]);

  if (status === 'starting' || status === 'idle') {
    return (
      <div style={{display: 'flex', gap: 12}}>
        <div style={{flex: 1}}>
          <h3>Preview (E2B prototype)</h3>
          <div style={{padding: 12, border: '1px solid #ddd', minHeight: 200}}>
            <strong>Starting preview…</strong>
            <div style={{marginTop:8}}>
              {logs.map((l, i) => <div key={i}><code>{l}</code></div>)}
            </div>
          </div>
        </div>
        <div style={{width: 360}}>
          <h4>Logs</h4>
          <div style={{padding: 12, border: '1px solid #eee', height: 200, overflow: 'auto'}}>
            {logs.map((l, i) => <div key={i}><code>{l}</code></div>)}
          </div>
        </div>
      </div>
    );
  }

  if (status === 'error') {
    return <div>Preview failed to start — check logs above.</div>;
  }

  return (
    <iframe
      title="Bolt E2B preview"
      src={url || undefined}
      style={{width: '100%', height: '720px', border: '1px solid #e6e6e6'}}
      sandbox="allow-scripts allow-same-origin"
    />
  );
}
