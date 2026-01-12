import { availableLangs, getLang, setLang } from './i18n';

export function LangToggle() {
  return (
    <select
      className="px-3 py-2 rounded-lg bg-[var(--bg)] border border-[var(--border)] text-sm focus:outline-none focus:border-green-500 cursor-pointer"
      value={getLang()}
      onChange={e => setLang(e.target.value as 'fr' | 'en' | 'ar')}
      aria-label="Select language"
    >
      {availableLangs.map(l => (
        <option key={l.code} value={l.code}>{l.label}</option>
      ))}
    </select>
  );
}
