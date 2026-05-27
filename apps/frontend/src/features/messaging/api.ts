import { apiClient } from '../../shared/api/client';

export interface Message {
  id: string;
  sender_id: string;
  receiver_id: string;
  content: string;
  read_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Conversation {
  user_id: string;
  last_message: Message;
  unread_count: number;
}

export interface SendMessagePayload {
  receiver_id: string;
  content: string;
}

export async function getConversations(): Promise<Conversation[]> {
  const { data } = await apiClient.get('/messaging/conversations');
  return data;
}

export async function getMessages(partnerId: string): Promise<Message[]> {
  const { data } = await apiClient.get(`/messaging/conversations/${partnerId}`);
  return data;
}

export async function sendMessage(payload: SendMessagePayload): Promise<Message> {
  const { data } = await apiClient.post('/messaging/send', payload);
  return data;
}
