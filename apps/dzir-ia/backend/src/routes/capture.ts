import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { randomUUID } from 'node:crypto';
import { authMiddleware, getAuth } from '../middleware/auth.js';
import { rateLimit } from '../middleware/rate_limit.js';
import { chargeCredits, finalizeCredits, getCaptureCost } from '../middleware/credits.js';
import { CaptureRequestSchema } from '../types/index.js';
import * as db from '../services/sqlite.js';
import * as qdrant from '../services/qdrant.js';
import { fetchAndExtract, FetchUrlError } from '../services/fetch_url.js';
import { parsePdfBase64, PdfParseError } from '../services/parse_pdf.js';
import {
  generateEmbeddings,
  resolveEmbeddingsConfig,
  type BYOKContext,
} from '../services/embeddings.js';

const capture = new Hono();

capture.use('*', authMiddleware);
capture.use('*', rateLimit('capture'));

// Minimum content length to accept
const MIN_CONTENT_LENGTH = 50;

/**
 * Extract user token from Authorization header
 */
function extractToken(c: any): string | null {
  const authHeader = c.req.header('Authorization');
  if (!authHeader?.startsWith('Bearer ')) {
    return null;
  }
  return authHeader.slice(7);
}

// POST /capture - Capture a new document
capture.post('/', zValidator('json', CaptureRequestSchema), async (c) => {
  const auth = getAuth(c);
  const body = c.req.valid('json');
  const userToken = extractToken(c);

  // Build BYOK context
  const byokContext: BYOKContext | undefined = userToken
    ? { userId: auth.userId, userToken }
    : undefined;

  // Check and reserve credits based on source type (dynamic cost)
  const cost = getCaptureCost(body.sourceType);
  const creditsResult = await chargeCredits(c, 'capture', cost);
  if (!creditsResult.success) {
    return c.json(
      {
        error: 'INSUFFICIENT_CREDITS',
        message: creditsResult.error,
        required: cost,
      },
      402
    );
  }

  // Verify collection exists and belongs to user
  const collection = db.getCollection(auth.userId, body.collectionId);
  if (!collection) {
    return c.json({ error: 'Collection not found' }, 404);
  }

  let content = '';
  let title = body.title || 'Untitled';
  let byline: string | undefined;
  let excerpt: string | undefined;

  // Handle different source types
  if (body.sourceType === 'url' && body.sourceUrl) {
    // Fetch and extract content from URL
    try {
      const extracted = await fetchAndExtract(body.sourceUrl);
      title = body.title || extracted.title;
      content = extracted.content;
      byline = extracted.byline;
      excerpt = extracted.excerpt;
    } catch (error) {
      if (error instanceof FetchUrlError) {
        return c.json(
          {
            error: 'Failed to fetch URL',
            details: error.message,
            statusCode: error.statusCode,
          },
          error.statusCode === 400 ? 400 : 422
        );
      }
      console.error('URL fetch error:', error);
      return c.json(
        {
          error: 'Failed to fetch URL',
          details: String(error),
        },
        500
      );
    }
  } else if (body.sourceType === 'text') {
    // Raw text content
    content = body.content || '';
    title = body.title || 'Text Note';
  } else if (body.sourceType === 'pdf') {
    // Parse PDF from base64
    if (!body.pdfBase64) {
      return c.json(
        {
          error: 'Missing PDF content',
          details: 'For PDF capture, provide pdfBase64 field with base64-encoded PDF.',
        },
        400
      );
    }

    try {
      const parsed = await parsePdfBase64(body.pdfBase64);
      title = body.title || parsed.title || body.filename || 'PDF Document';
      content = parsed.content;
      // Store PDF metadata
      byline = parsed.metadata?.author;
      excerpt = `${parsed.pageCount} page${parsed.pageCount > 1 ? 's' : ''}`;
    } catch (error) {
      if (error instanceof PdfParseError) {
        return c.json(
          {
            error: 'Failed to parse PDF',
            details: error.message,
          },
          422
        );
      }
      console.error('PDF parse error:', error);
      return c.json(
        {
          error: 'Failed to parse PDF',
          details: String(error),
        },
        500
      );
    }
  } else {
    content = body.content || '';
  }

  // Validate content is not empty
  if (!content || content.trim().length < MIN_CONTENT_LENGTH) {
    return c.json(
      {
        error: 'Content too short',
        details: `Content must be at least ${MIN_CONTENT_LENGTH} characters. Got ${content?.length || 0}.`,
      },
      400
    );
  }

  // Create document (UUID so it's also safe everywhere)
  const documentId = randomUUID();
  const document = db.createDocument(auth.userId, {
    id: documentId,
    collectionId: body.collectionId,
    title,
    sourceType: body.sourceType,
    sourceUrl: body.sourceUrl,
    content,
    summary: excerpt,
    metadata: {
      byline,
      extractedAt: new Date().toISOString(),
    },
  });

  // Chunk the content
  const chunks = chunkContent(content, documentId);

  // Store chunks in SQLite
  db.createChunks(auth.userId, chunks);

  // Check if embeddings are available (server key or BYOK)
  const embeddingsConfig = await resolveEmbeddingsConfig(byokContext);
  let vectorIndexed = false;
  let embeddingsTokensUsed = 0;

  if (embeddingsConfig) {
    // Generate embeddings for all chunks
    const chunkTexts = chunks.map((chunk) => chunk.content);
    const embeddingsResult = await generateEmbeddings(chunkTexts, byokContext);

    if (embeddingsResult && embeddingsResult.embeddings.length === chunks.length) {
      // Create vector points with real embeddings
      const vectorPoints: qdrant.VectorPoint[] = chunks.map((chunk, index) => ({
        id: chunk.id, // ✅ UUID (Qdrant accepte UUID ou entier)
        vector: embeddingsResult.embeddings[index].embedding,
        payload: {
          userId: auth.userId,
          collectionId: body.collectionId,
          documentId,
          chunkId: chunk.id,
          content: chunk.content,
          position: chunk.position,
        },
      }));

      try {
        await qdrant.upsertVectors(vectorPoints);
        vectorIndexed = true;
        embeddingsTokensUsed = embeddingsResult.totalTokensUsed;
      } catch (error) {
        console.error('Failed to upsert vectors to Qdrant:', error);
        // Continue without vector indexing
      }
    } else {
      console.warn('Embeddings generation returned incomplete results');
    }
  }

  // Deduct credits after successful capture
  await finalizeCredits(c);

  return c.json(
    {
      document,
      chunksCount: chunks.length,
      vectorIndexed,
      vectorIndexDisabled: !embeddingsConfig,
      embeddingsTokensUsed,
      message: vectorIndexed
        ? 'Document captured and indexed successfully'
        : embeddingsConfig
          ? 'Document captured but vector indexing failed'
          : 'Document captured (vector indexing disabled - no API key)',
    },
    201
  );
});

// Improved chunking function with sentence awareness
function chunkContent(
  content: string,
  documentId: string,
  maxChunkSize: number = 1000,
  minChunkSize: number = 100,
  overlap: number = 150
): Array<{ id: string; documentId: string; content: string; position: number }> {
  const chunks: Array<{ id: string; documentId: string; content: string; position: number }> = [];

  // Normalize content
  const normalizedContent = content
    .replace(/\r\n/g, '\n')
    .replace(/\r/g, '\n')
    .trim();

  if (normalizedContent.length <= maxChunkSize) {
    // Content fits in one chunk
    return [
      {
        id: randomUUID(), // ✅ UUID
        documentId,
        content: normalizedContent,
        position: 0,
      },
    ];
  }

  // Split into paragraphs first
  const paragraphs = normalizedContent.split(/\n\n+/).filter((p) => p.trim().length > 0);

  let currentChunk = '';
  let position = 0;

  for (let i = 0; i < paragraphs.length; i++) {
    const paragraph = paragraphs[i].trim();

    // If single paragraph is too long, split by sentences
    if (paragraph.length > maxChunkSize) {
      // Save current chunk if exists
      if (currentChunk.length >= minChunkSize) {
        chunks.push({
          id: randomUUID(), // ✅ UUID
          documentId,
          content: currentChunk.trim(),
          position: position++,
        });
        currentChunk = '';
      }

      // Split long paragraph by sentences
      const sentences = splitIntoSentences(paragraph);
      for (const sentence of sentences) {
        if (currentChunk.length + sentence.length > maxChunkSize && currentChunk.length >= minChunkSize) {
          chunks.push({
            id: randomUUID(), // ✅ UUID
            documentId,
            content: currentChunk.trim(),
            position: position++,
          });
          // Start new chunk with overlap
          currentChunk = getOverlapText(currentChunk, overlap) + ' ' + sentence;
        } else {
          currentChunk += (currentChunk ? ' ' : '') + sentence;
        }
      }
      continue;
    }

    // Check if adding this paragraph exceeds limit
    if (currentChunk.length + paragraph.length + 2 > maxChunkSize && currentChunk.length >= minChunkSize) {
      // Save current chunk
      chunks.push({
        id: randomUUID(), // ✅ UUID
        documentId,
        content: currentChunk.trim(),
        position: position++,
      });

      // Start new chunk with overlap from previous
      const overlapText = getOverlapText(currentChunk, overlap);
      currentChunk = overlapText ? overlapText + '\n\n' + paragraph : paragraph;
    } else {
      // Add to current chunk
      currentChunk += (currentChunk ? '\n\n' : '') + paragraph;
    }
  }

  // Don't forget the last chunk
  if (currentChunk.trim().length >= minChunkSize) {
    chunks.push({
      id: randomUUID(), // ✅ UUID
      documentId,
      content: currentChunk.trim(),
      position: position,
    });
  } else if (currentChunk.trim().length > 0 && chunks.length > 0) {
    // Append to previous chunk if too small
    chunks[chunks.length - 1].content += '\n\n' + currentChunk.trim();
  } else if (currentChunk.trim().length > 0) {
    // If it's the only content, keep it
    chunks.push({
      id: randomUUID(), // ✅ UUID
      documentId,
      content: currentChunk.trim(),
      position: position,
    });
  }

  return chunks;
}

// Split text into sentences
function splitIntoSentences(text: string): string[] {
  // Simple sentence splitting - handles common cases
  const sentences = text.split(/(?<=[.!?])\s+(?=[A-Z])/);
  return sentences.filter((s) => s.trim().length > 0);
}

// Get overlap text from end of chunk
function getOverlapText(chunk: string, overlapSize: number): string {
  if (chunk.length <= overlapSize) {
    return chunk;
  }

  // Try to find a sentence boundary within overlap region
  const overlapRegion = chunk.slice(-overlapSize * 2);
  const sentenceMatch = overlapRegion.match(/[.!?]\s+([A-Z][^.!?]*$)/);

  if (sentenceMatch) {
    return sentenceMatch[1];
  }

  // Fall back to word boundary
  const words = chunk.slice(-overlapSize).split(/\s+/);
  // Skip first partial word
  return words.slice(1).join(' ');
}

export default capture;
