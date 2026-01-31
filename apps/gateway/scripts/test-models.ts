/**
 * IAFactory Model Tester
 * Tests all models through the gateway to verify they work
 *
 * Usage: npx ts-node scripts/test-models.ts
 */

const GATEWAY_URL = 'http://localhost:5191/v1';
const TEST_API_KEY = 'iaf_test_key_12345';

interface TestResult {
  model: string;
  status: 'success' | 'error' | 'timeout';
  latency?: number;
  error?: string;
}

const MODELS_TO_TEST = [
  // FAST - Groq (should be fastest)
  'iaf-fast-llama-70b',
  'iaf-fast-llama-8b',

  // SMART - Premium
  'iaf-smart-gpt4o-mini',
  'iaf-smart-claude-haiku',
  'iaf-smart-gemini-flash',

  // CHEAP - DeepSeek
  'iaf-cheap-deepseek-v3',

  // OPEN - OpenRouter
  'iaf-open-llama-8b',
  'iaf-open-mistral-small',
];

async function testModel(model: string): Promise<TestResult> {
  const start = Date.now();

  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 30000); // 30s timeout

    const response = await fetch(`${GATEWAY_URL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${TEST_API_KEY}`,
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: 'user', content: 'Say "OK" and nothing else.' }
        ],
        max_tokens: 10,
        temperature: 0,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeout);

    if (!response.ok) {
      const error = await response.text();
      return {
        model,
        status: 'error',
        latency: Date.now() - start,
        error: `HTTP ${response.status}: ${error.substring(0, 100)}`,
      };
    }

    const data = await response.json();
    const content = data.choices?.[0]?.message?.content || '';

    return {
      model,
      status: 'success',
      latency: Date.now() - start,
    };

  } catch (error: any) {
    if (error.name === 'AbortError') {
      return {
        model,
        status: 'timeout',
        latency: 30000,
        error: 'Request timed out after 30s',
      };
    }

    return {
      model,
      status: 'error',
      latency: Date.now() - start,
      error: error.message,
    };
  }
}

async function main() {
  console.log('🧪 IAFactory Model Tester');
  console.log('========================');
  console.log(`Gateway: ${GATEWAY_URL}`);
  console.log(`API Key: ${TEST_API_KEY.substring(0, 10)}...`);
  console.log('');

  // First, check if gateway is reachable
  try {
    const healthCheck = await fetch(`${GATEWAY_URL}/models`, {
      headers: { 'Authorization': `Bearer ${TEST_API_KEY}` },
    });

    if (!healthCheck.ok) {
      console.error('❌ Gateway not reachable or auth failed');
      console.error(`   Status: ${healthCheck.status}`);
      const error = await healthCheck.text();
      console.error(`   Error: ${error.substring(0, 200)}`);
      process.exit(1);
    }

    console.log('✅ Gateway connected\n');
  } catch (error: any) {
    console.error('❌ Cannot connect to gateway:', error.message);
    process.exit(1);
  }

  // Test each model
  const results: TestResult[] = [];

  for (const model of MODELS_TO_TEST) {
    process.stdout.write(`Testing ${model}... `);
    const result = await testModel(model);
    results.push(result);

    if (result.status === 'success') {
      console.log(`✅ ${result.latency}ms`);
    } else if (result.status === 'timeout') {
      console.log(`⏱️ TIMEOUT`);
    } else {
      console.log(`❌ ${result.error}`);
    }
  }

  // Summary
  console.log('\n📊 Summary');
  console.log('==========');

  const success = results.filter(r => r.status === 'success').length;
  const errors = results.filter(r => r.status === 'error').length;
  const timeouts = results.filter(r => r.status === 'timeout').length;

  console.log(`✅ Success: ${success}/${results.length}`);
  console.log(`❌ Errors: ${errors}/${results.length}`);
  console.log(`⏱️ Timeouts: ${timeouts}/${results.length}`);

  if (errors > 0 || timeouts > 0) {
    console.log('\n❌ Failed models:');
    results.filter(r => r.status !== 'success').forEach(r => {
      console.log(`   - ${r.model}: ${r.error || 'timeout'}`);
    });
  }

  // Exit with error if any failed
  process.exit(errors + timeouts > 0 ? 1 : 0);
}

main();
