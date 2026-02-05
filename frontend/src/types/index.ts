// API Response Types matching backend schemas

export interface UserResponse {
  id: string;
  email: string;
  email_verified: boolean;
  role: string;
  created_at: string;
}

export interface ResultResponse {
  id: string;
  sample_id: string;
  status: 'authentic' | 'suspect' | 'inconclusive';
  confidence: number;
  model_version: string;
  summary: string | null;
  created_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export type SampleType = 'flour' | 'spice' | 'herb' | 'other';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  password: string;
}

export interface ApiError {
  detail: string;
}

export interface PaginatedResults {
  items: ResultResponse[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface DashboardStats {
  total_samples: number;
  authentic_count: number;
  suspect_count: number;
  recent_results: ResultResponse[];
}
