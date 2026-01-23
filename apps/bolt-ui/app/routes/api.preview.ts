import { json, type ActionFunctionArgs, type LoaderFunctionArgs } from '@remix-run/cloudflare';
import { withSecurity } from '~/lib/security';
import { ensurePreviewServer, getPreviewStatus } from '~/lib/.server/preview-manager';

async function previewStatusLoader({ request }: LoaderFunctionArgs) {
  const status = await getPreviewStatus(request);
  return json(status);
}

async function previewStartAction({ request }: ActionFunctionArgs) {
  const status = await ensurePreviewServer(request);
  return json(status);
}

export const loader = withSecurity(previewStatusLoader, { allowedMethods: ['GET'] });
export const action = withSecurity(previewStartAction, { allowedMethods: ['POST'] });
