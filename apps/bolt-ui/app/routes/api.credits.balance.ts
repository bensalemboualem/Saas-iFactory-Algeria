import { json, type LoaderFunctionArgs } from '@remix-run/cloudflare';

export const loader = async ({ request: _request }: LoaderFunctionArgs) => {
  // TODO: Implement real credits balance from database/service
  return json({
    balance: 1000,
    currency: 'DZD',
    unlimited: false,
  });
};
