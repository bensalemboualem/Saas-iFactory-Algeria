import * as Minio from 'minio';

const MINIO_ENDPOINT = process.env.MINIO_ENDPOINT || 'localhost';
const MINIO_PORT = parseInt(process.env.MINIO_PORT || '9000');
const MINIO_ACCESS_KEY = process.env.MINIO_ACCESS_KEY || 'minioadmin';
const MINIO_SECRET_KEY = process.env.MINIO_SECRET_KEY || 'minioadmin';
const MINIO_USE_SSL = process.env.MINIO_USE_SSL === 'true';
const BUCKET_NAME = 'dzir-files';

let client: Minio.Client | null = null;

export function getMinioClient(): Minio.Client {
  if (!client) {
    client = new Minio.Client({
      endPoint: MINIO_ENDPOINT,
      port: MINIO_PORT,
      useSSL: MINIO_USE_SSL,
      accessKey: MINIO_ACCESS_KEY,
      secretKey: MINIO_SECRET_KEY,
    });
  }
  return client;
}

export async function initializeMinio(): Promise<void> {
  const minio = getMinioClient();

  try {
    const bucketExists = await minio.bucketExists(BUCKET_NAME);

    if (!bucketExists) {
      await minio.makeBucket(BUCKET_NAME, 'us-east-1');
      console.log(`Created MinIO bucket: ${BUCKET_NAME}`);
    } else {
      console.log(`MinIO bucket ${BUCKET_NAME} already exists`);
    }
  } catch (error) {
    console.error('Failed to initialize MinIO:', error);
    throw error;
  }
}

export async function uploadFile(
  userId: string,
  fileName: string,
  buffer: Buffer,
  contentType: string
): Promise<string> {
  const minio = getMinioClient();
  const objectName = `${userId}/${Date.now()}-${fileName}`;

  await minio.putObject(BUCKET_NAME, objectName, buffer, buffer.length, {
    'Content-Type': contentType,
  });

  return objectName;
}

export async function getFileUrl(objectName: string, expiresIn: number = 3600): Promise<string> {
  const minio = getMinioClient();
  return minio.presignedGetObject(BUCKET_NAME, objectName, expiresIn);
}

export async function deleteFile(objectName: string): Promise<void> {
  const minio = getMinioClient();
  await minio.removeObject(BUCKET_NAME, objectName);
}

export async function getFileBuffer(objectName: string): Promise<Buffer> {
  const minio = getMinioClient();
  const stream = await minio.getObject(BUCKET_NAME, objectName);

  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    stream.on('data', (chunk) => chunks.push(chunk));
    stream.on('end', () => resolve(Buffer.concat(chunks)));
    stream.on('error', reject);
  });
}
