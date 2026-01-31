import { useStore } from '@nanostores/react';
import { memo, useEffect, useState } from 'react';
import { themeStore, toggleTheme } from '~/lib/stores/theme';
import { SunDim, MoonStars } from '@phosphor-icons/react';
import { classNames } from '~/utils/classNames';

interface ThemeSwitchProps {
  className?: string;
}

export const ThemeSwitch = memo(({ className }: ThemeSwitchProps) => {
  const theme = useStore(themeStore);
  const [domLoaded, setDomLoaded] = useState(false);

  useEffect(() => {
    setDomLoaded(true);
  }, []);

  return (
    domLoaded && (
      <button
        className={classNames(
          'flex items-center justify-center p-2 rounded-md text-gray-500 dark:text-gray-400 hover:text-bolt-elements-textPrimary hover:bg-bolt-elements-item-backgroundActive/10 transition-colors',
          className
        )}
        title="Toggle Theme"
        onClick={toggleTheme}
      >
        {theme === 'dark' ? (
          <SunDim size={24} weight="duotone" />
        ) : (
          <MoonStars size={24} weight="duotone" />
        )}
      </button>
    )
  );
});
