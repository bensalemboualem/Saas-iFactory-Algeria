import { AITool } from '../types';
import { 
    youtubeTitleGenerator, youtubeDescriptionGenerator, youtubeTagsGenerator,
    youtubeScriptWriter, youtubeShortsScript, youtubeThumbnailIdeas,
    youtubeHookGenerator, youtubeSeoOptimizer, youtubeContentIdeas,
    youtubeIntroOutroScript
} from './youtube/batch1-critical';

import { 
    youtubeVideoOutline, youtubeCommentReply, youtubeCommunityPost,
    youtubePlaylistOptimizer, youtubeChannelAudit, youtubeMonetizationTips,
    youtubeCollabPitch, youtubeBrandDealEmail, youtubeEndScreenCta,
    youtubePollIdeas
} from './youtube/batch2-high-priority';

export const youtubeTools: AITool[] = [
    youtubeTitleGenerator,
    youtubeDescriptionGenerator,
    youtubeTagsGenerator,
    youtubeScriptWriter,
    youtubeShortsScript,
    youtubeThumbnailIdeas,
    youtubeHookGenerator,
    youtubeSeoOptimizer,
    youtubeContentIdeas,
    youtubeIntroOutroScript,
    youtubeVideoOutline,
    youtubeCommentReply,
    youtubeCommunityPost,
    youtubePlaylistOptimizer,
    youtubeChannelAudit,
    youtubeMonetizationTips,
    youtubeCollabPitch,
    youtubeBrandDealEmail,
    youtubeEndScreenCta,
    youtubePollIdeas
];
