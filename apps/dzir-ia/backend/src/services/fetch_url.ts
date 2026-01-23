import { JSDOM } from 'jsdom';
import { Readability } from '@mozilla/readability';
import { isIP } from 'node:net';

export interface ExtractedContent {
  title: string;
  content: string;
  byline?: string;
  excerpt?: string;
  siteName?: string;
  lang?: string;
}

export interface FetchUrlOptions {
  timeout?: number;
  userAgent?: string;
}

const DEFAULT_USER_AGENT =
  'Mozilla/5.0 (compatible; DzirIA/1.0; +https://iafactory.dz/bot)';

const DEFAULT_TIMEOUT = 30000; // 30 seconds

// SSRF Protection: Blocked hosts and IP ranges
const BLOCKED_HOSTS = [
  'localhost',
  'localhost.localdomain',
  '127.0.0.1',
  '0.0.0.0',
  '::1',
  '[::1]',
  'metadata.google.internal',
  'metadata.google',
  '169.254.169.254', // AWS/GCP metadata
  'instance-data', // AWS metadata alias
];

// Private IP ranges (CIDR notation check)
function isPrivateIP(ip: string): boolean {
  // Remove IPv6 brackets if present
  const cleanIP = ip.replace(/^\[|\]$/g, '');

  // Check if it's a valid IP
  const ipVersion = isIP(cleanIP);
  if (ipVersion === 0) return false;

  if (ipVersion === 4) {
    const parts = cleanIP.split('.').map(Number);
    // 10.0.0.0/8
    if (parts[0] === 10) return true;
    // 172.16.0.0/12
    if (parts[0] === 172 && parts[1] >= 16 && parts[1] <= 31) return true;
    // 192.168.0.0/16
    if (parts[0] === 192 && parts[1] === 168) return true;
    // 127.0.0.0/8 (loopback)
    if (parts[0] === 127) return true;
    // 169.254.0.0/16 (link-local)
    if (parts[0] === 169 && parts[1] === 254) return true;
    // 0.0.0.0/8
    if (parts[0] === 0) return true;
  }

  if (ipVersion === 6) {
    const lower = cleanIP.toLowerCase();
    // Loopback
    if (lower === '::1') return true;
    // Link-local (fe80::/10)
    if (lower.startsWith('fe80:')) return true;
    // Private (fc00::/7)
    if (lower.startsWith('fc') || lower.startsWith('fd')) return true;
  }

  return false;
}

/**
 * Validate URL for SSRF protection
 */
function validateUrlForSSRF(url: string): void {
  const parsed = new URL(url);
  const hostname = parsed.hostname.toLowerCase();

  // Block disallowed schemes
  if (!['http:', 'https:'].includes(parsed.protocol)) {
    throw new FetchUrlError(`Blocked protocol: ${parsed.protocol}`, 400, url);
  }

  // Block known dangerous hosts
  if (BLOCKED_HOSTS.includes(hostname)) {
    throw new FetchUrlError(`Blocked host: ${hostname}`, 403, url);
  }

  // Block private IPs
  if (isPrivateIP(hostname)) {
    throw new FetchUrlError(`Blocked private IP: ${hostname}`, 403, url);
  }

  // Block URLs with credentials
  if (parsed.username || parsed.password) {
    throw new FetchUrlError('URLs with credentials are not allowed', 400, url);
  }

  // Block non-standard ports that might be used for internal services
  const port = parsed.port ? parseInt(parsed.port, 10) : (parsed.protocol === 'https:' ? 443 : 80);
  const allowedPorts = [80, 443, 8080, 8443];
  if (!allowedPorts.includes(port)) {
    throw new FetchUrlError(`Port ${port} is not allowed`, 403, url);
  }
}

export class FetchUrlError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public url?: string
  ) {
    super(message);
    this.name = 'FetchUrlError';
  }
}

/**
 * Fetch and extract readable content from a URL
 */
export async function fetchAndExtract(
  url: string,
  options: FetchUrlOptions = {}
): Promise<ExtractedContent> {
  const { timeout = DEFAULT_TIMEOUT, userAgent = DEFAULT_USER_AGENT } = options;

  // Validate URL
  let parsedUrl: URL;
  try {
    parsedUrl = new URL(url);
  } catch {
    throw new FetchUrlError(`Invalid URL: ${url}`, 400, url);
  }

  // SSRF Protection: Validate URL before fetching
  validateUrlForSSRF(url);

  // Fetch the page
  let response: Response;
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    response = await fetch(url, {
      headers: {
        'User-Agent': userAgent,
        Accept: 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5,fr;q=0.3,ar;q=0.2',
      },
      signal: controller.signal,
      redirect: 'follow',
    });

    clearTimeout(timeoutId);
  } catch (error) {
    if (error instanceof Error && error.name === 'AbortError') {
      throw new FetchUrlError(`Request timeout after ${timeout}ms`, 408, url);
    }
    throw new FetchUrlError(`Failed to fetch URL: ${error}`, 500, url);
  }

  if (!response.ok) {
    throw new FetchUrlError(
      `HTTP error: ${response.status} ${response.statusText}`,
      response.status,
      url
    );
  }

  // Check content type
  const contentType = response.headers.get('content-type') || '';
  if (!contentType.includes('text/html') && !contentType.includes('application/xhtml')) {
    throw new FetchUrlError(
      `Unsupported content type: ${contentType}. Expected HTML.`,
      415,
      url
    );
  }

  // Get HTML content
  const html = await response.text();

  if (!html || html.trim().length === 0) {
    throw new FetchUrlError('Empty response body', 204, url);
  }

  // Parse with JSDOM
  const dom = new JSDOM(html, {
    url,
    contentType: 'text/html',
  });

  const document = dom.window.document;

  // Extract with Readability
  const reader = new Readability(document, {
    charThreshold: 100,
    keepClasses: false,
  });

  const article = reader.parse();

  if (!article || !article.textContent || article.textContent.trim().length < 50) {
    // Fallback: try to get basic content
    const fallbackContent = extractFallbackContent(document);
    if (fallbackContent.content.length < 50) {
      throw new FetchUrlError(
        'Could not extract meaningful content from the page',
        422,
        url
      );
    }
    return fallbackContent;
  }

  // Clean up the text content
  const cleanContent = cleanText(article.textContent);

  return {
    title: article.title || extractTitle(document) || parsedUrl.hostname,
    content: cleanContent,
    byline: article.byline || undefined,
    excerpt: article.excerpt || undefined,
    siteName: article.siteName || undefined,
    lang: article.lang || document.documentElement.lang || undefined,
  };
}

/**
 * Fallback content extraction when Readability fails
 */
function extractFallbackContent(document: Document): ExtractedContent {
  // Try to get main content areas
  const selectors = [
    'main',
    'article',
    '[role="main"]',
    '.content',
    '.post-content',
    '.entry-content',
    '.article-content',
    '#content',
    '#main',
  ];

  let content = '';

  for (const selector of selectors) {
    const element = document.querySelector(selector);
    if (element) {
      content = cleanText(element.textContent || '');
      if (content.length > 100) break;
    }
  }

  // Last resort: get body text
  if (content.length < 100) {
    // Remove script, style, nav, header, footer
    const clone = document.body.cloneNode(true) as HTMLElement;
    const removeSelectors = ['script', 'style', 'nav', 'header', 'footer', 'aside', '.sidebar'];
    removeSelectors.forEach((sel) => {
      clone.querySelectorAll(sel).forEach((el) => el.remove());
    });
    content = cleanText(clone.textContent || '');
  }

  return {
    title: extractTitle(document),
    content,
  };
}

/**
 * Extract page title
 */
function extractTitle(document: Document): string {
  // Try og:title first
  const ogTitle = document.querySelector('meta[property="og:title"]');
  if (ogTitle) {
    const content = ogTitle.getAttribute('content');
    if (content) return content.trim();
  }

  // Try twitter:title
  const twitterTitle = document.querySelector('meta[name="twitter:title"]');
  if (twitterTitle) {
    const content = twitterTitle.getAttribute('content');
    if (content) return content.trim();
  }

  // Fall back to title tag
  const titleTag = document.querySelector('title');
  if (titleTag && titleTag.textContent) {
    return titleTag.textContent.trim();
  }

  // Last resort: h1
  const h1 = document.querySelector('h1');
  if (h1 && h1.textContent) {
    return h1.textContent.trim();
  }

  return 'Untitled';
}

/**
 * Clean and normalize text content
 */
function cleanText(text: string): string {
  return text
    // Normalize whitespace
    .replace(/[\t\r]+/g, ' ')
    // Collapse multiple newlines to max 2
    .replace(/\n{3,}/g, '\n\n')
    // Collapse multiple spaces
    .replace(/ {2,}/g, ' ')
    // Remove leading/trailing whitespace from lines
    .split('\n')
    .map((line) => line.trim())
    .join('\n')
    // Final trim
    .trim();
}

/**
 * Check if a URL is likely to be a valid web page
 */
export function isValidWebUrl(url: string): boolean {
  try {
    const parsed = new URL(url);
    return ['http:', 'https:'].includes(parsed.protocol);
  } catch {
    return false;
  }
}
