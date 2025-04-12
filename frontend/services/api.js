import axios from 'axios';


const backendUrl = import.meta.env.VITE_BACKEND_URL;

const api = axios.create({
  baseURL:backendUrl,
  timeout: 10000,
});

export default api;
