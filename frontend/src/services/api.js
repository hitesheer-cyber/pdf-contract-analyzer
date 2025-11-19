import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const uploadContract = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/contracts/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const getContracts = async (skip = 0, limit = 10) => {
  const response = await api.get('/contracts', {
    params: { skip, limit },
  });

  return response.data;
};

export const getContract = async (contractId) => {
  const response = await api.get(`/contracts/${contractId}`);
  return response.data;
};

export const getAnalytics = async () => {
  const response = await api.get('/analytics');
  return response.data;
};

export default api;
