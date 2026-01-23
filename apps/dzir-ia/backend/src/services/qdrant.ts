import { QdrantClient } from '@qdrant/js-client-rest';

const QDRANT_URL = process.env.QDRANT_URL || 'http://localhost:6333';
const COLLECTION_NAME = 'dzir_chunks';
const VECTOR_SIZE = 1536; // OpenAI ada-002 embedding size

let client: QdrantClient | null = null;

export function getQdrantClient(): QdrantClient {
  if (!client) {
    client = new QdrantClient({ url: QDRANT_URL });
  }
  return client;
}

export async function initializeQdrant(): Promise<void> {
  const qdrant = getQdrantClient();

  try {
    const collections = await qdrant.getCollections();
    const exists = collections.collections.some((c) => c.name === COLLECTION_NAME);

    if (!exists) {
      await qdrant.createCollection(COLLECTION_NAME, {
        vectors: {
          size: VECTOR_SIZE,
          distance: 'Cosine',
        },
        optimizers_config: {
          default_segment_number: 2,
        },
        replication_factor: 1,
      });

      // Create payload indexes for filtering
      await qdrant.createPayloadIndex(COLLECTION_NAME, {
        field_name: 'userId',
        field_schema: 'keyword',
      });

      await qdrant.createPayloadIndex(COLLECTION_NAME, {
        field_name: 'collectionId',
        field_schema: 'keyword',
      });

      await qdrant.createPayloadIndex(COLLECTION_NAME, {
        field_name: 'documentId',
        field_schema: 'keyword',
      });

      console.log(`Created Qdrant collection: ${COLLECTION_NAME}`);
    } else {
      console.log(`Qdrant collection ${COLLECTION_NAME} already exists`);
    }
  } catch (error) {
    console.error('Failed to initialize Qdrant:', error);
    throw error;
  }
}

export interface VectorPoint {
  id: string;
  vector: number[];
  payload: {
    userId: string;
    collectionId: string;
    documentId: string;
    chunkId: string;
    content: string;
    position: number;
    metadata?: Record<string, unknown>;
  };
}

export async function upsertVectors(points: VectorPoint[]): Promise<void> {
  const qdrant = getQdrantClient();
  await qdrant.upsert(COLLECTION_NAME, {
    wait: true,
    points: points.map((p) => ({
      id: p.id,
      vector: p.vector,
      payload: p.payload,
    })),
  });
}

export async function searchVectors(
  vector: number[],
  userId: string,
  collectionIds?: string[],
  limit: number = 10,
  threshold: number = 0.7
): Promise<Array<{ id: string; score: number; payload: VectorPoint['payload'] }>> {
  const qdrant = getQdrantClient();

  const filter: Record<string, unknown> = {
    must: [{ key: 'userId', match: { value: userId } }],
  };

  if (collectionIds && collectionIds.length > 0) {
    (filter.must as Array<Record<string, unknown>>).push({
      key: 'collectionId',
      match: { any: collectionIds },
    });
  }

  const results = await qdrant.search(COLLECTION_NAME, {
    vector,
    limit,
    score_threshold: threshold,
    filter,
    with_payload: true,
  });

  return results.map((r) => ({
    id: r.id as string,
    score: r.score,
    payload: r.payload as VectorPoint['payload'],
  }));
}

export async function deleteVectorsByDocument(documentId: string): Promise<void> {
  const qdrant = getQdrantClient();
  await qdrant.delete(COLLECTION_NAME, {
    wait: true,
    filter: {
      must: [{ key: 'documentId', match: { value: documentId } }],
    },
  });
}

export async function deleteVectorsByCollection(collectionId: string): Promise<void> {
  const qdrant = getQdrantClient();
  await qdrant.delete(COLLECTION_NAME, {
    wait: true,
    filter: {
      must: [{ key: 'collectionId', match: { value: collectionId } }],
    },
  });
}
