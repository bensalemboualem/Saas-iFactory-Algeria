"""
IA Factory - Brand API
Phase 1: Brand Configuration & Team Management
"""

from fastapi import APIRouter, HTTPException, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from typing import List, Optional

from ..database import get_db, Collections
from ..models.brand import (
    BrandVoice, 
    ContentPillar, 
    BrandGuidelines,
    UserProfile,
    UserRole,
    get_permissions_for_role
)

router = APIRouter(tags=["Brand Configuration"])


# =============================================================================
# BRAND SETUP
# =============================================================================

@router.post("/setup", response_model=dict, status_code=status.HTTP_201_CREATED)
async def setup_brand(
    brand_voice: BrandVoice,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Phase 1: Setup brand voice and configuration
    
    This is the first step in creating a brand. It defines the brand's
    voice, tone, target audience, and key values.
    """
    
    # Check if brand already exists
    existing = await db[Collections.BRANDS].find_one({
        "brand_name": brand_voice.brand_name
    })
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Brand '{brand_voice.brand_name}' already exists"
        )
    
    # Create brand document
    brand_doc = {
        **brand_voice.model_dump(),
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_active": True,
        "content_pillars": [],
        "niche": "Technology",
        "featured_topic": None
    }
    
    result = await db[Collections.BRANDS].insert_one(brand_doc)
    
    return {
        "status": "success",
        "brand_id": str(result.inserted_id),
        "brand_name": brand_voice.brand_name,
        "message": "Brand voice configured successfully. Next: Add content pillars."
    }


@router.get("/{brand_id}", response_model=dict)
async def get_brand(
    brand_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get brand details by ID"""
    
    try:
        brand = await db[Collections.BRANDS].find_one({
            "_id": ObjectId(brand_id)
        })
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid brand ID format")
    
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    brand["_id"] = str(brand["_id"])
    return brand


@router.put("/{brand_id}", response_model=dict)
async def update_brand(
    brand_id: str,
    brand_voice: BrandVoice,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update brand configuration"""
    
    try:
        result = await db[Collections.BRANDS].update_one(
            {"_id": ObjectId(brand_id)},
            {
                "$set": {
                    **brand_voice.model_dump(),
                    "updated_at": datetime.now()
                }
            }
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid brand ID format")
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    return {
        "status": "success",
        "message": "Brand updated successfully"
    }


# =============================================================================
# CONTENT PILLARS
# =============================================================================

@router.post("/{brand_id}/pillars", response_model=dict)
async def create_content_pillars(
    brand_id: str,
    pillars: List[ContentPillar],
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Phase 1: Define content pillars for the brand
    
    Content pillars define the categories of content and their distribution.
    The percentages must total 100%.
    """
    
    # Validate brand exists
    brand = await db[Collections.BRANDS].find_one({"_id": ObjectId(brand_id)})
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    # Validate percentages sum to 100
    total_percentage = sum(p.percentage_of_content for p in pillars)
    if total_percentage != 100:
        raise HTTPException(
            status_code=400,
            detail=f"Percentages must total 100%, got {total_percentage}%"
        )
    
    # Create pillar documents
    pillar_docs = []
    for pillar in pillars:
        pillar_doc = {
            **pillar.model_dump(),
            "brand_id": brand_id,
            "created_at": datetime.now()
        }
        pillar_docs.append(pillar_doc)
    
    # Delete existing pillars for this brand
    await db[Collections.PILLARS].delete_many({"brand_id": brand_id})
    
    # Insert new pillars
    result = await db[Collections.PILLARS].insert_many(pillar_docs)
    
    # Update brand with pillar references
    pillar_names = [p.name for p in pillars]
    await db[Collections.BRANDS].update_one(
        {"_id": ObjectId(brand_id)},
        {
            "$set": {
                "content_pillars": pillar_names,
                "updated_at": datetime.now()
            }
        }
    )
    
    return {
        "status": "success",
        "count": len(result.inserted_ids),
        "pillars": pillar_names,
        "message": f"Created {len(pillar_docs)} content pillars"
    }


@router.get("/{brand_id}/pillars", response_model=List[dict])
async def get_content_pillars(
    brand_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get all content pillars for a brand"""
    
    pillars = await db[Collections.PILLARS].find({
        "brand_id": brand_id
    }).to_list(None)
    
    for pillar in pillars:
        pillar["_id"] = str(pillar["_id"])
    
    return pillars


@router.put("/{brand_id}/pillars/{pillar_name}", response_model=dict)
async def update_pillar(
    brand_id: str,
    pillar_name: str,
    pillar: ContentPillar,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update a specific content pillar"""
    
    result = await db[Collections.PILLARS].update_one(
        {"brand_id": brand_id, "name": pillar_name},
        {"$set": pillar.model_dump()}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pillar not found")
    
    return {"status": "success", "message": "Pillar updated"}


# =============================================================================
# BRAND GUIDELINES (Complete)
# =============================================================================

@router.get("/{brand_id}/guidelines", response_model=dict)
async def get_brand_guidelines(
    brand_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Get complete brand guidelines for content generation
    
    Returns brand voice + content pillars + visual guidelines
    """
    
    brand = await db[Collections.BRANDS].find_one({"_id": ObjectId(brand_id)})
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    pillars = await db[Collections.PILLARS].find({
        "brand_id": brand_id
    }).to_list(None)
    
    brand["_id"] = str(brand["_id"])
    for pillar in pillars:
        pillar["_id"] = str(pillar["_id"])
    
    return {
        "brand": brand,
        "pillars": pillars,
        "total_pillars": len(pillars)
    }


# =============================================================================
# TEAM MANAGEMENT
# =============================================================================

@router.post("/{brand_id}/team/invite", response_model=dict)
async def invite_team_member(
    brand_id: str,
    email: str,
    role: UserRole,
    name: Optional[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Phase 1: Team Collaboration - Invite user to brand
    
    Roles:
    - admin: Full access
    - manager: Create, edit, schedule, invite creators
    - creator: Create and edit own content
    - viewer: View only access
    """
    
    # Validate brand exists
    brand = await db[Collections.BRANDS].find_one({"_id": ObjectId(brand_id)})
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    # Check if user already exists for this brand
    existing = await db[Collections.USERS].find_one({
        "email": email,
        "brand_id": brand_id
    })
    
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"User {email} already exists for this brand"
        )
    
    # Create user profile
    user = UserProfile(
        email=email,
        name=name or email.split("@")[0],
        role=role,
        brand_id=brand_id,
        permissions=get_permissions_for_role(role)
    )
    
    result = await db[Collections.USERS].insert_one(user.model_dump())
    
    # TODO: Send invitation email
    
    return {
        "status": "success",
        "user_id": str(result.inserted_id),
        "email": email,
        "role": role.value,
        "message": f"Invited {email} as {role.value}"
    }


@router.get("/{brand_id}/team", response_model=List[dict])
async def get_team_members(
    brand_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get all team members for a brand"""
    
    users = await db[Collections.USERS].find({
        "brand_id": brand_id
    }).to_list(None)
    
    for user in users:
        user["_id"] = str(user["_id"])
    
    return users


@router.put("/{brand_id}/team/{user_id}/role", response_model=dict)
async def update_user_role(
    brand_id: str,
    user_id: str,
    new_role: UserRole,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update a team member's role"""
    
    new_permissions = get_permissions_for_role(new_role)
    
    result = await db[Collections.USERS].update_one(
        {"_id": ObjectId(user_id), "brand_id": brand_id},
        {
            "$set": {
                "role": new_role.value,
                "permissions": new_permissions.model_dump()
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "status": "success",
        "message": f"Role updated to {new_role.value}"
    }


@router.delete("/{brand_id}/team/{user_id}", response_model=dict)
async def remove_team_member(
    brand_id: str,
    user_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Remove a team member from the brand"""
    
    result = await db[Collections.USERS].delete_one({
        "_id": ObjectId(user_id),
        "brand_id": brand_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "status": "success",
        "message": "Team member removed"
    }


# =============================================================================
# FEATURED TOPIC
# =============================================================================

@router.put("/{brand_id}/featured-topic", response_model=dict)
async def set_featured_topic(
    brand_id: str,
    topic: str,
    niche: Optional[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """
    Set the featured topic for content generation
    
    This topic will be expanded into 30 variations for bulk content creation.
    """
    
    update_data = {
        "featured_topic": topic,
        "updated_at": datetime.now()
    }
    
    if niche:
        update_data["niche"] = niche
    
    result = await db[Collections.BRANDS].update_one(
        {"_id": ObjectId(brand_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Brand not found")
    
    return {
        "status": "success",
        "featured_topic": topic,
        "message": "Featured topic set. Ready for bulk content generation."
    }
