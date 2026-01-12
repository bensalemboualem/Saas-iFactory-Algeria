"""
IA Factory - Analytics Models
Phase 4: Analytics & Optimization
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class MetricType(str, Enum):
    """Types of metrics tracked"""
    VIEWS = "views"
    LIKES = "likes"
    COMMENTS = "comments"
    SHARES = "shares"
    SAVES = "saves"
    REACH = "reach"
    IMPRESSIONS = "impressions"
    ENGAGEMENT_RATE = "engagement_rate"
    WATCH_TIME = "watch_time"
    FOLLOWERS_GAINED = "followers_gained"
    PROFILE_VISITS = "profile_visits"
    WEBSITE_CLICKS = "website_clicks"


class TimeRange(str, Enum):
    """Time range for analytics"""
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"
    ALL_TIME = "all_time"


class PerformanceMetric(BaseModel):
    """Individual performance metric"""
    
    id: Optional[str] = Field(None)
    brand_id: str = Field(...)
    content_id: str = Field(...)
    platform: str = Field(...)
    
    # Metrics
    views: int = Field(default=0)
    likes: int = Field(default=0)
    comments: int = Field(default=0)
    shares: int = Field(default=0)
    saves: int = Field(default=0)
    reach: int = Field(default=0)
    impressions: int = Field(default=0)
    
    # Calculated metrics
    engagement_rate: float = Field(default=0.0)
    watch_time_seconds: float = Field(default=0.0)
    avg_watch_percentage: float = Field(default=0.0)
    
    # Growth metrics
    followers_gained: int = Field(default=0)
    profile_visits: int = Field(default=0)
    website_clicks: int = Field(default=0)
    
    # Metadata
    timestamp: datetime = Field(default_factory=datetime.now)
    published_at: Optional[datetime] = Field(None)
    
    def calculate_engagement_rate(self) -> float:
        """Calculate engagement rate"""
        total_engagement = self.likes + self.comments + self.shares + self.saves
        if self.views > 0:
            return (total_engagement / self.views) * 100
        return 0.0


class ContentPerformance(BaseModel):
    """Performance data for a single content piece"""
    
    content_id: str = Field(...)
    title: str = Field(...)
    pillar_name: str = Field(...)
    published_at: datetime = Field(...)
    
    # Aggregated metrics across platforms
    total_views: int = Field(default=0)
    total_engagement: int = Field(default=0)
    engagement_rate: float = Field(default=0.0)
    
    # Per-platform breakdown
    platform_metrics: Dict[str, PerformanceMetric] = Field(default={})
    
    # Rankings
    performance_score: float = Field(default=0.0)
    rank_in_period: int = Field(default=0)


class PillarPerformance(BaseModel):
    """Performance aggregated by content pillar"""
    
    pillar_name: str = Field(...)
    brand_id: str = Field(...)
    
    # Metrics
    total_posts: int = Field(default=0)
    total_views: int = Field(default=0)
    total_engagement: int = Field(default=0)
    avg_engagement_rate: float = Field(default=0.0)
    
    # Best performing
    top_content: List[ContentPerformance] = Field(default=[])
    
    # Recommendations
    recommended_percentage: int = Field(default=0)
    current_percentage: int = Field(default=0)


class PlatformPerformance(BaseModel):
    """Performance aggregated by platform"""
    
    platform: str = Field(...)
    brand_id: str = Field(...)
    
    # Metrics
    total_posts: int = Field(default=0)
    total_views: int = Field(default=0)
    total_engagement: int = Field(default=0)
    avg_engagement_rate: float = Field(default=0.0)
    
    # Growth
    followers_total: int = Field(default=0)
    followers_gained: int = Field(default=0)
    growth_rate: float = Field(default=0.0)
    
    # Best times
    best_posting_times: List[str] = Field(default=[])
    best_posting_days: List[str] = Field(default=[])


class TrendAnalysis(BaseModel):
    """Trend analysis over time"""
    
    metric: MetricType
    time_range: TimeRange
    
    # Data points
    data_points: List[Dict[str, Any]] = Field(default=[])
    
    # Trend info
    trend_direction: str = Field(default="stable")  # up, down, stable
    percent_change: float = Field(default=0.0)
    
    # Forecasting
    predicted_next_period: Optional[float] = Field(None)


class OptimizationSuggestion(BaseModel):
    """AI-generated optimization suggestion"""
    
    id: Optional[str] = Field(None)
    brand_id: str = Field(...)
    
    # Suggestion
    category: str = Field(...)  # content, timing, hashtags, engagement
    title: str = Field(...)
    description: str = Field(...)
    priority: str = Field(default="medium")  # high, medium, low
    
    # Impact prediction
    estimated_impact: str = Field(default="")
    confidence_score: float = Field(default=0.0, ge=0, le=1)
    
    # Action
    actionable: bool = Field(default=True)
    action_type: str = Field(default="")  # adjust_schedule, change_pillar_mix, etc.
    action_params: Dict[str, Any] = Field(default={})
    
    # Status
    implemented: bool = Field(default=False)
    implemented_at: Optional[datetime] = Field(None)
    result_observed: Optional[str] = Field(None)
    
    # Metadata
    generated_at: datetime = Field(default_factory=datetime.now)


class ContentIdea(BaseModel):
    """AI-suggested content idea"""
    
    id: Optional[str] = Field(None)
    brand_id: str = Field(...)
    
    # Content idea
    topic: str = Field(...)
    hook: str = Field(...)
    pillar: str = Field(...)
    format: str = Field(default="reel")
    
    # Context
    why_suggested: str = Field(...)
    trending_score: float = Field(default=0.0, ge=0, le=1)
    relevance_score: float = Field(default=0.0, ge=0, le=1)
    
    # Status
    used: bool = Field(default=False)
    used_at: Optional[datetime] = Field(None)
    
    # Metadata
    generated_at: datetime = Field(default_factory=datetime.now)


class AnalyticsReport(BaseModel):
    """Complete analytics report"""
    
    id: Optional[str] = Field(None)
    brand_id: str = Field(...)
    
    # Time period
    time_range: TimeRange
    start_date: datetime
    end_date: datetime
    
    # Summary metrics
    total_posts: int = Field(default=0)
    total_views: int = Field(default=0)
    total_engagement: int = Field(default=0)
    avg_engagement_rate: float = Field(default=0.0)
    followers_gained: int = Field(default=0)
    
    # Breakdowns
    pillar_performance: List[PillarPerformance] = Field(default=[])
    platform_performance: List[PlatformPerformance] = Field(default=[])
    
    # Top content
    top_posts: List[ContentPerformance] = Field(default=[])
    worst_posts: List[ContentPerformance] = Field(default=[])
    
    # Trends
    trends: Dict[str, TrendAnalysis] = Field(default={})
    
    # AI Insights
    ai_summary: str = Field(default="")
    what_worked: List[str] = Field(default=[])
    what_needs_improvement: List[str] = Field(default=[])
    
    # Recommendations
    optimization_suggestions: List[OptimizationSuggestion] = Field(default=[])
    content_ideas: List[ContentIdea] = Field(default=[])
    
    # Optimal times discovered
    best_posting_times: Dict[str, List[str]] = Field(default={})
    
    # Metadata
    generated_at: datetime = Field(default_factory=datetime.now)


class DashboardSummary(BaseModel):
    """Dashboard summary for quick overview"""
    
    brand_id: str = Field(...)
    
    # Period comparison
    current_period: str = Field(...)
    previous_period: str = Field(...)
    
    # Key metrics with change
    views: Dict[str, Any] = Field(default={"value": 0, "change": 0})
    engagement: Dict[str, Any] = Field(default={"value": 0, "change": 0})
    engagement_rate: Dict[str, Any] = Field(default={"value": 0, "change": 0})
    followers: Dict[str, Any] = Field(default={"value": 0, "change": 0})
    
    # Quick stats
    posts_this_period: int = Field(default=0)
    posts_scheduled: int = Field(default=0)
    
    # Top performing
    top_post_thumbnail: Optional[str] = Field(None)
    top_post_views: int = Field(default=0)
    
    # AI insight of the day
    ai_insight: str = Field(default="")
    
    # Metadata
    last_updated: datetime = Field(default_factory=datetime.now)
