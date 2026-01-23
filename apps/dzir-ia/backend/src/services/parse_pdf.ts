import pdf from 'pdf-parse';

export interface ParsedPdf {
  title?: string;
  content: string;
  pageCount: number;
  metadata?: {
    author?: string;
    subject?: string;
    keywords?: string;
    creationDate?: string;
  };
}

export class PdfParseError extends Error {
  constructor(
    message: string,
    public readonly cause?: unknown
  ) {
    super(message);
    this.name = 'PdfParseError';
  }
}

/**
 * Parse PDF buffer and extract text content
 * @param buffer - PDF file as Buffer
 * @returns Parsed PDF with title and content
 */
export async function parsePdf(buffer: Buffer): Promise<ParsedPdf> {
  if (!buffer || buffer.length === 0) {
    throw new PdfParseError('Empty PDF buffer provided');
  }

  // Check PDF magic bytes
  const header = buffer.subarray(0, 5).toString('ascii');
  if (header !== '%PDF-') {
    throw new PdfParseError('Invalid PDF format: missing PDF header');
  }

  try {
    const data = await pdf(buffer);

    // Extract text content
    const content = data.text?.trim() || '';

    if (!content || content.length < 10) {
      throw new PdfParseError(
        'PDF contains no extractable text. It may be scanned/image-based (OCR not supported).'
      );
    }

    // Try to extract title from metadata or first line
    let title: string | undefined;

    if (data.info?.Title && typeof data.info.Title === 'string') {
      title = data.info.Title.trim();
    }

    // If no title in metadata, try to extract from first line
    if (!title) {
      const firstLine = content.split('\n')[0]?.trim();
      if (firstLine && firstLine.length > 3 && firstLine.length < 200) {
        title = firstLine;
      }
    }

    // Build metadata
    const metadata: ParsedPdf['metadata'] = {};
    if (data.info?.Author) metadata.author = String(data.info.Author);
    if (data.info?.Subject) metadata.subject = String(data.info.Subject);
    if (data.info?.Keywords) metadata.keywords = String(data.info.Keywords);
    if (data.info?.CreationDate) metadata.creationDate = String(data.info.CreationDate);

    return {
      title,
      content,
      pageCount: data.numpages || 1,
      metadata: Object.keys(metadata).length > 0 ? metadata : undefined,
    };
  } catch (error) {
    if (error instanceof PdfParseError) {
      throw error;
    }

    // Handle pdf-parse specific errors
    const message = error instanceof Error ? error.message : String(error);

    if (message.includes('password')) {
      throw new PdfParseError('PDF is password protected');
    }

    if (message.includes('Invalid') || message.includes('corrupt')) {
      throw new PdfParseError('PDF file is corrupted or invalid');
    }

    throw new PdfParseError(`Failed to parse PDF: ${message}`, error);
  }
}

/**
 * Parse base64-encoded PDF string
 * @param base64String - PDF content as base64 string
 * @returns Parsed PDF with title and content
 */
export async function parsePdfBase64(base64String: string): Promise<ParsedPdf> {
  if (!base64String || base64String.length === 0) {
    throw new PdfParseError('Empty base64 string provided');
  }

  // Remove data URL prefix if present
  const cleanBase64 = base64String.replace(/^data:application\/pdf;base64,/, '');

  try {
    const buffer = Buffer.from(cleanBase64, 'base64');
    return parsePdf(buffer);
  } catch (error) {
    if (error instanceof PdfParseError) {
      throw error;
    }
    throw new PdfParseError('Invalid base64 encoding', error);
  }
}
