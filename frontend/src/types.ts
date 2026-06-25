export type DatabaseType = 'MySQL' | 'PostgreSQL';

export type ResponseType = 'chart' | 'forecast' | 'text';

export interface QueryResponse {
  type: ResponseType;
  data: string[];
  chart_path?: string;
  chart_type?: 'bar' | 'line' | 'pie';
  insight?: string;
  sql: string;
  summary?: {
    [key: string]: any;
  };
  // Forecast-specific
  historical?: string[];
  forecast?: string[];
}

export type MessageRole = 'user' | 'assistant';

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
  status: 'sending' | 'sent' | 'error';
  results?: QueryResponse;
  fileName?: string;
}
