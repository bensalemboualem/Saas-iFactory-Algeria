import { PrismaClient } from '@prisma/client';
const prisma = new PrismaClient();

async function main() {
  const users = await prisma.user.findMany({
    include: { creditWallet: true }
  });
  console.log('=== USERS IN DB ===');
  for (const u of users) {
    console.log('- ' + (u.email || u.name || u.id));
    console.log('  ID: ' + u.id);
    console.log('  Credits: ' + (u.creditWallet?.balance ?? 'NO WALLET'));
  }
  console.log('Total: ' + users.length + ' users');
}
main().catch(console.error).finally(() => prisma.$disconnect());
