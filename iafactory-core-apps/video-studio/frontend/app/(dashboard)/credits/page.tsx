"use client";

import { useState, useEffect, Suspense } from "react";
import { motion } from "framer-motion";
import { Sparkles, Zap, Crown, Check, TrendingUp, Loader2, CheckCircle, XCircle } from "lucide-react";
import { useLocaleStore, useThemeStore } from "@/lib/store";
import { t, isRTL } from "@/lib/i18n";
import { useSearchParams } from "next/navigation";

interface CreditPack {
  id: string;
  name: Record<string, string>;
  credits: number;
  price: number;
  popular?: boolean;
  features: Record<string, string[]>;
}

const creditPacks: CreditPack[] = [
  {
    id: "starter",
    name: { fr: "Starter", ar: "المبتدئ", en: "Starter" },
    credits: 50,
    price: 990,
    features: {
      fr: ["50 crédits (~5 vidéos)", "Text-to-Video basique", "Image-to-Video basique", "Export 720p"],
      ar: ["50 رصيد (~5 فيديوهات)", "نص إلى فيديو أساسي", "صورة إلى فيديو أساسي", "تصدير 720p"],
      en: ["50 credits (~5 videos)", "Basic Text-to-Video", "Basic Image-to-Video", "720p Export"]
    },
  },
  {
    id: "pro",
    name: { fr: "Pro", ar: "احترافي", en: "Pro" },
    credits: 200,
    price: 2990,
    popular: true,
    features: {
      fr: ["200 crédits (~20 vidéos)", "Tous les modèles IA", "Voix Darija incluse", "Export 1080p", "Support prioritaire"],
      ar: ["200 رصيد (~20 فيديو)", "جميع نماذج الذكاء الاصطناعي", "صوت الدارجة مضمن", "تصدير 1080p", "دعم ذو أولوية"],
      en: ["200 credits (~20 videos)", "All AI models", "Darija voice included", "1080p Export", "Priority support"]
    },
  },
  {
    id: "business",
    name: { fr: "Business", ar: "أعمال", en: "Business" },
    credits: 500,
    price: 5990,
    features: {
      fr: ["500 crédits (~50 vidéos)", "Accès API illimité", "Voix personnalisée", "Export 4K", "Account Manager dédié", "Facturation entreprise"],
      ar: ["500 رصيد (~50 فيديو)", "وصول API غير محدود", "صوت مخصص", "تصدير 4K", "مدير حساب مخصص", "فواتير الشركات"],
      en: ["500 credits (~50 videos)", "Unlimited API access", "Custom voice", "4K Export", "Dedicated Account Manager", "Enterprise billing"]
    },
  },
];

const usageHistory = [
  { date: "2024-12-19", type: { fr: "Génération vidéo", ar: "إنشاء فيديو", en: "Video generation" }, credits: -10, description: { fr: "Promo Ramadan 2025", ar: "إعلان رمضان 2025", en: "Ramadan 2025 Promo" } },
  { date: "2024-12-18", type: { fr: "Voix-off", ar: "تعليق صوتي", en: "Voice-over" }, credits: -5, description: { fr: "Narration Darija", ar: "سرد بالدارجة", en: "Darija Narration" } },
  { date: "2024-12-18", type: { fr: "Achat", ar: "شراء", en: "Purchase" }, credits: 200, description: { fr: "Pack Pro", ar: "باقة احترافية", en: "Pro Pack" } },
  { date: "2024-12-17", type: { fr: "Génération vidéo", ar: "إنشاء فيديو", en: "Video generation" }, credits: -15, description: { fr: "Story Instagram", ar: "ستوري انستغرام", en: "Instagram Story" } },
];

// Component that uses searchParams - wrapped in Suspense
function CreditsContent() {
  const { locale } = useLocaleStore();
  const { theme } = useThemeStore();
  const rtl = isRTL(locale);
  const searchParams = useSearchParams();
  const [loadingPack, setLoadingPack] = useState<string | null>(null);
  const [balance, setBalance] = useState(150);
  
  // Check for Stripe redirect results
  const success = searchParams.get('success');
  const canceled = searchParams.get('canceled');
  
  useEffect(() => {
    if (success) {
      // Refresh balance after successful purchase
      setBalance(prev => prev + 200); // Demo: add Pro pack credits
    }
  }, [success]);
  
  const handlePurchase = async (packId: string) => {
    setLoadingPack(packId);
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'https://video-studio.iafactory.ch/api'}/v1/credits/purchase`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pack_id: packId }),
      });
      
      const data = await response.json();
      
      if (data.checkout_url) {
        // Redirect to Stripe Checkout
        window.location.href = data.checkout_url;
      } else if (data.success) {
        // Demo mode: credits added directly
        setBalance(data.new_balance);
        alert(data.message);
      }
    } catch (error) {
      console.error('Purchase error:', error);
      alert(locale === 'ar' ? 'خطأ في الشراء' : locale === 'en' ? 'Purchase error' : 'Erreur lors de l\'achat');
    } finally {
      setLoadingPack(null);
    }
  };
  
  const labels = {
    currentBalance: { fr: 'Solde actuel', ar: 'الرصيد الحالي', en: 'Current balance' },
    credits: { fr: 'crédits', ar: 'رصيد', en: 'credits' },
    videosRemaining: { fr: 'vidéos restantes', ar: 'فيديوهات متبقية', en: 'videos remaining' },
    buyCredits: { fr: 'Acheter des crédits', ar: 'شراء أرصدة', en: 'Buy credits' },
    popular: { fr: 'Populaire', ar: 'الأكثر شعبية', en: 'Popular' },
    buy: { fr: 'Acheter', ar: 'شراء', en: 'Buy' },
    buying: { fr: 'Achat en cours...', ar: 'جاري الشراء...', en: 'Processing...' },
    history: { fr: "Historique d'utilisation", ar: 'سجل الاستخدام', en: 'Usage history' },
    date: { fr: 'Date', ar: 'التاريخ', en: 'Date' },
    type: { fr: 'Type', ar: 'النوع', en: 'Type' },
    description: { fr: 'Description', ar: 'الوصف', en: 'Description' },
  };
  
  return (
    <div className={`min-h-screen p-8 ${theme === 'dark' ? 'bg-[#0a0a0f] text-white' : 'bg-gray-50 text-gray-900'}`} dir={rtl ? 'rtl' : 'ltr'}>
      <div className="max-w-6xl mx-auto">
        {/* Success/Cancel Messages */}
        {success && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 p-4 rounded-xl bg-green-500/20 border border-green-500/50 flex items-center gap-3"
          >
            <CheckCircle className="w-6 h-6 text-green-500" />
            <span className="text-green-400">
              {locale === 'ar' ? 'تم الشراء بنجاح! تمت إضافة الأرصدة إلى حسابك.' : 
               locale === 'en' ? 'Purchase successful! Credits have been added to your account.' : 
               'Achat réussi ! Les crédits ont été ajoutés à votre compte.'}
            </span>
          </motion.div>
        )}
        
        {canceled && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-6 p-4 rounded-xl bg-yellow-500/20 border border-yellow-500/50 flex items-center gap-3"
          >
            <XCircle className="w-6 h-6 text-yellow-500" />
            <span className="text-yellow-400">
              {locale === 'ar' ? 'تم إلغاء الشراء.' : 
               locale === 'en' ? 'Purchase was canceled.' : 
               'L\'achat a été annulé.'}
            </span>
          </motion.div>
        )}
        
        {/* Header */}
        <div className="mb-8">
          <h1 className={`text-3xl font-bold mb-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
            {t("nav.credits", locale)}
          </h1>
          <p className={theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}>
            {locale === 'ar' ? 'إدارة رصيدك وشراء أرصدة' : 
             locale === 'en' ? 'Manage your balance and purchase credits' : 
             'Gérez votre solde et achetez des crédits'}
          </p>
        </div>

        {/* Current balance */}
        <div className={`rounded-2xl p-8 mb-8 border ${
          theme === 'dark' 
            ? 'bg-gradient-to-br from-cyan-500/10 via-[#12121a] to-fuchsia-500/10 border-[#2a2a35]' 
            : 'bg-gradient-to-br from-cyan-50 via-white to-fuchsia-50 border-gray-200'
        }`}>
          <div className="flex items-center justify-between">
            <div>
              <p className={theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}>
                {labels.currentBalance[locale]}
              </p>
              <div className="flex items-baseline gap-2">
                <span className={`text-5xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>{balance}</span>
                <span className={`text-xl ${theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}`}>
                  {labels.credits[locale]}
                </span>
              </div>
              <p className={`text-sm mt-2 ${theme === 'dark' ? 'text-gray-500' : 'text-gray-500'}`}>
                ≈ {Math.floor(balance / 10)} {labels.videosRemaining[locale]}
              </p>
            </div>
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-cyan-400/20 to-fuchsia-500/20 flex items-center justify-center">
              <Sparkles className="w-12 h-12 text-cyan-400" />
            </div>
          </div>
        </div>

        {/* Credit packs */}
        <div className="mb-12">
          <h2 className={`text-xl font-semibold mb-6 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
            {labels.buyCredits[locale]}
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            {creditPacks.map((pack, index) => (
              <motion.div
                key={pack.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`relative rounded-2xl p-6 border-2 ${
                  pack.popular
                    ? "border-cyan-400 ring-2 ring-cyan-400/20"
                    : theme === 'dark' 
                      ? "bg-[#141419] border-[#2a2a35] hover:border-cyan-400/50" 
                      : "bg-white border-gray-200 hover:border-cyan-500/50"
                } transition-colors`}
              >
                {pack.popular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 flex items-center gap-1 px-3 py-1 bg-gradient-to-r from-cyan-400 to-fuchsia-500 rounded-full text-white">
                    <Crown className="w-4 h-4" />
                    <span className="text-sm font-medium">{labels.popular[locale]}</span>
                  </div>
                )}

                <div className="mb-6">
                  <div className="flex items-center gap-2 mb-2">
                    {pack.id === "starter" && <Zap className="w-5 h-5 text-yellow-500" />}
                    {pack.id === "pro" && <Sparkles className="w-5 h-5 text-cyan-400" />}
                    {pack.id === "business" && <Crown className="w-5 h-5 text-fuchsia-400" />}
                    <h3 className={`text-lg font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                      {pack.name[locale]}
                    </h3>
                  </div>
                  <div className="flex items-baseline gap-1">
                    <span className={`text-3xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                      {pack.price}
                    </span>
                    <span className={theme === 'dark' ? 'text-gray-400' : 'text-gray-600'}>DA</span>
                  </div>
                  <p className={`text-sm mt-1 ${theme === 'dark' ? 'text-gray-500' : 'text-gray-500'}`}>
                    {pack.credits} {labels.credits[locale]}
                  </p>
                </div>

                <ul className="space-y-3 mb-6">
                  {pack.features[locale].map((feature, i) => (
                    <li key={i} className={`flex items-center gap-2 text-sm ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>
                      <Check className="w-4 h-4 text-green-500 shrink-0" />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>

                <button
                  onClick={() => handlePurchase(pack.id)}
                  disabled={loadingPack !== null}
                  className={`w-full py-3 rounded-xl font-semibold transition-all flex items-center justify-center gap-2 ${
                    pack.popular
                      ? "bg-gradient-to-r from-cyan-400 to-fuchsia-500 text-white hover:shadow-lg hover:shadow-cyan-500/30"
                      : theme === 'dark' 
                        ? "bg-[#1a1a24] border border-[#2a2a35] hover:border-cyan-400 text-white" 
                        : "bg-gray-100 border border-gray-200 hover:border-cyan-500 text-gray-900"
                  } disabled:opacity-50 disabled:cursor-not-allowed`}
                >
                  {loadingPack === pack.id ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      {labels.buying[locale]}
                    </>
                  ) : (
                    labels.buy[locale]
                  )}
                </button>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Usage history */}
        <div>
          <h2 className={`text-xl font-semibold mb-6 flex items-center gap-2 ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
            <TrendingUp className="w-5 h-5 text-cyan-400" />
            {labels.history[locale]}
          </h2>
          <div className={`rounded-xl overflow-hidden border ${
            theme === 'dark' ? 'bg-[#141419] border-[#2a2a35]' : 'bg-white border-gray-200'
          }`}>
            <table className="w-full">
              <thead>
                <tr className={`border-b ${theme === 'dark' ? 'border-[#2a2a35]' : 'border-gray-200'}`}>
                  <th className={`text-${rtl ? 'right' : 'left'} text-sm font-medium px-6 py-4 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
                    {labels.date[locale]}
                  </th>
                  <th className={`text-${rtl ? 'right' : 'left'} text-sm font-medium px-6 py-4 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
                    {labels.type[locale]}
                  </th>
                  <th className={`text-${rtl ? 'right' : 'left'} text-sm font-medium px-6 py-4 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
                    {labels.description[locale]}
                  </th>
                  <th className={`text-${rtl ? 'left' : 'right'} text-sm font-medium px-6 py-4 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
                    {labels.credits[locale]}
                  </th>
                </tr>
              </thead>
              <tbody>
                {usageHistory.map((item, index) => (
                  <tr key={index} className={`border-b last:border-0 ${theme === 'dark' ? 'border-[#2a2a35]' : 'border-gray-100'}`}>
                    <td className={`px-6 py-4 text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
                      {new Date(item.date).toLocaleDateString(locale === 'ar' ? 'ar-DZ' : locale === 'en' ? 'en-US' : 'fr-FR')}
                    </td>
                    <td className={`px-6 py-4 text-sm ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                      {item.type[locale]}
                    </td>
                    <td className={`px-6 py-4 text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>
                      {item.description[locale]}
                    </td>
                    <td className={`px-6 py-4 text-sm text-${rtl ? 'left' : 'right'} font-medium ${
                      item.credits > 0 ? "text-green-500" : "text-red-500"
                    }`}>
                      {item.credits > 0 ? "+" : ""}{item.credits}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

// Main export with Suspense wrapper for useSearchParams
export default function CreditsPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-cyan-400" />
      </div>
    }>
      <CreditsContent />
    </Suspense>
  );
}
