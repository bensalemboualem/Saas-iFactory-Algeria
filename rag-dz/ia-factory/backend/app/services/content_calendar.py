"""
IA Factory - Content Calendar Service
Phase 2: Content scheduling and calendar management
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pytz
import logging

from ..models.distribution import Platform

logger = logging.getLogger(__name__)


class ContentCalendar:
    """
    Phase 2: Content Calendar & Scheduling
    
    Creates and manages content posting schedules
    based on brand guidelines and optimal times.
    """
    
    def __init__(
        self,
        brand_guidelines: Dict[str, Any],
        timezone: str = "Africa/Algiers"
    ):
        self.brand = brand_guidelines
        self.pillars = brand_guidelines.get('content_pillars', [])
        self.timezone = pytz.timezone(timezone)
        
        # Get posting schedule from guidelines
        posting_schedule = brand_guidelines.get('posting_schedule', {})
        self.optimal_hours = posting_schedule.get('optimal_hours', [19, 20, 21])
        self.posting_days = posting_schedule.get('posting_days', [0, 1, 2, 3, 4, 5, 6])
        self.posts_per_day = posting_schedule.get('posts_per_day', 1)
    
    def create_monthly_schedule(
        self,
        num_videos: int = 30,
        start_date: Optional[datetime] = None,
        platforms: Optional[List[Platform]] = None
    ) -> List[Dict[str, Any]]:
        """
        Create a monthly posting schedule
        
        Args:
            num_videos: Number of videos to schedule
            start_date: Start date (defaults to today)
            platforms: Target platforms (defaults to Instagram Reels)
        
        Returns:
            List of scheduled content entries
        """
        
        if start_date is None:
            start_date = datetime.now(self.timezone)
        elif start_date.tzinfo is None:
            start_date = self.timezone.localize(start_date)
        
        if platforms is None:
            platforms = [Platform.INSTAGRAM_REELS]
        
        # Calculate pillar distribution
        pillar_distribution = self._calculate_pillar_distribution(num_videos)
        
        # Get posting times
        post_times = self._calculate_posting_times(num_videos, start_date)
        
        # Create schedule entries
        schedule = []
        video_idx = 0
        pillar_counts = {name: 0 for name in pillar_distribution.keys()}
        
        # Interleave pillars for variety
        while video_idx < num_videos and video_idx < len(post_times):
            for pillar_name, target_count in pillar_distribution.items():
                if pillar_counts[pillar_name] < target_count and video_idx < num_videos:
                    # Find pillar details
                    pillar_info = next(
                        (p for p in self.pillars if p.get('name') == pillar_name),
                        {'name': pillar_name, 'hashtags': []}
                    )
                    
                    entry = {
                        "id": f"schedule_{video_idx}",
                        "video_id": f"video_{video_idx}",
                        "pillar": pillar_name,
                        "pillar_color": self._get_pillar_color(pillar_name),
                        "scheduled_time": post_times[video_idx].isoformat(),
                        "scheduled_time_local": post_times[video_idx].strftime("%Y-%m-%d %H:%M"),
                        "day_of_week": post_times[video_idx].strftime("%A"),
                        "platforms": [p.value for p in platforms],
                        "default_hashtags": pillar_info.get('hashtags', []),
                        "status": "scheduled"
                    }
                    
                    schedule.append(entry)
                    pillar_counts[pillar_name] += 1
                    video_idx += 1
        
        logger.info(f"📅 Created schedule with {len(schedule)} posts")
        return schedule
    
    def _calculate_pillar_distribution(
        self,
        num_videos: int
    ) -> Dict[str, int]:
        """Calculate how many videos per pillar based on percentages"""
        
        distribution = {}
        
        if not self.pillars:
            # Default single pillar if none defined
            return {"General": num_videos}
        
        total_assigned = 0
        
        for pillar in self.pillars:
            name = pillar.get('name', 'Unknown')
            percentage = pillar.get('percentage_of_content', 0)
            count = int((percentage / 100) * num_videos)
            distribution[name] = count
            total_assigned += count
        
        # Distribute remaining videos
        remaining = num_videos - total_assigned
        if remaining > 0 and self.pillars:
            # Add to first pillar
            first_pillar = self.pillars[0].get('name')
            distribution[first_pillar] = distribution.get(first_pillar, 0) + remaining
        
        return distribution
    
    def _calculate_posting_times(
        self,
        num_videos: int,
        start_date: datetime
    ) -> List[datetime]:
        """
        Calculate optimal posting times
        
        Distributes posts across days at optimal hours.
        """
        
        times = []
        current_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        hour_index = 0
        
        while len(times) < num_videos:
            # Skip non-posting days
            if current_date.weekday() not in self.posting_days:
                current_date += timedelta(days=1)
                continue
            
            # Add posts for this day
            for _ in range(self.posts_per_day):
                if len(times) >= num_videos:
                    break
                
                hour = self.optimal_hours[hour_index % len(self.optimal_hours)]
                posting_time = current_date.replace(hour=hour, minute=0, second=0)
                
                # Ensure it's in the future
                if posting_time > datetime.now(self.timezone):
                    times.append(posting_time)
                
                hour_index += 1
            
            current_date += timedelta(days=1)
        
        return times
    
    def _get_pillar_color(self, pillar_name: str) -> str:
        """Get color for pillar (for UI display)"""
        
        colors = {
            "Education": "#3B82F6",      # Blue
            "Entertainment": "#F59E0B",  # Amber
            "Inspiration": "#10B981",    # Green
            "Behind-the-scenes": "#8B5CF6",  # Purple
            "Community": "#EC4899",      # Pink
            "News": "#EF4444",           # Red
            "Tutorial": "#06B6D4",       # Cyan
            "General": "#6B7280"         # Gray
        }
        
        return colors.get(pillar_name, "#6B7280")
    
    def get_calendar_view(
        self,
        schedule: List[Dict[str, Any]],
        view: str = "month"
    ) -> Dict[str, Any]:
        """
        Format schedule for calendar view
        
        Args:
            schedule: List of scheduled entries
            view: View type (month, week, day)
        
        Returns:
            Calendar-formatted data
        """
        
        # Group by date
        by_date = {}
        for entry in schedule:
            date_str = entry['scheduled_time'][:10]  # YYYY-MM-DD
            if date_str not in by_date:
                by_date[date_str] = []
            by_date[date_str].append(entry)
        
        # Calculate statistics
        stats = {
            "total_posts": len(schedule),
            "posts_by_pillar": {},
            "posts_by_day": {},
            "posts_by_platform": {}
        }
        
        for entry in schedule:
            # By pillar
            pillar = entry.get('pillar', 'Unknown')
            stats["posts_by_pillar"][pillar] = stats["posts_by_pillar"].get(pillar, 0) + 1
            
            # By day
            day = entry.get('day_of_week', 'Unknown')
            stats["posts_by_day"][day] = stats["posts_by_day"].get(day, 0) + 1
            
            # By platform
            for platform in entry.get('platforms', []):
                stats["posts_by_platform"][platform] = stats["posts_by_platform"].get(platform, 0) + 1
        
        return {
            "view": view,
            "entries": schedule,
            "by_date": by_date,
            "statistics": stats,
            "timezone": str(self.timezone)
        }
    
    def reschedule_post(
        self,
        schedule: List[Dict[str, Any]],
        post_id: str,
        new_time: datetime
    ) -> List[Dict[str, Any]]:
        """
        Reschedule a single post
        
        Args:
            schedule: Current schedule
            post_id: ID of post to reschedule
            new_time: New posting time
        
        Returns:
            Updated schedule
        """
        
        for entry in schedule:
            if entry['id'] == post_id:
                if new_time.tzinfo is None:
                    new_time = self.timezone.localize(new_time)
                
                entry['scheduled_time'] = new_time.isoformat()
                entry['scheduled_time_local'] = new_time.strftime("%Y-%m-%d %H:%M")
                entry['day_of_week'] = new_time.strftime("%A")
                entry['status'] = "rescheduled"
                break
        
        return schedule
    
    def get_upcoming_posts(
        self,
        schedule: List[Dict[str, Any]],
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """Get posts scheduled for the next N days"""
        
        now = datetime.now(self.timezone)
        cutoff = now + timedelta(days=days)
        
        upcoming = []
        for entry in schedule:
            try:
                scheduled = datetime.fromisoformat(entry['scheduled_time'])
                if now <= scheduled <= cutoff:
                    upcoming.append(entry)
            except:
                pass
        
        # Sort by time
        upcoming.sort(key=lambda x: x['scheduled_time'])
        
        return upcoming
