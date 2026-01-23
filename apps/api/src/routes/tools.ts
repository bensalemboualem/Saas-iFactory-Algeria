import { Hono } from 'hono';
import { toolsRegistry } from '@iafactory/tools-registry';
import { aiEngine } from '@iafactory/ai-engine';
import { creditsSystem } from '@iafactory/credits-system';

const app = new Hono();

// List Tools
app.get('/', (c) => {
    const category = c.req.query('category') as any;
    const tools = toolsRegistry.getTools({ category });
    return c.json(tools);
});

// Get Tool Details
app.get('/:toolId', (c) => {
    const toolId = c.req.param('toolId');
    const tool = toolsRegistry.getTool(toolId);
    if (!tool) return c.json({ error: 'Tool not found' }, 404);
    return c.json(tool);
});

// Execute Tool
app.post('/:toolId/execute', async (c) => {
    try {
        const toolId = c.req.param('toolId');
        const inputs = await c.req.json();

        // Mock User ID for Phase 1
        const userId = "test-user-dz";

        // 1. Get Tool
        const tool = toolsRegistry.getTool(toolId);
        if (!tool) return c.json({ error: 'Tool not found' }, 404);

        // 2. Check Credits
        const hasCredits = await creditsSystem.check(userId, tool.credits);
        if (!hasCredits) return c.json({ error: 'Insufficient credits' }, 402);

        // 3. Build Prompt
        const prompt = toolsRegistry.buildPrompt(tool, inputs);

        // 4. AI Execution
        const result = await aiEngine.execute({
            model: tool.model,
            prompt,
            outputs: tool.outputs
        });

        // 5. Deduct Credits
        await creditsSystem.deduct(userId, tool.credits, toolId);

        return c.json({ result, creditsUsed: tool.credits });

    } catch (error: any) {
        console.error("Execution Error:", error);
        return c.json({ error: error.message }, 500);
    }
});

export default app;
