import { serve } from '@hono/node-server';
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import toolsRoute from './routes/tools';

const app = new Hono();

app.use('/*', cors());

app.get('/', (c) => c.text('IA Factory Algeria API Gateway'));

// Mount Routes
app.route('/tools', toolsRoute);

const port = 3001;
console.log(`Server is running on port ${port}`);

serve({
    fetch: app.fetch,
    port
});
