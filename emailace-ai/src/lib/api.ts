// API service for EmailAce AI
const API_BASE_URL = 'http://localhost:8000/api/v1';

export interface Email {
  id: number;
  sender: string;
  subject: string;
  body: string;
  date: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  priority: 'urgent' | 'high' | 'normal' | 'low';
  status: 'pending' | 'resolved' | 'archived';
  draft_reply?: string;
  is_urgent: boolean;
  summary?: string;
  entities?: string;
}

export interface Analytics {
  total_emails: number;
  resolved_emails: number;
  pending_emails: number;
  urgent_emails: number;
  sentiment_breakdown: Record<string, number>;
  priority_breakdown: Record<string, number>;
}

export interface ReplyResponse {
  draft_reply: string;
  sentiment: string;
  priority: string;
  summary: string;
  entities: Record<string, any>;
}

class ApiService {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  // Email endpoints
  async getEmails(): Promise<Email[]> {
    return this.request<Email[]>('/emails');
  }

  async getEmailDetail(id: number): Promise<Email> {
    return this.request<Email>(`/emails/${id}`);
  }

  async generateReply(id: number, customPrompt?: string): Promise<ReplyResponse> {
    return this.request<ReplyResponse>(`/emails/${id}/generate-reply`, {
      method: 'POST',
      body: JSON.stringify({ custom_prompt: customPrompt }),
    });
  }

  async sendReply(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/emails/${id}/send-reply`, {
      method: 'POST',
    });
  }

  async archiveEmail(id: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/emails/${id}/archive`, {
      method: 'POST',
    });
  }

  async searchEmails(query: string): Promise<Email[]> {
    return this.request<Email[]>(`/emails/search/${encodeURIComponent(query)}`);
  }

  // Analytics endpoints
  async getAnalytics(): Promise<Analytics> {
    return this.request<Analytics>('/analytics');
  }

  // Health check
  async healthCheck(): Promise<{ status: string; timestamp: string; database_connected: boolean }> {
    return this.request<{ status: string; timestamp: string; database_connected: boolean }>('/');
  }
}

export const apiService = new ApiService();


