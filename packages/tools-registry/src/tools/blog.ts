import { AITool } from '../types';
import { aiBlogWriter } from './blog/ai-blog-writer';
import { humanWrittenBlog } from './blog/human-written-blog';
import { aiHumanizer } from './blog/ai-humanizer';
import { blogTitleGenerator } from './blog/blog-title-generator';
import { blogOutlineGenerator } from './blog/blog-outline-generator';
import { blogTopicGenerator } from './blog/blog-topic-generator';
import { articleRewriter } from './blog/article-rewriter';
import { paraphrasingTool } from './blog/paraphrasing-tool';
import { summaryGenerator } from './blog/summary-generator';
import { oneClickBlog } from './blog/one-click-blog';

// Batch 2 Imports
import {
    blogIntroduction, blogConclusion, listicleGenerator, howToGuide,
    comparisonArticle, reviewArticle, caseStudyWriter, faqArticleGenerator
} from './blog/batch2-writing';

import {
    paragraphGenerator, contentExpander, blogSectionWriter,
    contentBriefGenerator, pillarContent, newsArticleWriter, blogIdeasFromUrl
} from './blog/batch2-optimization';

// Batch 3 Imports
import {
    blogIntroHook, textCompleter, bulletPointGenerator,
    prosConsGenerator, faqAnswers
} from './blog/batch3-writing';

import { toneChanger, sentenceRewriter } from './blog/batch3-rewriting';

import { blogMetaDescription, grammarChecker, keywordExtractor } from './blog/batch3-optimization';

export const blogTools: AITool[] = [
    // Batch 1
    aiBlogWriter,
    humanWrittenBlog,
    aiHumanizer,
    blogTitleGenerator,
    blogOutlineGenerator,
    blogTopicGenerator,
    articleRewriter,
    paraphrasingTool,
    summaryGenerator,
    oneClickBlog,

    // Batch 2 - Writing
    blogIntroduction,
    blogConclusion,
    listicleGenerator,
    howToGuide,
    comparisonArticle,
    reviewArticle,
    caseStudyWriter,
    faqArticleGenerator,

    // Batch 2 - Optimization & Ideation
    paragraphGenerator,
    contentExpander,
    blogSectionWriter,
    contentBriefGenerator,
    pillarContent,
    newsArticleWriter,
    blogIdeasFromUrl,

    // Batch 3 - Writing
    blogIntroHook,
    textCompleter,
    bulletPointGenerator,
    prosConsGenerator,
    faqAnswers,

    // Batch 3 - Rewriting
    toneChanger,
    sentenceRewriter,

    // Batch 3 - Optimization
    blogMetaDescription,
    grammarChecker,
    keywordExtractor
];
