/**
 * Types pour le système de présentation style ithy.ai
 * Adapté pour IA Factory RAG (Algérie/Suisse)
 */

export interface IthyResponseProps {
  title: string;
  sections: Section[];
  sources: Source[];
  charts?: ChartData[];
  faqs?: FAQ[];
  metadata: ResponseMetadata;
}

export interface Section {
  id: string;
  type: 'text' | 'table' | 'chart' | 'faq' | 'alert' | 'legal-reference';
  title: string;
  content: any;
  icon?: string;
}

export interface Source {
  id: string;
  title: string;
  url?: string;
  type: 'law' | 'decree' | 'circular' | 'jurisprudence' | 'official' | 'academic';
  country: 'DZ' | 'CH';
  date?: string;
  reference?: string; // Ex: "Loi n°90-10 du 14 avril 1990"
  relevance: number;
}

export interface ChartData {
  type: 'radar' | 'bar' | 'pie' | 'comparison';
  title: string;
  data: any[];
  config?: {
    colors?: string[];
    showLegend?: boolean;
    height?: number;
  };
}

export interface FAQ {
  question: string;
  answer: string;
  category?: string;
  relatedSources?: string[];
}

export interface ResponseMetadata {
  generatedAt: Date;
  agents: string[];
  confidence: number;
  language: 'fr' | 'ar' | 'de' | 'amazigh' | 'en';
}

export interface ComparisonRow {
  criterion: string;
  algerie: string | number;
  suisse: string | number;
  notes?: string;
}

export type AlertType = 'warning' | 'info' | 'success' | 'error';

export interface LegalAlertProps {
  type: AlertType;
  title: string;
  content: string;
  legalBasis?: string;
}
