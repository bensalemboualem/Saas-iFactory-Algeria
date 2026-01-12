"""
IAFactory - Billing API
========================
API complète pour gestion crédits, plans, et ROI
"""

from fastapi import FastAPI, HTTPException, Query, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json

from pricing_config import PLANS, CREDIT_COSTS, calculate_user_roi, export_plans_json
from feature_gating import FeatureGatingService, Feature, PLANS as FEATURE_PLANS
from providers_config import ProviderRouter, PROVIDERS, print_cost_comparison
from notifications import NotificationService, NotificationType

# ==============================================
# FASTAPI APP
# ==============================================

app = FastAPI(
    title="IAFactory Billing API",
    description="API de facturation et crédits IA",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Services
gating_service = FeatureGatingService()
provider_router = ProviderRouter()
notification_service = NotificationService()

# ==============================================
# MODELS
# ==============================================

class UsageRecord(BaseModel):
    user_id: str
    action: str  # chat_message, voice_minute, doc_contract, etc.
    credits_used: int
    metadata: Optional[Dict] = None

class CreditPurchase(BaseModel):
    user_id: str
    amount: int
    payment_method: str  # stripe, chargily, etc.

class PlanUpgrade(BaseModel):
    user_id: str
    new_plan_id: str
    payment_method: str

# ==============================================
# MOCK DATABASE (Replace with real DB)
# ==============================================

# In-memory user data (replace with PostgreSQL/Supabase)
USERS_DB: Dict[str, Dict] = {
    "demo_user": {
        "plan_id": "dz_pro",
        "credits_remaining": 847,
        "credits_total": 1000,
        "region": "dz",
        "usage_history": [],
        "created_at": datetime.utcnow() - timedelta(days=30),
        "renewal_date": datetime.utcnow() + timedelta(days=5),
    }
}

# ==============================================
# ENDPOINTS - PLANS
# ==============================================

@app.get("/api/plans")
async def get_plans(region: str = Query("dz", description="dz or ch")):
    """Retourne les plans disponibles pour une région"""
    plans_json = export_plans_json()

    # Filter by region
    if region == "dz":
        filtered = {k: v for k, v in plans_json.items() if k.startswith("dz_") or k == "digital_twin"}
    elif region == "ch":
        filtered = {k: v for k, v in plans_json.items() if k.startswith("ch_") or k == "digital_twin"}
    else:
        filtered = plans_json

    return {
        "region": region,
        "plans": filtered,
        "currency": "DZD" if region == "dz" else "CHF"
    }

@app.get("/api/plans/{plan_id}")
async def get_plan_details(plan_id: str):
    """Détails d'un plan spécifique"""
    plans_json = export_plans_json()
    plan = plans_json.get(plan_id)

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # Add features list
    feature_plan = FEATURE_PLANS.get(plan_id)
    if feature_plan:
        plan["features_list"] = [f.value for f in feature_plan.features]

    return plan

# ==============================================
# ENDPOINTS - CREDITS
# ==============================================

@app.get("/api/credits/{user_id}")
async def get_user_credits(user_id: str):
    """Retourne les crédits d'un utilisateur"""
    user = USERS_DB.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    plan = PLANS.get(user["plan_id"])

    return {
        "user_id": user_id,
        "plan_id": user["plan_id"],
        "plan_name": plan.name if plan else "Unknown",
        "credits": {
            "remaining": user["credits_remaining"],
            "total": user["credits_total"],
            "percent": round((user["credits_remaining"] / user["credits_total"]) * 100, 1)
        },
        "renewal_date": user.get("renewal_date", datetime.utcnow()).isoformat(),
        "low_credits_alert": user["credits_remaining"] < (user["credits_total"] * 0.1)
    }

@app.post("/api/credits/consume")
async def consume_credits(record: UsageRecord):
    """Consomme des crédits pour une action"""
    user = USERS_DB.get(record.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check sufficient credits
    credits_needed = CREDIT_COSTS.get(record.action, record.credits_used)
    if user["credits_remaining"] < credits_needed:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "insufficient_credits",
                "message": {
                    "fr": f"Crédits insuffisants. {credits_needed} requis, {user['credits_remaining']} disponibles.",
                    "ar": f"رصيد غير كافٍ. مطلوب {credits_needed}، متوفر {user['credits_remaining']}.",
                    "en": f"Insufficient credits. {credits_needed} required, {user['credits_remaining']} available."
                },
                "required": credits_needed,
                "available": user["credits_remaining"],
                "action_url": "/pricing"
            }
        )

    # Deduct credits
    user["credits_remaining"] -= credits_needed
    user["usage_history"].append({
        "action": record.action,
        "credits": credits_needed,
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": record.metadata
    })

    # Check for notifications
    await notification_service.check_and_notify(record.user_id, {
        "plan_id": user["plan_id"],
        "credits_remaining": user["credits_remaining"],
        "credits_total": user["credits_total"],
    })

    return {
        "success": True,
        "credits_consumed": credits_needed,
        "credits_remaining": user["credits_remaining"],
        "action": record.action
    }

@app.get("/api/credits/costs")
async def get_credit_costs():
    """Retourne les coûts en crédits par action"""
    return {
        "costs": CREDIT_COSTS,
        "categories": {
            "chat": ["chat_message", "rag_query", "rag_complex"],
            "voice": ["voice_minute", "voice_call", "voice_agent"],
            "video": ["video_short", "video_standard", "video_long"],
            "documents": ["doc_contract", "doc_legal", "doc_invoice", "doc_report"],
            "workflows": ["workflow_simple", "workflow_complex", "workflow_agent"]
        }
    }

# ==============================================
# ENDPOINTS - ROI DASHBOARD
# ==============================================

@app.get("/api/roi/{user_id}")
async def get_user_roi(user_id: str):
    """Calcule le ROI d'un utilisateur"""
    user = USERS_DB.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Aggregate usage
    usage = {}
    for record in user.get("usage_history", []):
        action = record["action"]
        usage[action] = usage.get(action, 0) + 1

    roi = calculate_user_roi(usage)
    plan = PLANS.get(user["plan_id"])

    return {
        "user_id": user_id,
        "period": "this_month",
        "roi": roi,
        "investment": {
            "plan_cost_chf": plan.price_chf if plan else 0,
            "overage_cost_chf": 0  # TODO: Calculate overage
        },
        "multiplier": round(roi["money_saved_chf"] / max(plan.price_chf, 1), 1) if plan else 0,
        "usage_breakdown": usage
    }

# ==============================================
# ENDPOINTS - FEATURE GATING
# ==============================================

@app.get("/api/features/check")
async def check_feature(
    user_id: str = Query(...),
    feature: str = Query(...)
):
    """Vérifie l'accès à une fonctionnalité"""
    user = USERS_DB.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        feature_enum = Feature(feature)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unknown feature: {feature}")

    result = gating_service.check_feature_access(user["plan_id"], feature_enum)

    if not result["allowed"]:
        response = gating_service.generate_gate_response(
            feature_enum,
            allowed=False,
            upgrade_plan=result["upgrade_plan"]
        )
        return {"allowed": False, **response}

    return {"allowed": True, "feature": feature}

@app.get("/api/features/user/{user_id}")
async def get_user_features(user_id: str):
    """Liste les fonctionnalités disponibles pour un utilisateur"""
    user = USERS_DB.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    features = gating_service.get_plan_features(user["plan_id"])

    return {
        "user_id": user_id,
        "plan_id": user["plan_id"],
        "features": features,
        "upgrade_suggestions": gating_service.get_upgrade_suggestions(user["plan_id"])
    }

# ==============================================
# ENDPOINTS - PROVIDERS
# ==============================================

@app.get("/api/providers")
async def get_providers():
    """Liste les providers LLM disponibles"""
    providers_list = []
    for name, provider in PROVIDERS.items():
        if provider.active:
            providers_list.append({
                "id": name,
                "name": provider.display_name,
                "models": provider.models,
                "cost": {
                    "input": provider.input_cost,
                    "output": provider.output_cost
                },
                "speed": provider.speed,
                "region": provider.region,
                "features": provider.features
            })

    # Sort by cost
    providers_list.sort(key=lambda p: p["cost"]["input"] + p["cost"]["output"])

    return {
        "providers": providers_list,
        "cheapest": providers_list[0]["id"] if providers_list else None,
        "recommended": {
            "dz": "mimo_v2_flash",
            "ch": "apertus_swiss",
            "speed": "groq_llama",
            "quality": "anthropic_claude"
        }
    }

@app.get("/api/providers/recommend")
async def recommend_provider(
    region: str = Query("global"),
    budget: str = Query("low"),
    task: str = Query("chat"),
    speed_priority: bool = Query(False)
):
    """Recommande le meilleur provider"""
    best = provider_router.get_best_provider(task, region, budget, speed_priority)

    return {
        "recommended": {
            "id": best.name,
            "name": best.display_name,
            "cost": f"${best.input_cost + best.output_cost:.2f}/1M tokens",
            "speed": f"{best.speed} tok/s",
            "reason": f"Optimal pour {region}, budget {budget}"
        }
    }

# ==============================================
# ENDPOINTS - NOTIFICATIONS
# ==============================================

@app.get("/api/notifications/{user_id}")
async def get_notifications(
    user_id: str,
    lang: str = Query("fr"),
    limit: int = Query(20)
):
    """Récupère les notifications d'un utilisateur"""
    user = USERS_DB.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate notifications based on current state
    notifications = await notification_service.check_and_notify(user_id, {
        "plan_id": user["plan_id"],
        "credits_remaining": user["credits_remaining"],
        "credits_total": user["credits_total"],
        "renewal_date": user.get("renewal_date"),
    })

    return {
        "notifications": [
            {
                "type": n.type.value,
                "title": n.title.get(lang, n.title.get("fr")),
                "message": n.message.get(lang, n.message.get("fr")),
                "action_url": n.action_url,
                "priority": n.priority
            }
            for n in notifications
        ],
        "count": len(notifications)
    }

# ==============================================
# HEALTH CHECK
# ==============================================

@app.get("/api/billing/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "billing-api",
        "version": "1.0.0",
        "providers": len([p for p in PROVIDERS.values() if p.active]),
        "plans": len(PLANS)
    }

# ==============================================
# RUN
# ==============================================

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("IAFactory Billing API")
    print("=" * 60)
    print_cost_comparison()
    print("\nStarting server on http://0.0.0.0:8230")
    uvicorn.run(app, host="0.0.0.0", port=8230)
