import { AITool } from '../types';
import { 
    instagramCaptionGenerator, instagramHashtagGenerator, tiktokCaptionGenerator,
    linkedinPostGenerator, twitterThreadGenerator, facebookPostGenerator,
    socialMediaCalendar, instagramBioGenerator, socialMediaAdCopy,
    reelsScriptGenerator, pinterestPinGenerator, socialMediaAudit
} from './social/batch1-critical';

import {
    linkedinHeadlineGenerator, linkedinSummaryGenerator, twitterBioGenerator,
    tiktokHashtagGenerator, instagramStoryIdeas, socialProofGenerator,
    ugcBriefGenerator, influencerOutreachEmail, socialMediaReport,
    contentRepurposePlanner, viralHookGenerator, engagementResponseTemplates
} from './social/batch2-high-priority';

import {
    facebookGroupPost, linkedinArticleOutline, socialContestGenerator,
    whatsappBroadcastMessage, telegramChannelPost, discordAnnouncement
} from './social/batch3-medium-priority';

export const socialTools: AITool[] = [
    instagramCaptionGenerator,
    instagramHashtagGenerator,
    tiktokCaptionGenerator,
    linkedinPostGenerator,
    twitterThreadGenerator,
    facebookPostGenerator,
    socialMediaCalendar,
    instagramBioGenerator,
    socialMediaAdCopy,
    reelsScriptGenerator,
    pinterestPinGenerator,
    socialMediaAudit,
    linkedinHeadlineGenerator,
    linkedinSummaryGenerator,
    twitterBioGenerator,
    tiktokHashtagGenerator,
    instagramStoryIdeas,
    socialProofGenerator,
    ugcBriefGenerator,
    influencerOutreachEmail,
    socialMediaReport,
    contentRepurposePlanner,
    viralHookGenerator,
    engagementResponseTemplates,
    facebookGroupPost,
    linkedinArticleOutline,
    socialContestGenerator,
    whatsappBroadcastMessage,
    telegramChannelPost,
    discordAnnouncement
];
