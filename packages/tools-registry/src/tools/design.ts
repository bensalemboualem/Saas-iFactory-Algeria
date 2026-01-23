import { AITool } from '../types';
import {
    midjourneyPromptGenerator,
    dallePromptGenerator,
    stableDiffusionPromptGenerator,
    imageAltTextGenerator,
    socialMediaImageIdeas,
    logoConceptGenerator,
    colorPaletteGenerator,
    uiComponentIdeas
} from './design/batch1-critical';
import {
    thumbnailIdeaGenerator, infographicOutlineGenerator, bannerAdConcept,
    productMockupIdeas, iconDescriptionGenerator, brandStyleGuideGenerator,
    imageCaptionGenerator
} from './design/batch2-high-priority';

export const designTools: AITool[] = [
    midjourneyPromptGenerator,
    dallePromptGenerator,
    stableDiffusionPromptGenerator,
    imageAltTextGenerator,
    socialMediaImageIdeas,
    logoConceptGenerator,
    colorPaletteGenerator,
    uiComponentIdeas,
    thumbnailIdeaGenerator,
    infographicOutlineGenerator,
    bannerAdConcept,
    productMockupIdeas,
    iconDescriptionGenerator,
    brandStyleGuideGenerator,
    imageCaptionGenerator
];
