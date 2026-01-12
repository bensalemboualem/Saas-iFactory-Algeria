import http from 'k6/http';
import { check, sleep } from 'k6';

const BASE_URL = __ENV.K6_BASE_URL || 'http://localhost:8180';
const API_KEY = __ENV.K6_API_KEY || 'change-me-in-production';

export const options = {
  vus: __ENV.K6_VUS ? Number(__ENV.K6_VUS) : 25,
  duration: __ENV.K6_DURATION || '10m',
  thresholds: {
    http_req_duration: ['p(95)<1800', 'avg<900'],
    http_req_failed: ['rate<0.05'],
  },
};

function generatePayload() {
  const includeTests = Math.random() > 0.4;
  const messages = [
    { role: 'user', content: 'Projet plateforme souveraine data-room.' },
    { role: 'assistant', agent: 'bmm-architect', content: 'Architecture hexagonale, FastAPI, React, PGVector.' },
    { role: 'assistant', agent: 'bmm-pm', content: 'Epics: onboarding, ingestion, audit trail.' },
  ];

  if (includeTests) {
    messages.push({ role: 'assistant', agent: 'bmm-tea', content: 'Tests: unit, integration, chaos.' });
  }

  return JSON.stringify({
    messages,
    agents_used: includeTests
      ? ['bmm-architect', 'bmm-pm', 'bmm-tea']
      : ['bmm-architect', 'bmm-pm'],
  });
}

const headers = {
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY,
  },
};

export default function () {
  const res = http.post(`${BASE_URL}/api/orchestrator/analyze-readiness`, generatePayload(), headers);
  check(res, {
    'analyze 200': (r) => r.status === 200,
  });

  const projectReady = res.json('analysis.project_ready');

  if (!projectReady) {
    // Supervisory endpoints should remain healthy even without backlog.
    const pending = http.get(`${BASE_URL}/api/orchestrator/pending-workflows?limit=5`, {
      headers: { 'X-API-Key': API_KEY },
    });

    check(pending, {
      'pending 200': (r) => r.status === 200,
    });

    const first = pending.json('pending[0].id');
    if (first) {
      const recover = http.post(
        `${BASE_URL}/api/orchestrator/pending-workflows/${first}/recover`,
        null,
        { headers: { 'X-API-Key': API_KEY } },
      );

      check(recover, {
        'recover 200/204': (r) => r.status === 200,
      });
    }
  }

  sleep(Math.random() * 2 + 0.5);
}

