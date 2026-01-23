/**
 * NexusToggle - Toggle for enabling/disabling Nexus orchestration mode
 *
 * When enabled, requests are routed through the Nexus meta-orchestrator
 * which coordinates BMAD, Archon, and Bolt services.
 */

import React, { useEffect, useState } from 'react';
import { useStore } from '@nanostores/react';
import * as Tooltip from '@radix-ui/react-tooltip';
import {
  nexusModeEnabled,
  nexusConnectionStatus,
  nexusError,
  toggleNexusMode,
  refreshNexusHealth,
} from '~/lib/modules/nexus/store';

interface NexusToggleProps {
  className?: string;
}

export const NexusToggle: React.FC<NexusToggleProps> = ({ className = '' }) => {
  const enabled = useStore(nexusModeEnabled);
  const status = useStore(nexusConnectionStatus);
  const error = useStore(nexusError);
  const [isToggling, setIsToggling] = useState(false);

  // No auto-init - Nexus starts OFF by default
  // User must explicitly click to enable

  // Refresh health periodically when connected
  useEffect(() => {
    if (enabled && status === 'connected') {
      const interval = setInterval(() => {
        refreshNexusHealth();
      }, 30000); // Every 30 seconds

      return () => clearInterval(interval);
    }
  }, [enabled, status]);

  const handleToggle = async () => {
    setIsToggling(true);

    try {
      await toggleNexusMode();
    } finally {
      setIsToggling(false);
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case 'connected':
        return 'bg-green-500';
      case 'connecting':
        return 'bg-yellow-500 animate-pulse';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'connected':
        return 'Connected to Nexus';
      case 'connecting':
        return 'Connecting...';
      case 'error':
        return error || 'Connection error';
      default:
        return 'Nexus Mode OFF';
    }
  };

  return (
    <Tooltip.Provider>
      <Tooltip.Root>
        <Tooltip.Trigger asChild>
          <button
            onClick={handleToggle}
            disabled={isToggling}
            className={`
              flex items-center gap-2 px-3 py-1.5 rounded-lg
              transition-all duration-200 ease-in-out
              ${
                enabled
                  ? 'bg-[#00a651] text-white hover:bg-[#008c45]'
                  : 'bg-bolt-elements-background-depth-2 text-bolt-elements-textSecondary hover:bg-bolt-elements-background-depth-3'
              }
              ${isToggling ? 'opacity-50 cursor-wait' : 'cursor-pointer'}
              ${className}
            `}
          >
            {/* Status indicator */}
            <span className={`w-2 h-2 rounded-full ${getStatusColor()}`} />

            {/* Icon */}
            <svg
              className="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              {enabled ? (
                // Connected icon - network nodes
                <>
                  <circle cx="12" cy="12" r="3" />
                  <circle cx="19" cy="5" r="2" />
                  <circle cx="5" cy="5" r="2" />
                  <circle cx="19" cy="19" r="2" />
                  <circle cx="5" cy="19" r="2" />
                  <line x1="12" y1="9" x2="12" y2="5" />
                  <line x1="14.5" y1="13.5" x2="17" y2="17" />
                  <line x1="9.5" y1="13.5" x2="7" y2="17" />
                  <line x1="14.5" y1="10.5" x2="17" y2="7" />
                  <line x1="9.5" y1="10.5" x2="7" y2="7" />
                </>
              ) : (
                // Disconnected icon - simple circle
                <circle cx="12" cy="12" r="10" />
              )}
            </svg>

            {/* Label */}
            <span className="text-sm font-medium">
              {isToggling ? 'Connecting...' : enabled ? 'Nexus' : 'Nexus OFF'}
            </span>
          </button>
        </Tooltip.Trigger>

        <Tooltip.Portal>
          <Tooltip.Content
            className="
              bg-bolt-elements-background-depth-2
              text-bolt-elements-textPrimary
              px-3 py-2 rounded-lg shadow-lg
              text-sm max-w-xs
              border border-bolt-elements-borderColor
            "
            sideOffset={5}
          >
            <div className="flex flex-col gap-1">
              <div className="font-medium">IA Factory Nexus Mode</div>
              <div className="text-bolt-elements-textSecondary text-xs">{getStatusText()}</div>
              {enabled && (
                <div className="text-bolt-elements-textSecondary text-xs mt-1">
                  Requests routed through Meta-Orchestrator
                  <br />
                  UI validation: Chargily, i18n, RTL, Dark mode
                </div>
              )}
              {!enabled && (
                <div className="text-bolt-elements-textSecondary text-xs mt-1">
                  Click to enable Nexus orchestration
                </div>
              )}
            </div>
            <Tooltip.Arrow className="fill-bolt-elements-background-depth-2" />
          </Tooltip.Content>
        </Tooltip.Portal>
      </Tooltip.Root>
    </Tooltip.Provider>
  );
};

export default NexusToggle;
