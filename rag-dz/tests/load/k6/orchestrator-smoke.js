import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.K6_BASE_URL || 'http://localhost:8180';
const API_KEY = __ENV.K6_API_KEY || 'change-me-in-production';

export const options = {
  vus: __ENV.K6_VUS ? Number(__ENV.K6_VUS) : 10,
  duration: __ENV.K6_DURATION || '1m',
  thresholds: {
    http_req_duration: ['p(95)<1200', 'avg<600'],
    http_req_failed: ['rate<0.02'],
  },
};

export default function () {
  const payload = JSON.stringify({
    messages: [
      { role: 'user', content: 'Nous devons créer un portail client complet.' },
      { role: 'assistant', agent: 'bmm-architect', content: 'Architecture microservices + FastAPI/React.' },
      { role: 'assistant', agent: 'bmm-ux-designer', content: 'UX mobile-first avec 3 parcours utilisateur.' },
      { role: 'assistant', agent: 'bmm-pm', content: 'Features: Auth, espace docs, notifications.' },
      { role: 'assistant', agent: 'bmm-tea', content: 'Plan de tests unitaires + E2E.' },
    ],
    agents_used: ['bmm-architect', 'bmm-ux-designer', 'bmm-pm', 'bmm-tea'],
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': API_KEY,
    },
  };

  const analyzeRes = http.post(`${BASE_URL}/api/orchestrator/analyze-readiness`, payload, params);
  check(analyzeRes, {
    'analyze 200': (res) => res.status === 200,
    'project ready bool present': (res) => res.json('analysis.project_ready') !== undefined,
  });

  const synthRes = http.post(`${BASE_URL}/api/orchestrator/synthesize-knowledge`, payload, params);
  check(synthRes, {
    'synthesize 200': (res) => res.status === 200,
    'knowledge doc length ok': (res) => (res.json('knowledge_document') || '').length > 200,
  });

  sleep(1);
}

