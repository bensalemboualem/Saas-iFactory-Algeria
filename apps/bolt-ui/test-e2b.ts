/**
 * Test E2B - IAFactory Algérie
 * Vérifie que le SDK E2B fonctionne correctement
 */

import { Sandbox } from '@e2b/code-interpreter';

async function testE2B() {
  console.log('🧪 Test E2B IAFactory...\n');

  // Test 1: Création sandbox
  console.log('1. Création sandbox...');
  const apiKey = process.env.VITE_E2B_API_KEY || process.env.E2B_API_KEY;
  if (!apiKey) {
    console.error('❌ VITE_E2B_API_KEY / E2B_API_KEY not set - skipping live E2B test to avoid leaking keys.');
    return;
  }
  const sandbox = await Sandbox.create({ apiKey });
  console.log('✅ Sandbox créé:', sandbox.sandboxId, '\n');

  // Test 2: Exécution Python
  console.log('2. Exécution Python...');
  const result = await sandbox.runCode('print("Salam Algérie! 🇩🇿")');
  console.log('✅ Result:', JSON.stringify(result, null, 2));
  // Check different output properties
  console.log('   - logs:', result.logs);
  console.log('   - results:', result.results);

  // Test 3: Test fichiers
  console.log('\n3. Test fichiers...');
  await sandbox.files.write('/home/user/test.txt', 'Bonjour IAFactory!');
  const content = await sandbox.files.read('/home/user/test.txt');
  console.log('✅ Fichier lu:', content);

  // Test 4: Exécution commande shell
  console.log('\n4. Test commande shell...');
  const cmdResult = await sandbox.commands.run('echo "Hello from E2B sandbox"');
  console.log('✅ Shell output:', cmdResult.stdout);

  // Test 5: Cleanup
  await sandbox.kill();
  console.log('\n✅ Test terminé avec succès!');
}

testE2B().catch((error) => {
  console.error('❌ Erreur:', error.message);
  process.exit(1);
});
