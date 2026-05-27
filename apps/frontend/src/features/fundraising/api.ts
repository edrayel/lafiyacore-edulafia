import { apiClient } from '../../shared/api/client';

export interface FundraisingCampaign {
  id: string;
  name: string;
  description?: string;
  target_amount: number;
  raised_amount: number;
  start_date: string;
  end_date: string;
  status: string;
  created_at: string;
}

export interface CreateCampaignPayload {
  name: string;
  description?: string;
  target_amount: number;
  start_date: string;
  end_date: string;
}

export async function getCampaigns(params?: { status?: string }): Promise<FundraisingCampaign[]> {
  const { data } = await apiClient.get('/fundraising/campaigns', { params });
  return data;
}

export async function createCampaign(payload: CreateCampaignPayload): Promise<FundraisingCampaign> {
  const { data } = await apiClient.post('/fundraising/campaigns', payload);
  return data;
}

export async function addDonation(campaignId: string, amount: number): Promise<void> {
  await apiClient.post(`/fundraising/campaigns/${campaignId}/donations`, { amount });
}
