/**
 * Translation Widget - React Component
 * iafactory AI Tools Frontend
 */

import React, { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001/api/v1';

interface TranslationResult {
  success: boolean;
  translated_text: string;
  source_language: string;
  target_language: string;
  character_count: number;
  provider: string;
}

const languages = [
  { code: 'fr', name: 'Français', flag: '🇫🇷' },
  { code: 'ar', name: 'العربية', flag: '🇩🇿' },
  { code: 'en', name: 'English', flag: '🇬🇧' },
  { code: 'es', name: 'Español', flag: '🇪🇸' },
  { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
  { code: 'it', name: 'Italiano', flag: '🇮🇹' },
];

export const TranslatorWidget: React.FC = () => {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [sourceLang, setSourceLang] = useState('fr');
  const [targetLang, setTargetLang] = useState('ar');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [charCount, setCharCount] = useState(0);

  const handleTranslate = async () => {
    if (!inputText.trim()) {
      setError('Veuillez entrer du texte à traduire');
      return;
    }

    if (sourceLang === targetLang) {
      setError('Les langues source et cible doivent être différentes');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post<TranslationResult>(
        `${API_BASE_URL}/translator/translate`,
        {
          text: inputText,
          source_language: sourceLang,
          target_language: targetLang,
          preserve_formatting: true,
          tenant_id: 'rag-dz', // ou 'helvetia' selon le contexte
        }
      );

      if (response.data.success) {
        setOutputText(response.data.translated_text);
        setCharCount(response.data.character_count);
      } else {
        setError('Erreur lors de la traduction');
      }
    } catch (err: any) {
      setError(err.response?.data?.message || 'Erreur de connexion à l\'API');
      console.error('Translation error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSwapLanguages = () => {
    const temp = sourceLang;
    setSourceLang(targetLang);
    setTargetLang(temp);
    setInputText(outputText);
    setOutputText(inputText);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(outputText);
    alert('Texte copié !');
  };

  return (
    <div className="translator-widget max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-center text-gray-800">
        🌐 Traducteur Multilingue
      </h2>

      {/* Language Selection */}
      <div className="flex items-center justify-between mb-4 gap-4">
        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Langue source
          </label>
          <select
            value={sourceLang}
            onChange={(e) => setSourceLang(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {languages.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.flag} {lang.name}
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={handleSwapLanguages}
          className="mt-7 p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition"
          title="Inverser les langues"
        >
          ⇄
        </button>

        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Langue cible
          </label>
          <select
            value={targetLang}
            onChange={(e) => setTargetLang(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {languages.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.flag} {lang.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Text Areas */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Texte à traduire
          </label>
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Entrez votre texte ici..."
            className="w-full h-48 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            dir={sourceLang === 'ar' ? 'rtl' : 'ltr'}
          />
          <div className="text-sm text-gray-500 mt-1">
            {inputText.length} caractères
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Traduction
          </label>
          <textarea
            value={outputText}
            readOnly
            placeholder="La traduction apparaîtra ici..."
            className="w-full h-48 px-4 py-2 border border-gray-300 rounded-lg bg-gray-50 resize-none"
            dir={targetLang === 'ar' ? 'rtl' : 'ltr'}
          />
          <div className="text-sm text-gray-500 mt-1">
            {charCount > 0 && `${charCount} caractères traduits`}
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700">
          ⚠️ {error}
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex gap-3">
        <button
          onClick={handleTranslate}
          disabled={isLoading || !inputText.trim()}
          className={`flex-1 px-6 py-3 rounded-lg font-medium transition ${
            isLoading || !inputText.trim()
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }`}
        >
          {isLoading ? (
            <>
              <span className="inline-block animate-spin mr-2">⏳</span>
              Traduction en cours...
            </>
          ) : (
            '🚀 Traduire'
          )}
        </button>

        <button
          onClick={handleCopy}
          disabled={!outputText}
          className={`px-6 py-3 rounded-lg font-medium transition ${
            !outputText
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-green-600 text-white hover:bg-green-700'
          }`}
        >
          📋 Copier
        </button>
      </div>

      {/* Info Footer */}
      <div className="mt-6 pt-4 border-t border-gray-200 text-sm text-gray-600 text-center">
        Propulsé par iafactory AI Tools • OpenAI GPT-4o-mini
      </div>
    </div>
  );
};

export default TranslatorWidget;
