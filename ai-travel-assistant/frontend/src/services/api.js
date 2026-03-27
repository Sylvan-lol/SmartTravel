import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8081/api';

export async function sendMessage(messages) {
  const response = await axios.post(`${API_BASE}/chat`, { messages, user_id: 'default' });
  return response.data;
}