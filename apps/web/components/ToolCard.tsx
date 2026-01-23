import Link from 'next/link';

interface Tool {
  id: string;
  slug: string;
  name: { fr: string; ar: string; en: string };
  description: { fr: string; ar: string; en: string };
  category: string;
  credits: number;
  isAlgeriaExclusive?: boolean;
}

interface ToolCardProps {
  tool: Tool;
  lang?: 'fr' | 'ar' | 'en';
}

const categoryIcons: Record<string, string> = {
  blog: '📝',
  seo: '🔍',
  social: '📱',
  youtube: '🎬',
  email: '📧',
  ecommerce: '🛒',
  'admin-dz': '🏛️',
  'education-dz': '🎓',
  'finance-dz': '💰',
  'compliance-dz': '📋',
};

export default function ToolCard({ tool, lang = 'fr' }: ToolCardProps) {
  const icon = categoryIcons[tool.category] || '⚡';

  return (
    <Link
      href={`/tools/${tool.category}/${tool.slug}`}
      className="bg-white rounded-xl p-5 shadow-sm hover:shadow-md transition group relative block"
    >
      {tool.isAlgeriaExclusive && (
        <div className="absolute top-3 right-3 bg-red-500 text-white text-xs px-2 py-0.5 rounded flex items-center gap-1">
          <span>🇩🇿</span>
          <span>Exclusif</span>
        </div>
      )}

      <div className="text-3xl mb-3">{icon}</div>

      <h3 className="font-semibold text-gray-900 mb-2 group-hover:text-green-600 transition">
        {tool.name[lang]}
      </h3>

      <p className="text-sm text-gray-500 mb-3 line-clamp-2">
        {tool.description[lang]}
      </p>

      <div className="flex items-center justify-between text-sm">
        <span className="text-gray-400 capitalize">
          {tool.category.replace('-dz', ' DZ').replace('-', ' ')}
        </span>
        <span className="text-green-600 font-medium">{tool.credits} crédits</span>
      </div>
    </Link>
  );
}
