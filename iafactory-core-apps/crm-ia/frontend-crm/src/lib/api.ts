// src/lib/api.ts

import {
  ClientCreate, Client, ClientUpdate,
  CaseCreate, Case, CaseUpdate,
  NoteCreate, Note,
  FileInfo,
  AIAnalysisResponse
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8212';

async function callApi<T>(endpoint: string, method: string, data?: any, isFormData: boolean = false): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers: HeadersInit = isFormData ? {} : { 'Content-Type': 'application/json' };

  const config: RequestInit = {
    method,
    headers,
  };

  if (data) {
    if (isFormData) {
      config.body = data;
    } else {
      config.body = JSON.stringify(data);
    }
  }

  const response = await fetch(url, config);

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || `API Error: ${response.status} - ${response.statusText}`);
  }

  return response.json();
}

// --- Client Endpoints ---
export const clientApi = {
  create: (data: ClientCreate): Promise<Client> => callApi('/api/crm/client', 'POST', data),
  list: (): Promise<Client[]> => callApi('/api/crm/clients', 'GET'),
  get: (id: string): Promise<Client> => callApi(`/api/crm/client/${id}`, 'GET'),
  update: (id: string, data: ClientUpdate): Promise<Client> => callApi(`/api/crm/case/${id}`, 'PATCH', data),
  delete: (id: string): Promise<{ success: boolean; message: string }> => callApi(`/api/crm/client/${id}`, 'DELETE'),
};

// --- Case Endpoints ---
export const caseApi = {
  create: (data: CaseCreate): Promise<Case> => callApi('/api/crm/case', 'POST', data),
  list: (clientId?: string): Promise<Case[]> => callApi(`/api/crm/cases${clientId ? `?client_id=${clientId}` : ''}`, 'GET'),
  get: (id: string): Promise<Case> => callApi(`/api/crm/case/${id}`, 'GET'),
  update: (id: string, data: CaseUpdate): Promise<Case> => callApi(`/api/crm/case/${id}`, 'PATCH', data),
  delete: (id: string): Promise<{ success: boolean; message: string }> => callApi(`/api/crm/case/${id}`, 'DELETE'),
};

// --- Note Endpoints ---
export const noteApi = {
  create: (caseId: string, data: NoteCreate): Promise<Note> => callApi(`/api/crm/case/${caseId}/note`, 'POST', data),
  list: (caseId: string): Promise<Note[]> => callApi(`/api/crm/case/${caseId}/notes`, 'GET'),
};

// --- File Endpoints ---
export const fileApi = {
  upload: (caseId: string, file: File): Promise<FileInfo> => {
    const formData = new FormData();
    formData.append('file', file);
    return callApi(`/api/crm/case/${caseId}/file`, 'POST', formData, true);
  },
  list: (caseId: string): Promise<FileInfo[]> => callApi(`/api/crm/case/${caseId}/files`, 'GET'),
  download: (fileId: string): string => `${API_BASE_URL}/api/crm/files/${fileId}`,
};

// --- AI Analysis Endpoints ---
export const aiApi = {
  analyzeCase: (caseId: string): Promise<AIAnalysisResponse> => callApi(`/api/crm/case/${caseId}/ai-analyze`, 'POST'),
};

// --- General ---
export const generalApi = {
    getHealth: (): Promise<any> => callApi('/health', 'GET'),
    getStats: (): Promise<any> => callApi('/api/crm/stats', 'GET'),
};
