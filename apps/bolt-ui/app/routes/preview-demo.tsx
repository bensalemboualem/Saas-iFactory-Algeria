import PreviewIframe from '~/app/components/PreviewIframe';

export default function PreviewDemo() {
  return (
    <div style={{padding: 20}}>
      <h2>Bolt — E2B preview (prototype)</h2>
      <p>This demo starts a sandboxed preview (prototype). Use only in dev.</p>
      <PreviewIframe />
    </div>
  );
}
