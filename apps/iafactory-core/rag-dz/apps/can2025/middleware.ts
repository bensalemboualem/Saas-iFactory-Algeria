
import createMiddleware from 'next-intl/middleware';
import { locales, localePrefix } from './navigation';

export default createMiddleware({
  defaultLocale: 'fr', // Default locale if no locale is detected
  localePrefix,
  locales
});

export const config = {
  // Match only internationalized pathnames
  matcher: ['/', '/(fr|en|ar)/:path*']
};
