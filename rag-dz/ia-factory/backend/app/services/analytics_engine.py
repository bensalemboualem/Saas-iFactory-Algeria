"""
IA Factory - Analytics Engine Service
Phase 4: Performance Analytics & AI Optimization
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from anthropic import Anthropic

from ..config import settings
from ..models.analytics import (
    PerformanceMetric,
    ContentPerformance,
    PillarPerformance,
    PlatformPerformance,
    AnalyticsReport,
    OptimizationSuggestion,
    ContentIdea,
    DashboardSummary,
    TimeRange
)

logger = logging.getLogger(__name__)


class AnalyticsEngine:
    """
    Phase 4: Analytics & Optimization Engine
    
    Aggregates performance data, generates insights,
    and provides AI-powered optimization recommendations.
    """
    
    def __init__(self, db):
        self.db = db
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.claude_model
    
    async def get_dashboard_summary(
        self,
        brand_id: str,
        days: int = 30
    ) -> DashboardSummary:
        """
        Get performance summary for dashboard
        
        Args:
            brand_id: Brand identifier
            days: Number of days to analyze
        
        Returns:
            Dashboard summary with key metrics
        """
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        prev_start = start_date - timedelta(days=days)
        
        # Get current period metrics
        current_metrics = await self.db.metrics.find({
            "brand_id": brand_id,
            "timestamp": {"$gte": start_date, "$lte": end_date}
        }).to_list(None)
        
        # Get previous period metrics
        prev_metrics = await self.db.metrics.find({
            "brand_id": brand_id,
            "timestamp": {"$gte": prev_start, "$lt": start_date}
        }).to_list(None)
        
        # Calculate totals
        current_views = sum(m.get('views', 0) for m in current_metrics)
        current_engagement = sum(
            m.get('likes', 0) + m.get('comments', 0) + m.get('shares', 0) + m.get('saves', 0)
            for m in current_metrics
        )
        
        prev_views = sum(m.get('views', 0) for m in prev_metrics) or 1
        prev_engagement = sum(
            m.get('likes', 0) + m.get('comments', 0) + m.get('shares', 0) + m.get('saves', 0)
            for m in prev_metrics
        ) or 1
        
        # Calculate changes
        views_change = ((current_views - prev_views) / prev_views) * 100
        engagement_change = ((current_engagement - prev_engagement) / prev_engagement) * 100
        
        # Engagement rate
        current_rate = (current_engagement / max(current_views, 1)) * 100
        prev_rate = (prev_engagement / max(prev_views, 1)) * 100
        rate_change = current_rate - prev_rate
        
        # Get scheduled posts count
        scheduled_posts = await self.db.scheduled_posts.count_documents({
            "brand_id": brand_id,
            "status": "scheduled"
        })
        
        # Find top post
        top_post = None
        if current_metrics:
            sorted_metrics = sorted(current_metrics, key=lambda x: x.get('views', 0), reverse=True)
            if sorted_metrics:
                top_post = sorted_metrics[0]
        
        # Generate AI insight
        ai_insight = await self._generate_quick_insight(
            current_views, current_engagement, current_rate,
            views_change, engagement_change
        )
        
        return DashboardSummary(
            brand_id=brand_id,
            current_period=f"Last {days} days",
            previous_period=f"Previous {days} days",
            views={
                "value": current_views,
                "change": round(views_change, 1),
                "trend": "up" if views_change > 0 else "down"
            },
            engagement={
                "value": current_engagement,
                "change": round(engagement_change, 1),
                "trend": "up" if engagement_change > 0 else "down"
            },
            engagement_rate={
                "value": round(current_rate, 2),
                "change": round(rate_change, 2),
                "trend": "up" if rate_change > 0 else "down"
            },
            followers={
                "value": sum(m.get('followers_gained', 0) for m in current_metrics),
                "change": 0
            },
            posts_this_period=len(current_metrics),
            posts_scheduled=scheduled_posts,
            top_post_thumbnail=top_post.get('thumbnail_url') if top_post else None,
            top_post_views=top_post.get('views', 0) if top_post else 0,
            ai_insight=ai_insight,
            last_updated=datetime.now()
        )
    
    async def _generate_quick_insight(
        self,
        views: int,
        engagement: int,
        rate: float,
        views_change: float,
        engagement_change: float
    ) -> str:
        """Generate a quick AI insight for the dashboard"""
        
        prompt = f"""
Generate a ONE sentence insight about this content performance:

Views: {views:,} ({views_change:+.1f}% change)
Engagement: {engagement:,} ({engagement_change:+.1f}% change)
Engagement Rate: {rate:.2f}%

Be specific, actionable, and encouraging. Focus on the most important trend.
Return ONLY the insight sentence.
"""
        
        try:
            response = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except:
            if views_change > 0:
                return f"Your content is growing! Views up {views_change:.1f}% this period."
            else:
                return "Consider experimenting with new content formats to boost engagement."
    
    async def get_content_performance(
        self,
        brand_id: str,
        content_id: str
    ) -> ContentPerformance:
        """Get detailed performance for a single content piece"""
        
        metrics = await self.db.metrics.find({
            "brand_id": brand_id,
            "content_id": content_id
        }).to_list(None)
        
        if not metrics:
            return None
        
        # Get content info
        content = await self.db.content.find_one({"_id": content_id})
        
        # Aggregate across platforms
        total_views = sum(m.get('views', 0) for m in metrics)
        total_engagement = sum(
            m.get('likes', 0) + m.get('comments', 0) + m.get('shares', 0) + m.get('saves', 0)
            for m in metrics
        )
        
        # Per-platform breakdown
        platform_metrics = {}
        for metric in metrics:
            platform = metric.get('platform', 'unknown')
            if platform not in platform_metrics:
                platform_metrics[platform] = PerformanceMetric(**metric)
        
        return ContentPerformance(
            content_id=content_id,
            title=content.get('title', '') if content else '',
            pillar_name=content.get('pillar_name', '') if content else '',
            published_at=content.get('published_at', datetime.now()) if content else datetime.now(),
            total_views=total_views,
            total_engagement=total_engagement,
            engagement_rate=(total_engagement / max(total_views, 1)) * 100,
            platform_metrics=platform_metrics,
            performance_score=self._calculate_performance_score(total_views, total_engagement)
        )
    
    def _calculate_performance_score(self, views: int, engagement: int) -> float:
        """Calculate a normalized performance score (0-100)"""
        # Simple scoring: weighted combination of views and engagement
        # This should be calibrated based on brand's typical performance
        view_score = min(views / 10000, 1) * 50  # 10K views = 50 points max
        engagement_score = min(engagement / 1000, 1) * 50  # 1K engagement = 50 points max
        return round(view_score + engagement_score, 1)
    
    async def get_pillar_performance(
        self,
        brand_id: str,
        time_range: TimeRange = TimeRange.MONTH
    ) -> List[PillarPerformance]:
        """Get performance aggregated by content pillar"""
        
        days = {
            TimeRange.DAY: 1,
            TimeRange.WEEK: 7,
            TimeRange.MONTH: 30,
            TimeRange.QUARTER: 90,
            TimeRange.YEAR: 365
        }.get(time_range, 30)
        
        start_date = datetime.now() - timedelta(days=days)
        
        # Get all content with metrics
        pipeline = [
            {"$match": {"brand_id": brand_id, "timestamp": {"$gte": start_date}}},
            {"$lookup": {
                "from": "content",
                "localField": "content_id",
                "foreignField": "_id",
                "as": "content_info"
            }},
            {"$unwind": "$content_info"},
            {"$group": {
                "_id": "$content_info.pillar_name",
                "total_posts": {"$sum": 1},
                "total_views": {"$sum": "$views"},
                "total_likes": {"$sum": "$likes"},
                "total_comments": {"$sum": "$comments"},
                "total_shares": {"$sum": "$shares"},
                "total_saves": {"$sum": "$saves"}
            }}
        ]
        
        results = await self.db.metrics.aggregate(pipeline).to_list(None)
        
        performances = []
        for result in results:
            total_engagement = (
                result.get('total_likes', 0) +
                result.get('total_comments', 0) +
                result.get('total_shares', 0) +
                result.get('total_saves', 0)
            )
            
            performances.append(PillarPerformance(
                pillar_name=result['_id'] or 'Unknown',
                brand_id=brand_id,
                total_posts=result.get('total_posts', 0),
                total_views=result.get('total_views', 0),
                total_engagement=total_engagement,
                avg_engagement_rate=(total_engagement / max(result.get('total_views', 1), 1)) * 100
            ))
        
        return performances
    
    async def get_platform_performance(
        self,
        brand_id: str,
        time_range: TimeRange = TimeRange.MONTH
    ) -> List[PlatformPerformance]:
        """Get performance aggregated by platform"""
        
        days = {
            TimeRange.DAY: 1,
            TimeRange.WEEK: 7,
            TimeRange.MONTH: 30,
            TimeRange.QUARTER: 90
        }.get(time_range, 30)
        
        start_date = datetime.now() - timedelta(days=days)
        
        pipeline = [
            {"$match": {"brand_id": brand_id, "timestamp": {"$gte": start_date}}},
            {"$group": {
                "_id": "$platform",
                "total_posts": {"$sum": 1},
                "total_views": {"$sum": "$views"},
                "total_likes": {"$sum": "$likes"},
                "total_comments": {"$sum": "$comments"},
                "total_shares": {"$sum": "$shares"},
                "total_saves": {"$sum": "$saves"},
                "followers_gained": {"$sum": "$followers_gained"}
            }}
        ]
        
        results = await self.db.metrics.aggregate(pipeline).to_list(None)
        
        performances = []
        for result in results:
            total_engagement = (
                result.get('total_likes', 0) +
                result.get('total_comments', 0) +
                result.get('total_shares', 0) +
                result.get('total_saves', 0)
            )
            
            performances.append(PlatformPerformance(
                platform=result['_id'] or 'unknown',
                brand_id=brand_id,
                total_posts=result.get('total_posts', 0),
                total_views=result.get('total_views', 0),
                total_engagement=total_engagement,
                avg_engagement_rate=(total_engagement / max(result.get('total_views', 1), 1)) * 100,
                followers_gained=result.get('followers_gained', 0)
            ))
        
        return performances
    
    async def get_ai_recommendations(
        self,
        brand_id: str,
        brand_guidelines: Dict[str, Any]
    ) -> List[OptimizationSuggestion]:
        """Get AI-powered optimization recommendations"""
        
        # Gather data
        summary = await self.get_dashboard_summary(brand_id, days=30)
        pillar_perf = await self.get_pillar_performance(brand_id)
        platform_perf = await self.get_platform_performance(brand_id)
        
        # Prepare data for Claude
        data_summary = {
            "total_views": summary.views.get('value', 0),
            "views_change": summary.views.get('change', 0),
            "engagement_rate": summary.engagement_rate.get('value', 0),
            "rate_change": summary.engagement_rate.get('change', 0),
            "posts_count": summary.posts_this_period,
            "pillars": [
                {
                    "name": p.pillar_name,
                    "posts": p.total_posts,
                    "views": p.total_views,
                    "engagement_rate": p.avg_engagement_rate
                }
                for p in pillar_perf
            ],
            "platforms": [
                {
                    "name": p.platform,
                    "posts": p.total_posts,
                    "views": p.total_views,
                    "engagement_rate": p.avg_engagement_rate
                }
                for p in platform_perf
            ]
        }
        
        prompt = f"""
Analyze this content performance data and provide optimization recommendations:

PERFORMANCE DATA:
{json.dumps(data_summary, indent=2)}

BRAND INFO:
- Name: {brand_guidelines.get('brand_name', 'Unknown')}
- Pillars: {[p.get('name') for p in brand_guidelines.get('content_pillars', [])]}
- Target Audience: {brand_guidelines.get('target_audience', 'General')}

Generate 5 specific, actionable recommendations as JSON:
{{
    "recommendations": [
        {{
            "category": "content|timing|hashtags|engagement|format",
            "title": "Short title (5-7 words)",
            "description": "Detailed recommendation with specific actions",
            "priority": "high|medium|low",
            "estimated_impact": "Expected improvement description",
            "action_type": "adjust_schedule|change_pillar_mix|try_new_format|etc"
        }}
    ]
}}

Focus on:
1. What's working well (double down)
2. What needs improvement
3. Quick wins
4. Long-term strategies
5. Platform-specific tactics
"""
        
        try:
            response = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            text = response.content[0].text
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            
            if json_start >= 0:
                data = json.loads(text[json_start:json_end])
                recommendations = data.get('recommendations', [])
                
                return [
                    OptimizationSuggestion(
                        brand_id=brand_id,
                        category=r.get('category', 'content'),
                        title=r.get('title', ''),
                        description=r.get('description', ''),
                        priority=r.get('priority', 'medium'),
                        estimated_impact=r.get('estimated_impact', ''),
                        action_type=r.get('action_type', ''),
                        confidence_score=0.8
                    )
                    for r in recommendations
                ]
            
        except Exception as e:
            logger.error(f"AI recommendations failed: {e}")
        
        # Default recommendations if AI fails
        return [
            OptimizationSuggestion(
                brand_id=brand_id,
                category="content",
                title="Analyze your top performing content",
                description="Review your best performing posts and identify common patterns",
                priority="high",
                estimated_impact="Better understanding of what resonates",
                action_type="analyze"
            )
        ]
    
    async def generate_content_ideas(
        self,
        brand_id: str,
        brand_guidelines: Dict[str, Any],
        count: int = 5
    ) -> List[ContentIdea]:
        """Generate AI-powered content ideas based on performance"""
        
        # Get top performing content
        top_metrics = await self.db.metrics.find({
            "brand_id": brand_id
        }).sort("views", -1).limit(10).to_list(None)
        
        # Get content details for top metrics
        top_topics = []
        for metric in top_metrics:
            content = await self.db.content.find_one({"_id": metric.get('content_id')})
            if content:
                top_topics.append(content.get('topic', ''))
        
        pillars = [p.get('name') for p in brand_guidelines.get('content_pillars', [])]
        
        prompt = f"""
Generate {count} content ideas for this brand:

BRAND: {brand_guidelines.get('brand_name', 'IA Factory')}
NICHE: {brand_guidelines.get('niche', 'Technology')}
PILLARS: {pillars}
TARGET AUDIENCE: {brand_guidelines.get('target_audience', 'Entrepreneurs')}

TOP PERFORMING TOPICS:
{top_topics[:5] if top_topics else ['No data yet']}

Generate fresh content ideas as JSON:
{{
    "ideas": [
        {{
            "topic": "Specific content topic",
            "hook": "Attention-grabbing opening line",
            "pillar": "Which pillar this belongs to",
            "why_suggested": "Why this will perform well",
            "trending_score": 0.8,
            "relevance_score": 0.9
        }}
    ]
}}

Ideas should be:
- Specific and actionable
- Aligned with top performing content patterns
- Fresh and timely
- Suitable for 15-second reels
"""
        
        try:
            response = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            text = response.content[0].text
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            
            if json_start >= 0:
                data = json.loads(text[json_start:json_end])
                ideas = data.get('ideas', [])
                
                return [
                    ContentIdea(
                        brand_id=brand_id,
                        topic=idea.get('topic', ''),
                        hook=idea.get('hook', ''),
                        pillar=idea.get('pillar', pillars[0] if pillars else 'General'),
                        why_suggested=idea.get('why_suggested', ''),
                        trending_score=idea.get('trending_score', 0.5),
                        relevance_score=idea.get('relevance_score', 0.5)
                    )
                    for idea in ideas
                ]
        
        except Exception as e:
            logger.error(f"Content idea generation failed: {e}")
        
        return []
    
    async def generate_full_report(
        self,
        brand_id: str,
        brand_guidelines: Dict[str, Any],
        time_range: TimeRange = TimeRange.MONTH
    ) -> AnalyticsReport:
        """Generate a comprehensive analytics report"""
        
        days = {
            TimeRange.WEEK: 7,
            TimeRange.MONTH: 30,
            TimeRange.QUARTER: 90
        }.get(time_range, 30)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Gather all data
        summary = await self.get_dashboard_summary(brand_id, days)
        pillar_perf = await self.get_pillar_performance(brand_id, time_range)
        platform_perf = await self.get_platform_performance(brand_id, time_range)
        recommendations = await self.get_ai_recommendations(brand_id, brand_guidelines)
        content_ideas = await self.generate_content_ideas(brand_id, brand_guidelines)
        
        # Get top and worst posts
        all_metrics = await self.db.metrics.find({
            "brand_id": brand_id,
            "timestamp": {"$gte": start_date}
        }).to_list(None)
        
        sorted_by_views = sorted(all_metrics, key=lambda x: x.get('views', 0), reverse=True)
        
        # Generate AI summary
        ai_summary = await self._generate_report_summary(
            summary, pillar_perf, platform_perf
        )
        
        return AnalyticsReport(
            brand_id=brand_id,
            time_range=time_range,
            start_date=start_date,
            end_date=end_date,
            total_posts=summary.posts_this_period,
            total_views=summary.views.get('value', 0),
            total_engagement=summary.engagement.get('value', 0),
            avg_engagement_rate=summary.engagement_rate.get('value', 0),
            followers_gained=summary.followers.get('value', 0),
            pillar_performance=pillar_perf,
            platform_performance=platform_perf,
            ai_summary=ai_summary,
            optimization_suggestions=recommendations,
            content_ideas=content_ideas,
            generated_at=datetime.now()
        )
    
    async def _generate_report_summary(
        self,
        summary: DashboardSummary,
        pillars: List[PillarPerformance],
        platforms: List[PlatformPerformance]
    ) -> str:
        """Generate AI summary for the report"""
        
        prompt = f"""
Write a brief executive summary (3-4 sentences) for this content performance report:

Views: {summary.views.get('value', 0):,} ({summary.views.get('change', 0):+.1f}%)
Engagement: {summary.engagement.get('value', 0):,} ({summary.engagement.get('change', 0):+.1f}%)
Engagement Rate: {summary.engagement_rate.get('value', 0):.2f}%

Top Pillar: {pillars[0].pillar_name if pillars else 'N/A'}
Top Platform: {platforms[0].platform if platforms else 'N/A'}

Be concise, highlight key wins and areas for improvement.
"""
        
        try:
            response = await asyncio.to_thread(
                self.client.messages.create,
                model=self.model,
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except:
            return f"This period saw {summary.views.get('value', 0):,} views with a {summary.engagement_rate.get('value', 0):.2f}% engagement rate."
