// src/lib/types.ts

// Enums (mirroring Python enums from main.py)
export type ClientType = "freelance" | "pme" | "particulier" | "entreprise" | "cabinet";
export type CaseStatus = "ouvert" | "en_cours" | "en_attente" | "ferme";
export type CasePriority = "basse" | "moyenne" | "haute" | "urgente";
export type CaseCategory = "juridique" | "fiscal" | "administratif" | "business" | "rh" | "autre";
export type NoteAuthor = "user" | "ai";

// --- Client Types ---
export interface ClientCreate {
  name: string;
  email?: string;
  phone?: string;
  type?: ClientType;
  activity_sector?: string;
  address?: string;
  notes?: string;
}

export interface Client extends ClientCreate {
  id: string;
  user_id?: string;
  created_at: string;
  updated_at: string;
  cases_count?: number; // Calculated field
}

export interface ClientUpdate {
  name?: string;
  email?: string;
  phone?: string;
  type?: ClientType;
  activity_sector?: string;
  address?: string;
  notes?: string;
}

// --- Case Types ---
export interface CaseCreate {
  client_id: string;
  title: string;
  description?: string;
  status?: CaseStatus;
  priority?: CasePriority;
  category?: CaseCategory;
  tags?: string[];
}

export interface Case extends CaseCreate {
  id: string;
  created_at: string;
  updated_at: string;
  last_ai_update?: string;
  notes_count?: number; // Calculated field
  files_count?: number; // Calculated field
  client_name?: string; // Calculated field
}

export interface CaseUpdate {
  title?: string;
  description?: string;
  status?: CaseStatus;
  priority?: CasePriority;
  category?: CaseCategory;
  tags?: string[];
}

// --- Note Types ---
export interface NoteCreate {
  content: string;
  author_type?: NoteAuthor;
}

export interface Note extends NoteCreate {
  id: string;
  case_id: string;
  created_at: string;
}

// --- File Types ---
export interface FileInfo {
  id: string;
  case_id: string;
  file_name: string;
  file_url: string;
  file_type?: string;
  file_size?: number;
  uploaded_at: string;
}

// --- AI Analysis Types ---
export interface AIAnalysisResponse {
  success: boolean;
  summary: string;
  action_items?: string[];
  risks?: string[];
  recommended_docs?: string[];
  next_steps?: string[];
  legal_insights?: string;
  fiscal_insights?: string;
  references?: { title: string; source: string; }[]; // Assuming simple structure
  analysis_timestamp: string;
  credits_used?: number;
}
