import { AITool } from '../types';
import { 
    cnasAssistant, casnosSimulator, impotsDzAssistant, cnrcAssistant,
    sonelgazAssistant, seaalAssistant, cnrRetraiteAssistant,
    anemEmploiAssistant, ansejCnacAssistant, passeportCniAssistant
} from './admin-dz/batch1-critical';

import { 
    avocatVirtuelDz, douaneCalculator, contratLocationDz, statutsEntrepriseGenerator,
    attestationTravailGenerator, lettreMotivationDz, telecomDzAssistant,
    algeriePosteAssistant, scolariteDzAssistant, logementDzAssistant
} from './admin-dz/batch2-high-priority';

import { 
    permisConduireAssistant, carteGriseAssistant, etatCivilAssistant,
    casierJudiciaireAssistant, serviceNationalAssistant, banquePubliqueAssistant,
    nisNifAssistant, administrationLocaleGuide, recoursAdministratifAssistant,
    calculateurSalaireNet
} from './admin-dz/batch3-medium-priority';

export const adminDzTools: AITool[] = [
    cnasAssistant,
    casnosSimulator,
    impotsDzAssistant,
    cnrcAssistant,
    sonelgazAssistant,
    seaalAssistant,
    cnrRetraiteAssistant,
    anemEmploiAssistant,
    ansejCnacAssistant,
    passeportCniAssistant,
    avocatVirtuelDz,
    douaneCalculator,
    contratLocationDz,
    statutsEntrepriseGenerator,
    attestationTravailGenerator,
    lettreMotivationDz,
    telecomDzAssistant,
    algeriePosteAssistant,
    scolariteDzAssistant,
    logementDzAssistant,
    permisConduireAssistant,
    carteGriseAssistant,
    etatCivilAssistant,
    casierJudiciaireAssistant,
    serviceNationalAssistant,
    banquePubliqueAssistant,
    nisNifAssistant,
    administrationLocaleGuide,
    recoursAdministratifAssistant,
    calculateurSalaireNet
];
