import { memo } from 'react';
import { Gear, Question } from '@phosphor-icons/react';

interface SettingsButtonProps {
  onClick: () => void;
}

export const SettingsButton = memo(({ onClick }: SettingsButtonProps) => {
  return (
    <button
      onClick={onClick}
      title="Settings"
      data-testid="settings-button"
      className="flex items-center justify-center p-2 rounded-md text-gray-500 dark:text-gray-400 hover:text-bolt-elements-textPrimary hover:bg-bolt-elements-item-backgroundActive/10 transition-colors"
    >
      <Gear size={24} weight="regular" />
    </button>
  );
});

interface HelpButtonProps {
  onClick: () => void;
}

export const HelpButton = memo(({ onClick }: HelpButtonProps) => {
  return (
    <button
      onClick={onClick}
      title="Help & Documentation"
      data-testid="help-button"
      className="flex items-center justify-center p-2 rounded-md text-gray-500 dark:text-gray-400 hover:text-bolt-elements-textPrimary hover:bg-bolt-elements-item-backgroundActive/10 transition-colors"
    >
      <Question size={24} weight="regular" />
    </button>
  );
});
