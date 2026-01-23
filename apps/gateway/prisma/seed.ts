import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Seeding gateway database...');

  // Create test org
  const org = await prisma.org.upsert({
    where: { slug: 'iafactory-test' },
    update: {},
    create: {
      name: 'IAFactory Test',
      slug: 'iafactory-test',
      isActive: true,
    },
  });
  console.log('✅ Org created:', org.slug);

  // Create test user
  const user = await prisma.user.upsert({
    where: { email: 'test@iafactory.dz' },
    update: {},
    create: {
      email: 'test@iafactory.dz',
      name: 'Test User',
      role: 'admin',
      isActive: true,
      orgId: org.id,
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
      key: 'iaf_test_key_12345',
      name: 'Test API Key',
      userId: user.id,
      isActive: true,
    },
  });
  console.log('✅ API Key created:', apiKey.key);

  console.log('\n🎉 Seed completed!');
  console.log('\n📋 Test with:');
  console.log('curl -X POST http://localhost:3001/v1/chat/completions \\');
  console.log('  -H "Authorization: Bearer iaf_test_key_12345" \\');
  console.log('  -H "Content-Type: application/json" \\');
  console.log('  -d \'{"model": "iaf-cheap-deepseek", "messages": [{"role": "user", "content": "Hello!"}]}\'');
}

main()
  .catch((e) => {
    console.error('❌ Seed failed:', e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
