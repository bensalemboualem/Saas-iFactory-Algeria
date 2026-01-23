import { AITool } from '../types';
import {
    businessPlanGenerator, pitchDeckGenerator, swotAnalysisGenerator,
    buyerPersonaGenerator, valuePropositionGenerator, competitiveAnalysisGenerator,
    executiveSummaryGenerator, meetingAgendaGenerator
} from './business/batch1-critical';
import {
    proposalGenerator, invoiceGenerator, contractTemplateGenerator, okrGenerator,
    kpiDashboardGenerator, projectBriefGenerator, companyDescriptionGenerator,
    missionVisionGenerator
} from './business/batch2-high-priority';
import {
    partnershipProposal, pressReleaseGenerator, jobDescriptionGenerator,
    onboardingChecklist
} from './business/batch3-medium-priority';

export const businessTools: AITool[] = [
    businessPlanGenerator,
    pitchDeckGenerator,
    swotAnalysisGenerator,
    buyerPersonaGenerator,
    valuePropositionGenerator,
    competitiveAnalysisGenerator,
    executiveSummaryGenerator,
    meetingAgendaGenerator,
    proposalGenerator,
    invoiceGenerator,
    contractTemplateGenerator,
    okrGenerator,
    kpiDashboardGenerator,
    projectBriefGenerator,
    companyDescriptionGenerator,
    missionVisionGenerator,
    partnershipProposal,
    pressReleaseGenerator,
    jobDescriptionGenerator,
    onboardingChecklist
];
