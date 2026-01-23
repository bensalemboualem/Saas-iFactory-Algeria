import { AITool } from '../types';
import {
    emailSubjectLineGenerator, coldEmailGenerator, newsletterGenerator,
    emailSequenceGenerator, followUpEmailGenerator, promotionalEmailGenerator,
    welcomeEmailGenerator, emailCtaGenerator
} from './email/batch1-critical';

export const emailTools: AITool[] = [
    emailSubjectLineGenerator,
    coldEmailGenerator,
    newsletterGenerator,
    emailSequenceGenerator,
    followUpEmailGenerator,
    promotionalEmailGenerator,
    welcomeEmailGenerator,
    emailCtaGenerator
];
