import http from 'k6/http';
import { check } from 'k6';

const BASE_URL = __ENV.K6_BASE_URL || 'http://localhost:8180';
const API_KEY = __ENV.K6_API_KEY || 'change-me-in-production';

export const options = {
  stages: [
    { duration: '1m', target: 20 },
    { duration: '3m', target: 50 },
    { duration: '1m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<1500', 'avg<800'],
    http_req_failed: ['rate<0.03'],
  },
};

const payload = JSON.stringify({
  messages: [
    { role: 'user', content: 'Nous devons mettre en production un CRM médical.' },
    { role: 'assistant', agent: 'bmm-architect', content: 'Stack FastAPI + React + Postgres + Redis.' },
    { role: 'assistant', agent: 'bmm-pm', content: 'Features: Fiche patient, calendrier, notifications.' },
    { role: 'assistant', agent: 'bmm-ux-designer', content: 'UX responsive, accessible WCAG AA.' },
    { role: 'assistant', agent: 'bmm-tea', content: 'Plan tests unitaires + contract tests.' },
  ],
  agents_used: ['bmm-architect', 'bmm-pm', 'bmm-ux-designer', 'bmm-tea'],
});

const params = {
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY,
  },
};

export default function () {
  const res = http.post(`${BASE_URL}/api/orchestrator/analyze-readiness`, payload, params);

  check(res, {
    'status 200': (r) => r.status === 200,
    'confidence present': (r) => typeof r.json('analysis.confidence_score') === 'number',
  });
}

