import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const processTransaction = async (data) => {
  const response = await api.post('/transaction', data);
  return response.data;
};

export const fetchAlerts = async () => {
  const response = await api.get('/alerts');
  return response.data;
};

export const fetchTrace = async (accountId) => {
  const response = await api.get(`/trace/${accountId}`);
  return response.data;
};

export const runScenario = async (name) => {
  const response = await api.post(`/simulation/run/${name}`);
  return response.data;
};

export const resetSystem = async () => {
  const response = await api.post('/simulation/reset');
  return response.data;
};

export const fetchHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

export const fetchAccountSummary = async (accountId) => {
  const response = await api.get(`/account/${accountId}`);
  return response.data;
};