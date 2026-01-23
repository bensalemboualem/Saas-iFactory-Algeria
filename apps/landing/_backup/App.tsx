import Header from './components/Header';
import { legacyBody, legacyScripts } from './legacy';
import './legacy.css';
import { useEffect } from 'react';

// Retirer le header du legacy HTML (il est remplacé par le composant React)
function removeHeaderFromLegacy(html: string): string {
  // Retire tout de <!-- Header --> jusqu'à </header> inclus
  // Support pour HTML normal ET HTML échappé (Unicode: \u003c = <, \u003e = >)
  let result = html;

  // Pattern pour HTML normal
  result = result.replace(/<!--\s*Header\s*-->[\s\S]*?<\/header>/gi, '');

  // Pattern pour HTML échappé Unicode (\u003c = <, \u003e = >)
  result = result.replace(/\\u003c!--\s*Header\s*--\\u003e[\s\S]*?\\u003c\/header\\u003e/gi, '');

  return result;
}

export default function App() {
  const cleanedLegacyBody = removeHeaderFromLegacy(legacyBody);

  useEffect(() => {
    // Exécuter les scripts legacy après le rendu
    legacyScripts.forEach((script: { inline?: string; src?: string }) => {
      if (script.inline) {
        try {
          const fn = new Function(script.inline);
          fn();
        } catch (e) {
          console.error('Legacy script error:', e);
        }
      } else if (script.src) {
        const scriptEl = document.createElement('script');
        scriptEl.src = script.src;
        document.body.append(scriptEl);
      }
    });
  }, []);

  return (
    <>
      <Header />
      <div 
        dangerouslySetInnerHTML={{ __html: cleanedLegacyBody }} 
        id="legacy-content" 
        style={{ paddingTop: '110px' }}
      />
    </>
  );
}
