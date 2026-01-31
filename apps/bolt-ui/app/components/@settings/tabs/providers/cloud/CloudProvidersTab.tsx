/**
 * IAFactory Cloud Providers Tab
 *
 * SECURITY: Only IAFactory is available as cloud provider.
 * All cloud AI calls go through IAFactory Gateway for:
 * - Billing/credits management
 * - Rate limiting
 * - Usage tracking
 *
 * Direct provider access (OpenAI, Anthropic, etc.) is DISABLED.
 */

import React, { useEffect, useState, useCallback } from 'react';
import { Switch } from '~/components/ui/Switch';
import { useSettings } from '~/lib/hooks/useSettings';
import { logStore } from '~/lib/stores/logs';
import { motion } from 'framer-motion';
import { classNames } from '~/utils/classNames';
import { toast } from 'react-toastify';
import { TbCloudComputing } from 'react-icons/tb';
import { FaIndustry } from 'react-icons/fa';
import Cookies from 'js-cookie';

const IAFACTORY_API_KEY_LINK = 'https://iafactory.dz/dashboard/api-keys';
const IAFACTORY_GATEWAY_URL = 'http://localhost:5191/v1';

const CloudProvidersTab = () => {
  const settings = useSettings();
  const [isEnabled, setIsEnabled] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [isEditingKey, setIsEditingKey] = useState(false);
  const [tempKey, setTempKey] = useState('');

  // Load IAFactory provider settings
  useEffect(() => {
    const iaFactorySettings = settings.providers?.['IAFactory']?.settings;
    setIsEnabled(iaFactorySettings?.enabled ?? false);

    // Load API key from cookies
    const storedKeys = Cookies.get('apiKeys');
    if (storedKeys) {
      try {
        const parsed = JSON.parse(storedKeys);
        setApiKey(parsed['IAFactory'] || '');
        setTempKey(parsed['IAFactory'] || '');
      } catch {
        // Ignore parse errors
      }
    }
  }, [settings.providers]);

  const handleToggleProvider = useCallback(
    (enabled: boolean) => {
      const currentSettings = settings.providers?.['IAFactory']?.settings || {};
      settings.updateProviderSettings('IAFactory', { ...currentSettings, enabled });

      setIsEnabled(enabled);

      if (enabled) {
        logStore.logProvider('IAFactory provider enabled', { provider: 'IAFactory' });
        toast.success('IAFactory enabled');
      } else {
        logStore.logProvider('IAFactory provider disabled', { provider: 'IAFactory' });
        toast.success('IAFactory disabled');
      }
    },
    [settings],
  );

  const handleSaveApiKey = useCallback(() => {
    // Save to cookies
    const currentKeys = Cookies.get('apiKeys');
    let parsedKeys: Record<string, string> = {};
    if (currentKeys) {
      try {
        parsedKeys = JSON.parse(currentKeys);
      } catch {
        // Ignore parse errors
      }
    }
    parsedKeys['IAFactory'] = tempKey;
    Cookies.set('apiKeys', JSON.stringify(parsedKeys));

    setApiKey(tempKey);
    setIsEditingKey(false);
    toast.success('IAFactory API key saved');
  }, [tempKey]);

  return (
    <div className="space-y-6">
      <motion.div
        className="space-y-4"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex items-center justify-between gap-4 mt-8 mb-4">
          <div className="flex items-center gap-2">
            <div
              className={classNames(
                'w-8 h-8 flex items-center justify-center rounded-lg',
                'bg-bolt-elements-background-depth-3',
                'text-purple-500',
              )}
            >
              <TbCloudComputing className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-md font-medium text-bolt-elements-textPrimary">Cloud Provider</h4>
              <p className="text-sm text-bolt-elements-textSecondary">
                Connect to IAFactory Gateway for cloud AI models
              </p>
            </div>
          </div>
        </div>

        {/* IAFactory Provider Card */}
        <motion.div
          className={classNames(
            'rounded-lg border bg-bolt-elements-background text-bolt-elements-textPrimary shadow-sm',
            'bg-bolt-elements-background-depth-2',
            'hover:bg-bolt-elements-background-depth-3',
            'transition-all duration-200',
            'relative overflow-hidden group',
            'flex flex-col',
          )}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          whileHover={{ scale: 1.02 }}
        >
          <div className="flex items-start gap-4 p-4">
            <motion.div
              className={classNames(
                'w-12 h-12 flex items-center justify-center rounded-xl',
                'bg-gradient-to-br from-purple-500/20 to-blue-500/20',
                'transition-all duration-200',
                isEnabled ? 'text-purple-500' : 'text-bolt-elements-textSecondary',
              )}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
            >
              <FaIndustry className="w-6 h-6" />
            </motion.div>

            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-4 mb-2">
                <div>
                  <h4 className="text-lg font-semibold text-bolt-elements-textPrimary group-hover:text-purple-500 transition-colors">
                    IAFactory
                  </h4>
                  <p className="text-sm text-bolt-elements-textSecondary mt-1">
                    Access GPT-4, Claude, Llama, DeepSeek and more via IAFactory Gateway
                  </p>
                </div>
                <Switch checked={isEnabled} onCheckedChange={handleToggleProvider} />
              </div>

              {/* Available Models Info */}
              <div className="mt-3 flex flex-wrap gap-2">
                <span className="px-2 py-1 text-xs rounded-full bg-green-500/10 text-green-500">Fast (Groq)</span>
                <span className="px-2 py-1 text-xs rounded-full bg-blue-500/10 text-blue-500">Smart (OpenRouter)</span>
                <span className="px-2 py-1 text-xs rounded-full bg-orange-500/10 text-orange-500">Cheap (DeepSeek)</span>
              </div>

              {/* API Key Section */}
              {isEnabled && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.2 }}
                  className="mt-4 pt-4 border-t border-bolt-elements-borderColor"
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-bolt-elements-textSecondary">API Key</span>
                    {apiKey ? (
                      <span className="flex items-center gap-1 text-xs text-green-500">
                        <div className="w-2 h-2 rounded-full bg-green-500" />
                        Configured
                      </span>
                    ) : (
                      <span className="flex items-center gap-1 text-xs text-red-500">
                        <div className="w-2 h-2 rounded-full bg-red-500" />
                        Not configured
                      </span>
                    )}
                  </div>

                  {isEditingKey ? (
                    <div className="flex items-center gap-2">
                      <input
                        type="password"
                        value={tempKey}
                        onChange={(e) => setTempKey(e.target.value)}
                        placeholder="iaf_xxxxxxxxxx"
                        className={classNames(
                          'flex-1 px-3 py-2 rounded-lg text-sm',
                          'bg-bolt-elements-background-depth-3 border border-bolt-elements-borderColor',
                          'text-bolt-elements-textPrimary placeholder-bolt-elements-textTertiary',
                          'focus:outline-none focus:ring-2 focus:ring-purple-500/30',
                        )}
                      />
                      <button
                        onClick={handleSaveApiKey}
                        className="px-3 py-2 text-sm bg-green-500/20 text-green-500 rounded-lg hover:bg-green-500/30 transition-colors"
                      >
                        Save
                      </button>
                      <button
                        onClick={() => {
                          setIsEditingKey(false);
                          setTempKey(apiKey);
                        }}
                        className="px-3 py-2 text-sm bg-red-500/20 text-red-500 rounded-lg hover:bg-red-500/30 transition-colors"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => setIsEditingKey(true)}
                        className="px-3 py-2 text-sm bg-purple-500/20 text-purple-500 rounded-lg hover:bg-purple-500/30 transition-colors"
                      >
                        {apiKey ? 'Change API Key' : 'Set API Key'}
                      </button>
                      {!apiKey && (
                        <a
                          href={IAFACTORY_API_KEY_LINK}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="px-3 py-2 text-sm bg-blue-500/20 text-blue-500 rounded-lg hover:bg-blue-500/30 transition-colors"
                        >
                          Get API Key
                        </a>
                      )}
                    </div>
                  )}
                </motion.div>
              )}
            </div>
          </div>

          <motion.div
            className="absolute inset-0 border-2 border-purple-500/0 rounded-lg pointer-events-none"
            animate={{
              borderColor: isEnabled ? 'rgba(168, 85, 247, 0.2)' : 'rgba(168, 85, 247, 0)',
              scale: isEnabled ? 1 : 0.98,
            }}
            transition={{ duration: 0.2 }}
          />
        </motion.div>

        {/* Info Box */}
        <motion.div
          className={classNames(
            'rounded-lg p-4',
            'bg-blue-500/10 border border-blue-500/20',
          )}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          <h5 className="text-sm font-medium text-blue-400 mb-2">Why IAFactory?</h5>
          <ul className="text-xs text-bolt-elements-textSecondary space-y-1">
            <li>• Unified access to multiple AI models (GPT-4, Claude, Llama, DeepSeek)</li>
            <li>• Pay-as-you-go billing with transparent pricing</li>
            <li>• No need to manage multiple API keys</li>
            <li>• Automatic fallback if a provider is down</li>
          </ul>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default CloudProvidersTab;
