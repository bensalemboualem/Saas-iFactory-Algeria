import { PrismaClient } from '../src/generated/prisma/index.js';
import { randomUUID } from 'crypto';

const prisma = new PrismaClient();

// Fixed IDs for test data
const TEST_ORG_ID = 'org_test_iafactory_001';
const TEST_USER_ID = 'usr_test_iafactory_001';
const TEST_API_KEY_ID = 'key_test_iafactory_001';

async function main() {
  console.log('🌱 Seeding gateway database...');

  // Create test org
  const org = await prisma.org.upsert({
    where: { slug: 'iafactory-test' },
    update: {},
    create: {
      id: TEST_ORG_ID,
      name: 'IAFactory Test',
      slug: 'iafactory-test',
      isActive: true,
      updatedAt: new Date(),
    },
  });
  console.log('✅ Org created:', org.slug);

  // Create test user
  const user = await prisma.user.upsert({
    where: { email: 'test@iafactory.dz' },
    update: {},
    create: {
      id: TEST_USER_ID,
      email: 'test@iafactory.dz',
      name: 'Test User',
      role: 'admin',
      isActive: true,
      orgId: org.id,
      updatedAt: new Date(),
    },
  });
  console.log('✅ User created:', user.email);

  // Create credit wallet with 1000 credits
  const wallet = await prisma.creditWallet.upsert({
    where: { userId: user.id },
    update: { balance: 1000 },
    create: {
      userId: user.id,
      balance: 1000,
    },
  });
  console.log('✅ Wallet created with', wallet.balance, 'credits');

  // Create API key
  const apiKey = await prisma.apiKey.upsert({
    where: { key: 'iaf_test_key_12345' },
    update: {},
    create: {
      id: TEST_API_KEY_ID,
      key: 'iaf_test_key_12345',
      name: 'Test API Key',
      userId: user.id,
      isActive: true,
    },
  });
  console.log('✅ API Key created:', apiKey.key);

  console.log('\n🎉 Seed completed!');
  console.log('\n📋 Test with:');
  console.log('curl -X POST http://localhost:5191/v1/chat/completions \\');
  console.log('  -H "Authorization: Bearer iaf_test_key_12345" \\');
  console.log('  -H "Content-Type: application/json" \\');
  console.log('  -d \'{"model": "iaf-cheap-deepseek-v3", "messages": [{"role": "user", "content": "Hello!"}]}\'');
}

main()
  .catch((e) => {
    console.error('❌ Seed failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
