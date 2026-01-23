import { AITool } from '../types';
import {
    metaTagGenerator, keywordGenerator, longtailKeywordGenerator,
    metaDescriptionGenerator, seoContentOptimizer, competitorKeywordAnalyzer,
    schemaMarkupGenerator
} from './seo/seo-critical';

import {
    titleTagOptimizer, internalLinkingSuggester, urlSlugOptimizer,
    headingStructureAnalyzer, imageAltGenerator, contentGapAnalyzer,
    seoAuditChecklist, serpPreview
} from './seo/seo-high-priority';

import {
    readabilityScoreAnalyzer, keywordDensityChecker, anchorTextOptimizer,
    robotsTxtGenerator, sitemapGenerator
} from './seo/seo-medium-priority';

export const seoTools: AITool[] = [
    // Critical
    metaTagGenerator,
    keywordGenerator,
    longtailKeywordGenerator,
    metaDescriptionGenerator,
    seoContentOptimizer,
    competitorKeywordAnalyzer,
    schemaMarkupGenerator,

    // High Priority
    titleTagOptimizer,
    internalLinkingSuggester,
    urlSlugOptimizer,
    headingStructureAnalyzer,
    imageAltGenerator,
    contentGapAnalyzer,
    seoAuditChecklist,
    serpPreview,

    // Medium Priority
    readabilityScoreAnalyzer,
    keywordDensityChecker,
    anchorTextOptimizer,
    robotsTxtGenerator,
    sitemapGenerator
];
