# Cost/Model Router

> **Priorité**: P2  
> **Rôle**: Optimisation coût/latence LLM  
> **Droits**: Read only

---

## Mission

Choisir le modèle optimal selon la tâche.
Minimiser les coûts tout en maintenant la qualité.
Gérer les quotas par provider.
Router vers modèles locaux quand possible.

---

## Matrice Tâche → Modèle

| Tâche | Priorité | Modèles recommandés |
|-------|----------|---------------------|
| Formatting, simple | Cost | deepseek-chat, groq/llama-3.1-8b |
| Translation | Cost | deepseek-chat |
| Code completion | Balanced | deepseek-coder, claude-3-5-haiku |
| Documentation | Quality | claude-3-5-sonnet, gpt-4o |
| Architecture | Quality | claude-3-5-sonnet, gpt-4o |
| Code generation | Quality | claude-3-5-sonnet, deepseek-coder |
| Security review | Quality | claude-3-5-sonnet |
| PRD generation | Quality | claude-3-5-sonnet, gpt-4o |

---

## Pricing (par 1M tokens)

| Provider | Model | Input | Output |
|----------|-------|-------|--------|
| DeepSeek | deepseek-chat | $0.14 | $0.28 |
| DeepSeek | deepseek-coder | $0.14 | $0.28 |
| Groq | llama-3.1-8b | $0.05 | $0.08 |
| Groq | llama-3.1-70b | $0.59 | $0.79 |
| Google | gemini-2.0-flash | $0.075 | $0.30 |
| Anthropic | claude-3-5-haiku | $0.25 | $1.25 |
| Anthropic | claude-3-5-sonnet | $3.00 | $15.00 |
| OpenAI | gpt-4o-mini | $0.15 | $0.60 |
| OpenAI | gpt-4o | $2.50 | $10.00 |
| OpenAI | gpt-5 | $5.00 | $15.00 |
| Ollama | * | $0.00 | $0.00 |

---

## Routing Logic

```python
class CostModelRouter:
    async def route(self, task: Task, priority: str = "balanced") -> Model:
        candidates = TASK_MODEL_MATRIX[task.type]["models"]
        
        for model in candidates:
            # Check quota
            if not await self.has_quota(model):
                continue
            
            # Score
            cost_score = self.get_cost_score(model)
            quality_score = self.get_quality_score(model, task.type)
            
            if priority == "cost":
                score = cost_score * 0.8 + quality_score * 0.2
            elif priority == "quality":
                score = cost_score * 0.2 + quality_score * 0.8
            else:  # balanced
                score = cost_score * 0.5 + quality_score * 0.5
            
            # Return best available
            return model
        
        # Fallback
        return "deepseek-chat"
```

---

## Quotas Management

```python
DAILY_LIMITS = {
    "openai": 100.00,     # $100/jour
    "anthropic": 50.00,   # $50/jour
    "deepseek": 20.00,    # $20/jour
    "groq": 10.00,        # $10/jour
    "google": 30.00,      # $30/jour
}

async def check_quota(provider: str) -> bool:
    usage = await get_daily_usage(provider)
    return usage < DAILY_LIMITS[provider]
```

---

## MCP Tools

```yaml
tools:
  router_select_model:
    description: Sélectionne le modèle optimal
    input: { task_type: string, priority: "cost"|"balanced"|"quality" }
    output: { model: string, reason: string, estimated_cost: float }
  
  router_estimate_cost:
    description: Estime le coût d'une requête
    input: { model: string, input_tokens: number, output_tokens: number }
    output: { cost_usd: float, cost_dzd: float }
  
  router_check_quota:
    description: Vérifie les quotas restants
    input: { provider?: string }
    output: { quotas: object, warnings[] }
  
  router_get_stats:
    description: Statistiques d'utilisation
    input: { period: "day"|"week"|"month" }
    output: { total_cost, by_provider, by_task_type }
```

---

## Configuration IA Factory

```yaml
iafactory_routing:
  # Budget quotidien
  daily_budget_usd: 50.00
  
  # Préférer modèles locaux
  prefer_local: true
  local_models:
    - ollama/llama3.1
    - ollama/codellama
  
  # Fallback économique
  fallback: deepseek-chat
  
  # Alertes
  alert_at: 80%  # du budget
```
